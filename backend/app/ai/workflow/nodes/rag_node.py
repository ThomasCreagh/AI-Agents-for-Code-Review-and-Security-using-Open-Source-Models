from langchain_core.messages import SystemMessage
from app.models import AgentState
import time

from app.ai.dependencies import AIDependencies
from app.ai.llm.llm import count_tokens
from app.ai.workflow.utils import log_debug
from app.ai.workflow.tools.document_tools import retrieve_documents, format_documents, enhance_query_with_code_analysis
from app.ai.workflow.tools.message_tools import create_context_message, create_error_message

def rag_agent(state: AgentState, deps: AIDependencies):
    messages = state["messages"]
    query = state["latest_user_message"]
    context = state.get("context", {})
    
    if count_tokens(query) > deps.token_limit:
        query = query[:1500]  # ~500 tokens for average text
        log_debug("Query truncated to ~500 tokens for performance")
    
    code_analysis = context.get("code_analysis", [])
    
    enhanced_query = enhance_query_with_code_analysis(query, code_analysis)

    try:
        docs = retrieve_documents(deps.vector_store, enhanced_query, k=deps.max_documents)

        if deps.enable_throttling:
            time.sleep(deps.throttling_delay)

        context_text, doc_sources = format_documents(docs)
        
        context_message = create_context_message(context_text)

        return {
            "messages": messages + [context_message],
            "context": {
                "retrieved_docs": docs if docs else [],
                "doc_sources": doc_sources,
                "query_used": enhanced_query,
                "code_analysis": code_analysis 
            },
            "latest_user_message": query
        }
    except Exception as e:
        log_debug(f"Error in RAG agent: {str(e)}")
        error_message = create_error_message("Could not retrieve context from the database. Proceeding with analysis based on available information only.")
        return {
            "messages": messages + [error_message],
            "context": {
                "retrieved_docs": [],
                "doc_sources": [],
                "query_used": enhanced_query,
                "code_analysis": code_analysis
            },
            "latest_user_message": query
        }