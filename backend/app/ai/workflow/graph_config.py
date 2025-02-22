from typing import TypedDict, List, Dict, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END, START
from langgraph.types import interrupt
from ..database.db_query import query_database
import os
import json

# Setup debug logging (always enabled)
DEBUG_LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(DEBUG_LOG_PATH, exist_ok=True)
DEBUG_LOG_FILE = os.path.join(DEBUG_LOG_PATH, "rag_debug.log")

def log_debug(message):
    """Write debug message to log file and console"""
    print(f"[RAG DEBUG] {message}")
    with open(DEBUG_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{message}\n")

class AgentState(TypedDict):
    messages: List[BaseMessage]  # All conversation messages
    latest_user_message: str     # The most recent user message
    context: Dict[str, Any]      # Holds retrieved context and other data

# RAG Agent - Retrieves relevant information
def rag_agent(state: AgentState, vector_store, llm):
    """Agent that retrieves context from the vector store."""
    messages = state["messages"]
    query = state["latest_user_message"]
    
    log_debug(f"Processing query: '{query}'")
    
    # Retrieve documents using vector_store
    docs = query_database(vector_store, query, k=3)
    log_debug(f"Retrieved {len(docs)} documents")
    
    # Log document details
    for i, doc in enumerate(docs):
        # Get metadata if available
        metadata = getattr(doc, 'metadata', {})
        source = metadata.get('source', 'unknown')
        
        # Document preview (truncated)
        preview = doc.page_content[:150] + "..." if len(doc.page_content) > 150 else doc.page_content
        log_debug(f"Document {i+1} from '{source}':\n{preview}")
        
        # Log similarity score if available
        if hasattr(doc, 'metadata') and 'score' in doc.metadata:
            log_debug(f"Similarity score: {doc.metadata['score']}")
    
    if not docs or len(docs) == 0:
        context = "No relevant information found in the knowledge base."
        log_debug("WARNING: No relevant documents were found in the vector store")
    else:
        context = "\n".join(doc.page_content for doc in docs)
        log_debug(f"Total context length: {len(context)} characters")
    
    # Create a context message
    context_message = SystemMessage(
        content=f"Context for the security question:\n\n{context}"
    )
    
    # Store document references in context for later verification
    doc_sources = [getattr(doc, 'metadata', {}).get('source', 'unknown') for doc in docs]
    
    # Return the updated state with context and document sources
    return {
        "messages": messages + [context_message],
        "context": {
            "retrieved_docs": docs if docs else [],
            "doc_sources": doc_sources,
            "query_used": query
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
        log_debug(f"Security analysis using documents from: {', '.join(doc_sources)}")
    
    # Create a specialized prompt for security analysis
    security_prompt = SystemMessage(content="""
    You are a specialized security analysis agent. Your task is to:
    1. Identify potential security vulnerabilities in the user's question
    2. Analyze the security implications 
    3. Provide a detailed security assessment
    
    Analyze the query and any provided context. If you don't have specific information
    about the topic in the context, clearly state that limitation but still provide 
    your assessment based on the query itself.
    
    At the end of your response, indicate the source of your information 
    (either from the provided context documents or from general knowledge).
    """)
    
    # Create a human message with the original query to ensure it's processed
    query_message = HumanMessage(content=f"Security analysis for: {query}")
    
    # Prepare the messages for the LLM
    agent_messages = [security_prompt] + messages + [query_message]
    
    log_debug(f"Sending security analysis request to LLM with {len(agent_messages)} messages")
    
    # Get a response from the LLM
    response = llm.invoke(agent_messages)
    
    # Convert to AIMessage if it's not already
    if not isinstance(response, AIMessage):
        response = AIMessage(content=str(response))
    
    log_debug(f"Received security analysis response: {response.content[:100]}...")
    
    # Return the updated state
    return {
        "messages": messages + [response],
        "latest_user_message": query,
        "context": state.get("context", {})  # Preserve the context
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
    
    If the context doesn't contain specific information about the user's query, acknowledge 
    this limitation and suggest that the user might want to add relevant documents to 
    the knowledge base for better responses in the future.
    
    At the end of your response, please add a separate section titled "Sources:" that briefly 
    mentions whether your response was primarily based on the retrieved documents or on 
    general knowledge.
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

# Function to get user input
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
        "context": state.get("context", {})  # Preserve context
    }

# Create the graph
def create_security_rag_graph(llm, vector_store):
    # Define the graph with our custom state
    workflow = StateGraph(AgentState)
    
    # Add nodes to the graph
    workflow.add_node("rag", lambda state: rag_agent(state, vector_store, llm))
    workflow.add_node("security", lambda state: security_analysis_agent(state, llm))
    workflow.add_node("generate_response", lambda state: generate_response(state, llm))
    workflow.add_node("get_user_input", get_user_input)
    
    # Add edges
    workflow.add_edge(START, "rag")
    workflow.add_edge("rag", "security")
    workflow.add_edge("security", "generate_response")
    workflow.add_edge("generate_response", "get_user_input")
    workflow.add_edge("get_user_input", "rag")
    
    return workflow