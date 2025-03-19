from langchain_core.messages import HumanMessage
from langgraph.types import interrupt
from app.models import AgentState

from ..utils import log_debug

def get_user_input(state: AgentState):
    """Interrupts the graph to get user input."""
    value = interrupt({})

    log_debug(f"Received new user input: {value}")

    human_message = HumanMessage(content=value)

    return {
        "latest_user_message": value,
        "messages": state["messages"] + [human_message],
        "context": {}  
    }