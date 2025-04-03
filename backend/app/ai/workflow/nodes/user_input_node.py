from langchain_core.messages import HumanMessage
from langgraph.types import interrupt
from app.models import AgentState

from ..utils import (
    log_debug, log_agent_start, log_agent_end,
    LOG_LEVEL_INFO, LOG_LEVEL_DEBUG,
    SECTION_SEPARATOR
)

def get_user_input(state: AgentState):
    """Interrupts the graph to get user input."""
    # Log agent start
    log_agent_start("USER INPUT", state)
    
    # Store original state for comparison
    original_state = state.copy()
    
    # Interrupt for user input
    log_debug("Waiting for user input...", level=LOG_LEVEL_INFO)
    value = interrupt({})

    # Log received input
    preview = value[:100] + "..." if len(value) > 100 else value
    log_debug(f"Received new user input: {preview}", level=LOG_LEVEL_INFO)
    
    # Log conversation length
    message_count = len(state["messages"])
    log_debug(f"Current conversation length: {message_count} messages", level=LOG_LEVEL_DEBUG)

    # Create human message
    human_message = HumanMessage(content=value)
    
    # Log cycle completion
    log_debug(f"{SECTION_SEPARATOR}", level=LOG_LEVEL_INFO)
    log_debug("STARTING NEW CONVERSATION CYCLE", level=LOG_LEVEL_INFO)
    log_debug(f"{SECTION_SEPARATOR}", level=LOG_LEVEL_INFO)

    # Create updated state
    new_state = {
        "latest_user_message": value,
        "messages": state["messages"] + [human_message],
        "context": {}  # Reset context for new cycle
    }
    
    # Log agent end
    log_agent_end("USER INPUT", original_state, new_state)
    
    return new_state