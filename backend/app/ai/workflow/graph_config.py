from langgraph.graph import StateGraph, END, START

from app.models import AgentState
from app.ai.dependencies import AIDependencies
from .nodes.rag_node import rag_agent
from .nodes.security_node import security_analysis_agent
from .nodes.response_node import generate_response
from .nodes.user_input_node import get_user_input
from .nodes.ast_node import code_analysis_agent
from .nodes.integrated_node import integrated_analysis_agent
from .utils import log_debug

def create_security_rag_graph(deps: AIDependencies):
    workflow = StateGraph(AgentState)

    workflow.add_node("code_analysis", code_analysis_agent)
    workflow.add_node("rag", lambda state: rag_agent(state, deps))
    workflow.add_node("integrate", integrated_analysis_agent)
    workflow.add_node("security", lambda state: security_analysis_agent(state, deps))
    workflow.add_node("generate_response", lambda state: generate_response(state, deps))
    workflow.add_node("get_user_input", get_user_input)

    workflow.add_edge(START, "code_analysis")
    workflow.add_edge("code_analysis", "rag")
    workflow.add_edge("rag", "integrate")
    workflow.add_edge("integrate", "security")
    workflow.add_edge("security", "generate_response")
    workflow.add_edge("generate_response", "get_user_input")
    workflow.add_edge("get_user_input", "code_analysis")

    return workflow