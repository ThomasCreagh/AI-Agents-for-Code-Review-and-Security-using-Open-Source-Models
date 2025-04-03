from langchain_core.messages import SystemMessage
from app.models import AgentState
from ..utils import log_debug, log_agent_start, log_agent_end, LOG_LEVEL_INFO, LOG_LEVEL_DEBUG

def supervisor_agent(state: AgentState, deps):
    """
    Supervisor agent that examines user input and decides which specialized agent to route to.
    
    Routes to:
    - code_analysis: When input contains code or code-related questions
    - rag: When input is a general query that needs information retrieval
    - security: When input explicitly asks about security without code
    """
    # Log agent start
    log_agent_start("SUPERVISOR", state)
    
    # Store original state for comparison
    original_state = state.copy()
    
    messages = state["messages"]
    query = state["latest_user_message"]
    
    # Simple keyword and pattern matching for routing decisions
    code_indicators = ["def ", "class ", "import ", "```python", "from ", "function", "code"]
    security_keywords = ["security", "secure", "vulnerability", "exploit", "risk", "threat", 
                         "authentication", "authorization"]
    
    # Log detailed pattern matching
    detected_code_patterns = [indicator for indicator in code_indicators if indicator in query]
    detected_security_patterns = [keyword for keyword in security_keywords if keyword.lower() in query.lower()]
    
    contains_code = len(detected_code_patterns) > 0
    asks_about_security = len(detected_security_patterns) > 0
    
    # Log pattern detection
    if detected_code_patterns:
        log_debug(f"Code patterns detected: {detected_code_patterns}", level=LOG_LEVEL_DEBUG)
    if detected_security_patterns:
        log_debug(f"Security keywords detected: {detected_security_patterns}", level=LOG_LEVEL_DEBUG)
    
    # Determine the route based on content analysis
    if contains_code:
        route_to = "code_analysis"
        explanation = f"Query contains code patterns: {', '.join(detected_code_patterns[:3])}"
        log_debug(f"Routing decision: {route_to} - {explanation}", level=LOG_LEVEL_INFO)
    elif asks_about_security and not contains_code:
        route_to = "security"
        explanation = f"Query contains security keywords without code: {', '.join(detected_security_patterns[:3])}"
        log_debug(f"Routing decision: {route_to} - {explanation}", level=LOG_LEVEL_INFO)
    else:
        route_to = "rag"
        explanation = "Query requires information retrieval from documentation"
        log_debug(f"Routing decision: {route_to} - {explanation}", level=LOG_LEVEL_INFO)
    
    # Add a system message explaining the routing decision
    routing_message = SystemMessage(
        content=f"Routing query to {route_to}: {explanation}"
    )
    
    # Create updated state
    new_state = {
        "messages": messages + [routing_message],
        "latest_user_message": query,
        "route_to": route_to,  # Add routing information to state
        "context": {}  # Reset context when starting a new route
    }
    
    # Log agent end
    log_agent_end("SUPERVISOR", original_state, new_state)
    
    return new_state