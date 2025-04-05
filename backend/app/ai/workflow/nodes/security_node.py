from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.models import AgentState
import time

from app.ai.dependencies import AIDependencies
from app.ai.workflow.utils import (
    log_debug, log_agent_start, log_agent_end,
    LOG_LEVEL_INFO, LOG_LEVEL_DEBUG
)
from app.ai.workflow.tools.security_tools import format_document_sources, create_security_prompt
from app.ai.workflow.tools.message_tools import create_prompt_message, create_query_message, format_llm_response

def security_analysis_agent(state: AgentState, deps: AIDependencies):
    """
    Performs security analysis based on code analysis and retrieved documents.
    Structured to provide function-specific vulnerability assessment.
    """
    # Log agent start
    log_agent_start("SECURITY ANALYSIS", state)
    
    # Store original state for comparison
    original_state = state.copy()
    
    messages = state["messages"]
    query = state["latest_user_message"]
    context = state.get("context", {})

    # Apply throttling delay
    if deps.enable_throttling:
        delay = deps.throttling_delay
        log_debug(f"Applying throttling delay: {delay}s", level=LOG_LEVEL_DEBUG)
        time.sleep(delay)

    # Get document sources
    doc_sources = context.get("doc_sources", [])
    source_names = format_document_sources(doc_sources)
    
    # Check if we have code analysis
    code_analysis = context.get("code_analysis", [])
    has_code_analysis = len(code_analysis) > 0
    
    # Get code summary if available
    code_summary = context.get("code_summary", None)
    
    # Get full code for references
    full_code = context.get("full_code", [])
    
    # Log security analysis inputs
    log_debug(
        "Security analysis inputs:", 
        level=LOG_LEVEL_INFO,
        data={
            "has_code_analysis": has_code_analysis,
            "has_code_summary": code_summary is not None,
            "code_blocks": len(full_code),
            "document_sources": source_names if source_names else "None",
            "security_focus_areas": deps.security_focus_areas
        }
    )
    
    # Create security prompt, using code_summary if available
    security_prompt_content = create_security_prompt(has_code_analysis, code_summary)
    log_debug(
        "Created security prompt", 
        level=LOG_LEVEL_DEBUG,
        data=security_prompt_content[:100] + "..." if len(security_prompt_content) > 100 else security_prompt_content
    )
    
    # Create a message with the complete original code
    if full_code:
        original_code = "\n".join(full_code)
        full_code_message = SystemMessage(content=f"Complete code for analysis:\n```python\n{original_code}\n```")
        log_debug("Added complete original code to analysis", level=LOG_LEVEL_INFO)
    else:
        full_code_message = None
    
    # Create function index message to help reference code
    if has_code_analysis and code_summary:
        function_index = "Code Functions:\n"
        for i, func_name in enumerate(code_summary.get('functions', [])):
            function_index += f"{i+1}. {func_name}\n"
        
        # Add categories of functions if available
        if code_summary.get('security_operations'):
            function_index += "\nFunction Categories:\n"
            for category, funcs in code_summary.get('security_operations', {}).items():
                if funcs:
                    cat_name = category.replace("_", " ").title()
                    function_index += f"- {cat_name}: {', '.join(funcs[:3])}\n"
        
        function_reference = create_prompt_message(function_index)
        log_debug("Created function reference index", level=LOG_LEVEL_DEBUG)
    else:
        function_reference = None
    
    security_prompt = create_prompt_message(security_prompt_content)
    query_message = create_query_message(query)

    # Create agent messages for LLM
    agent_messages = [security_prompt]
    
    # Add the full code right after the security prompt
    if full_code_message:
        agent_messages.append(full_code_message)
    
    # Add existing messages
    agent_messages.extend(messages)
    
    # Add function reference if available
    if function_reference:
        agent_messages.append(function_reference)
    
    # Add query message at the end
    agent_messages.append(query_message)
    
    log_debug(f"Preparing LLM request with {len(agent_messages)} messages", level=LOG_LEVEL_DEBUG)

    # Log security analysis request
    log_debug(f"Sending security analysis request to LLM", level=LOG_LEVEL_INFO)

    # Get response from LLM
    response = deps.llm.invoke(agent_messages)
    
    # Format response
    formatted_response = format_llm_response(response)
    
    # Log response preview
    response_text = formatted_response.content
    response_preview = response_text[:100] + "..." if len(response_text) > 100 else response_text
    log_debug(
        "Received security analysis response:", 
        level=LOG_LEVEL_DEBUG,
        data=response_preview
    )

    # Create updated state
    new_state = {
        "messages": messages + [formatted_response],
        "latest_user_message": query,
        "context": context  
    }
    
    # Log agent end
    log_agent_end("SECURITY ANALYSIS", original_state, new_state)
    
    return new_state