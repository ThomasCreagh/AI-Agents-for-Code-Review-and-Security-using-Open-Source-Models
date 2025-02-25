from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END, START
from langgraph.types import interrupt
import os

from ..database.db_query import query_database
from app.models import AgentState
from .ast_node import code_analysis_agent
from .integrated_node import integrated_analysis_agent

DEBUG_LOG_PATH = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(DEBUG_LOG_PATH, exist_ok=True)
DEBUG_LOG_FILE = os.path.join(DEBUG_LOG_PATH, "rag_debug.log")


def log_debug(message):
    """Write debug message to log file and console"""
    print(f"[RAG DEBUG] {message}")
    with open(DEBUG_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{message}\n")


def rag_agent(state: AgentState, vector_store, llm):
    """Agent that retrieves context from the vector store."""
    messages = state["messages"]
    query = state["latest_user_message"]
    context = state.get("context", {})
    
    # If we have code analysis, use it to enhance the query
    code_analysis = context.get("code_analysis", [])
    enhanced_query = query
    
    if code_analysis:
        # Extract function names and purposes for better retrieval
        function_info = []
        for analysis in code_analysis:
            for func_name, details in analysis.items():
                params = ', '.join(details['params'])
                function_info.append(f"{func_name}({params})")
        
        if function_info:
            enhanced_query = f"{query} Functions analyzed: {', '.join(function_info)}"
            log_debug(f"Enhanced query with code analysis: '{enhanced_query}'")

    # Retrieve documents using vector_store
    try:
        docs = query_database(vector_store, enhanced_query, k=3)
        log_debug(f"Retrieved {len(docs)} documents")

        # Format documents with citation markers
        formatted_docs = []
        doc_sources = []
        
        for i, doc in enumerate(docs):
            metadata = getattr(doc, 'metadata', {})
            source = metadata.get('source', 'unknown')
            page = metadata.get('page_number', '')
            
            # Add citation marker at end of document content
            citation_id = f"[{i+1}]"
            formatted_content = f"{doc.page_content} {citation_id}"
            formatted_docs.append(formatted_content)
            
            # Store source info for later reference
            doc_sources.append({
                'id': citation_id,
                'source': source,
                'page': page
            })
            
            # Log document details
            preview = doc.page_content[:150] + "..." if len(doc.page_content) > 150 else doc.page_content
            log_debug(f"Document {i+1} from '{source}':\n{preview}")

        if not docs or len(docs) == 0:
            context_text = "No relevant information found in the knowledge base."
            log_debug("WARNING: No relevant documents were found in the vector store")
        else:
            # Join formatted documents with citations
            context_text = "\n\n".join(formatted_docs)
            
            # Add source reference guide at the end
            source_guide = "\n\nSources:\n"
            for src in doc_sources:
                page_info = f", page {src['page']}" if src['page'] else ""
                source_guide += f"{src['id']} {src['source']}{page_info}\n"
            
            context_text += source_guide
            log_debug(f"Total context length: {len(context_text)} characters")

        # Create a context message
        context_message = SystemMessage(
            content=f"Context for the security question:\n\n{context_text}"
        )

        # Return the updated state with context and document sources
        return {
            "messages": messages + [context_message],
            "context": {
                "retrieved_docs": docs if docs else [],
                "doc_sources": doc_sources,
                "query_used": enhanced_query,
                "code_analysis": code_analysis  # Preserve code analysis
            },
            "latest_user_message": query
        }
    except Exception as e:
        log_debug(f"Error in RAG agent: {str(e)}")
        # Create a context message about the error
        error_message = SystemMessage(
            content=f"Note: Could not retrieve context from the database. Proceeding with analysis based on available information only."
        )
        return {
            "messages": messages + [error_message],
            "context": {
                "retrieved_docs": [],
                "doc_sources": [],
                "query_used": enhanced_query,
                "code_analysis": code_analysis  # Preserve code analysis
            },
            "latest_user_message": query
        }


def security_analysis_agent(state: AgentState, llm):
    """Specialized agent that analyzes security concerns."""
    messages = state["messages"]
    query = state["latest_user_message"]
    context = state.get("context", {})

    # Log document sources used for this analysis
    doc_sources = context.get("doc_sources", [])
    if doc_sources:
        source_names = []
        for src in doc_sources:
            if isinstance(src, dict):
                source_names.append(src.get('source', 'unknown'))
            else:
                source_names.append(src)
                
        log_debug(f"Security analysis using documents from: {', '.join(source_names)}")
    
    # Check if we have code analysis results
    code_analysis = context.get("code_analysis", [])
    has_code_analysis = len(code_analysis) > 0
    
    if has_code_analysis:
        log_debug("Security analysis includes code analysis results")

    # Create a specialized prompt for security analysis
    security_prompt_content = """
    You are a specialized security analysis agent. Your task is to:
    1. Identify potential security vulnerabilities in the user's question
    2. Analyze the security implications 
    3. Provide a detailed security assessment
    
    Analyze the query and any provided context. If you don't have specific information
    about the topic in the context, clearly state that limitation but still provide 
    your assessment based on the query itself.
    
    IMPORTANT: When referring to information from security standards or documents, use the 
    citation markers ([1], [2], etc.) that appear in the context to indicate your sources.
    """
    
    # Add code-specific instructions if code was analyzed
    if has_code_analysis:
        security_prompt_content += """
        The user's query includes code that has been analyzed. Pay special attention to:
        - Function parameters that might accept user input
        - Return values that might contain sensitive information
        - Potential security vulnerabilities in the code structure
        - Input validation and sanitization
        - Error handling approaches
        
        Use the code analysis provided to offer specific security recommendations.
        """
    
    security_prompt_content += """
    At the end of your response, indicate the source of your information 
    (either from the provided context documents, code analysis, or from general knowledge).
    """

    security_prompt = SystemMessage(content=security_prompt_content)

    # Create a human message with the original query to ensure it's processed
    query_message = HumanMessage(content=f"Security analysis for: {query}")

    # Prepare the messages for the LLM
    agent_messages = [security_prompt] + messages + [query_message]

    log_debug(
        f"Sending security analysis request to LLM with {len(agent_messages)} messages")

    # Get a response from the LLM
    response = llm.invoke(agent_messages)

    # Convert to AIMessage if it's not already
    if not isinstance(response, AIMessage):
        response = AIMessage(content=str(response))

    log_debug(
        f"Received security analysis response: {response.content[:100]}...")

    # Return the updated state
    return {
        "messages": messages + [response],
        "latest_user_message": query,
        "context": context  # Preserve the context
    }


def generate_response(state: AgentState, llm):
    """Generate a final response to the user."""
    messages = state["messages"]
    query = state["latest_user_message"]
    context = state.get("context", {})

    # Create a prompt for the final response with source verification
    response_prompt = SystemMessage(content="""
    Based on the security analysis and retrieved information, provide a comprehensive
    response to the user's question. 
    
    When referring to information from the documents in your response, use citation 
    markers like [1], [2], etc. that match the citation markers in the context.
    
    If the context doesn't contain specific information about the user's query, acknowledge 
    this limitation and suggest that the user might want to add relevant documents to 
    the knowledge base for better responses in the future.
    
    At the end of your response, please add a separate section titled "## Sources" that lists all
    the documents you referenced, with their full citation information as provided in the context.
    Also indicate which parts of your response were based on these sources versus general knowledge.
    
    Format the sources section like this:
    
    ## Sources
    
    [1] Document Name, Page X - Used for information on <specific topic>
    [2] Document Name - Used for information on <specific topic>
    [General Knowledge] - Used for information on <specific topics not covered by documents>
    """)

    # Create a human message with the original query
    query_message = HumanMessage(content=f"User question: {query}")

    # Prepare the messages for the LLM
    agent_messages = [response_prompt] + messages + [query_message]

    log_debug(f"Sending final response request to LLM")

    # Get a response from the LLM
    response = llm.invoke(agent_messages)

    # Convert to AIMessage if it's not already
    if not isinstance(response, AIMessage):
        response = AIMessage(content=str(response))

    log_debug(f"Final response generated: {response.content[:100]}...")

    # Return the updated state with the AI's response added to messages
    return {
        "messages": messages + [response],
        "latest_user_message": query,
        "context": context  # Preserve the context
    }


def get_user_input(state: AgentState):
    """Interrupts the graph to get user input."""
    # Use LangGraph's interrupt mechanism to get user input
    value = interrupt({})

    log_debug(f"Received new user input: {value}")

    # Create a human message from the user input
    human_message = HumanMessage(content=value)

    # Update the latest user message and add to message history
    return {
        "latest_user_message": value,
        "messages": state["messages"] + [human_message],
        "context": {}  # Reset context for each new query
    }


def create_security_rag_graph(llm, vector_store):
    # Define the graph with our custom state
    workflow = StateGraph(AgentState)

    # Add nodes to the graph
    workflow.add_node("code_analysis", code_analysis_agent)
    workflow.add_node("rag", lambda state: rag_agent(state, vector_store, llm))
    workflow.add_node("integrate", integrated_analysis_agent)
    workflow.add_node("security", lambda state: security_analysis_agent(state, llm))
    workflow.add_node("generate_response", lambda state: generate_response(state, llm))
    workflow.add_node("get_user_input", get_user_input)

    # Add edges - new flow: analyze code first, then query RAG
    workflow.add_edge(START, "code_analysis")
    workflow.add_edge("code_analysis", "rag")
    workflow.add_edge("rag", "integrate")
    workflow.add_edge("integrate", "security")
    workflow.add_edge("security", "generate_response")
    workflow.add_edge("generate_response", "get_user_input")
    workflow.add_edge("get_user_input", "code_analysis")

    return workflow