from langgraph.graph import StateGraph, END, START

from app.models import AgentState
from app.ai.dependencies import AIDependencies
from .nodes.rag_node import rag_agent
from .nodes.security_node import security_analysis_agent
from .nodes.response_node import generate_response
from .nodes.user_input_node import get_user_input
from .nodes.ast_node import code_analysis_agent
from .nodes.integrated_node import integrated_analysis_agent
from .nodes.supervisor_node import supervisor_agent
from .nodes.bandit_node import bandit_analysis_agent  # Import the new Bandit node
from .utils import log_debug

def create_security_rag_graph(deps: AIDependencies):
    """
    Create a supervisor-based workflow for security analysis.
    
    The supervisor examines the user input and routes to the appropriate specialized agent:
    - code_analysis: When input contains code
    - rag: When input requires information retrieval
    - security: When input asks about security without code
    
    All routes converge at the generate_response node for final answer generation.
    """
    workflow = StateGraph(AgentState)

    # Add nodes to the graph
    workflow.add_node("supervisor", lambda state: supervisor_agent(state, deps))
    workflow.add_node("code_analysis", code_analysis_agent)
    workflow.add_node("bandit", bandit_analysis_agent)  # Add Bandit node
    workflow.add_node("rag", lambda state: rag_agent(state, deps))
    workflow.add_node("integrate", integrated_analysis_agent)
    workflow.add_node("security", lambda state: security_analysis_agent(state, deps))
    workflow.add_node("generate_response", lambda state: generate_response(state, deps))
    workflow.add_node("get_user_input", get_user_input)

    # Define conditional routing based on supervisor's decision
    def route_based_on_supervisor(state):
        route = state.get("route_to", "rag")  # Default to RAG if no route specified
        log_debug(f"Routing to {route} based on supervisor decision")
        return route

    # Connect supervisor to specialized agents based on routing decision
    workflow.add_conditional_edges(
        "supervisor",
        route_based_on_supervisor,
        {
            "code_analysis": "code_analysis",
            "rag": "rag",
            "security": "security"
        }
    )

    # Connect the workflow from START to supervisor
    workflow.add_edge(START, "supervisor")
    
    # Connect code_analysis to bandit
    workflow.add_edge("code_analysis", "bandit")
    
    # Connect bandit to RAG (code analysis with bandit results needs context from docs)
    workflow.add_edge("bandit", "rag")
    
    # Connect RAG to integrate 
    workflow.add_edge("rag", "integrate")
    
    # Connect integrate to security
    workflow.add_edge("integrate", "security")
    
    # All specialized processing paths converge at generate_response
    workflow.add_edge("security", "generate_response")
    
    # Connect response generation to user input for the next cycle
    workflow.add_edge("generate_response", "get_user_input")
    
    # Connect back to supervisor for next cycle
    workflow.add_edge("get_user_input", "supervisor")
    
    return workflow