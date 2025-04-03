from langchain_core.messages import SystemMessage
from app.models import AgentState
import time

from app.ai.dependencies import AIDependencies
from app.ai.llm.llm import count_tokens
from app.ai.workflow.utils import (
    log_debug, log_agent_start, log_agent_end,
    LOG_LEVEL_INFO, LOG_LEVEL_DEBUG, LOG_LEVEL_ERROR, LOG_LEVEL_WARN,
    format_document_preview
)
from app.ai.workflow.tools.document_tools import (
    retrieve_documents, format_documents, enhance_query_with_code_summary
)
from app.ai.workflow.tools.message_tools import create_context_message, create_error_message

def rag_agent(state: AgentState, deps: AIDependencies):
    """
    Retrieval Augmented Generation agent that retrieves relevant documents
    based on the user query and adds them to the context.
    """
    # Log agent start
    log_agent_start("RAG", state)
    
    # Store original state for comparison
    original_state = state.copy()
    
    messages = state["messages"]
    query = state["latest_user_message"]
    context = state.get("context", {})
    
    # Only truncate query if it exceeds the token limit
    original_query_length = len(query)
    original_token_count = count_tokens(query)
    
    if count_tokens(query) > deps.token_limit:
        query = query[:2000]  # ~500 tokens for average text
        truncated_token_count = count_tokens(query)
        log_debug(
            f"Query truncated from {original_token_count} to {truncated_token_count} tokens", 
            level=LOG_LEVEL_WARN
        )
    
    # Get code analysis from context
    code_analysis = context.get("code_analysis", [])
    
    # Get structured code summary if available
    code_summary = context.get("code_summary", None)
    
    # Enhance query with code summary if available
    enhanced_query = enhance_query_with_code_summary(query, code_summary)
    
    if enhanced_query != query:
        log_debug(
            "Query enhancement details:", 
            level=LOG_LEVEL_DEBUG,
            data={
                "original_query_length": original_query_length,
                "enhanced_query_length": len(enhanced_query),
                "enhancement_source": "Code summary"
            }
        )

    try:
        # Log retrieval attempt
        log_debug(
            f"Retrieving documents with k={deps.max_documents}", 
            level=LOG_LEVEL_INFO
        )
        
        # Retrieve documents
        docs = retrieve_documents(deps.vector_store, enhanced_query, k=deps.max_documents)
        
        # Log document retrieval results
        if docs:
            log_debug(
                f"Retrieved {len(docs)} documents", 
                level=LOG_LEVEL_INFO
            )
            
            # Log document preview
            doc_preview = format_document_preview(docs)
            log_debug(
                "Document previews:", 
                level=LOG_LEVEL_DEBUG,
                data=doc_preview
            )
            
            # Log sources for verification
            sources = []
            for doc in docs:
                metadata = getattr(doc, 'metadata', {})
                source = metadata.get('source', 'unknown')
                sources.append(source)
            
            log_debug(
                "Retrieved document sources:", 
                level=LOG_LEVEL_INFO,
                data=sources
            )
        else:
            log_debug(
                "No documents retrieved from vector store", 
                level=LOG_LEVEL_WARN
            )

        # Apply throttling if enabled
        if deps.enable_throttling:
            log_debug(
                f"Applying throttling delay: {deps.throttling_delay}s", 
                level=LOG_LEVEL_DEBUG
            )
            time.sleep(deps.throttling_delay)

        # Format documents for context
        context_text, doc_sources = format_documents(docs)
        
        # Create context message
        context_message = create_context_message(context_text)

        # Log the source information being stored
        log_debug(
            f"Storing {len(doc_sources)} document sources in context", 
            level=LOG_LEVEL_INFO,
            data=[src.get('source', 'unknown') for src in doc_sources]
        )

        # Create updated state
        new_state = {
            "messages": messages + [context_message],
            "context": {
                "retrieved_docs": docs if docs else [],
                "doc_sources": doc_sources,
                "query_used": enhanced_query,
                "code_analysis": code_analysis,
                "code_summary": code_summary,  # Keep code_summary in context
                "security_standards_used": [src.get('source', 'unknown') for src in doc_sources]  # Add this explicit list
            },
            "latest_user_message": query
        }
        
        # Log agent end
        log_agent_end("RAG", original_state, new_state)
        
        return new_state
        
    except Exception as e:
        log_debug(f"Error in RAG agent: {str(e)}", level=LOG_LEVEL_ERROR)
        
        # Create error message
        error_message = create_error_message(
            "Could not retrieve context from the database. Proceeding with analysis based on available information only."
        )
        
        # Create updated state with error
        new_state = {
            "messages": messages + [error_message],
            "context": {
                "retrieved_docs": [],
                "doc_sources": [],
                "query_used": enhanced_query,
                "code_analysis": code_analysis,
                "code_summary": code_summary,  # Keep code_summary in context even on error
                "security_standards_used": []  # Empty list for failed retrieval
            },
            "latest_user_message": query
        }
        
        # Log agent end (with error)
        log_agent_end("RAG", original_state, new_state)
        
        return new_state