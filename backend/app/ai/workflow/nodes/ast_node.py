from langchain_core.messages import SystemMessage
from app.models import AgentState
from app.ai.workflow.utils import (
    log_debug, log_agent_start, log_agent_end, 
    LOG_LEVEL_INFO, LOG_LEVEL_DEBUG, LOG_LEVEL_ERROR,
    format_code_analysis
)
from app.ai.workflow.tools.code_tools import (
    detect_code_in_query, extract_code_blocks, 
    analyze_code_blocks, format_analysis_results, create_code_summary
)
from app.ai.workflow.tools.message_tools import create_analysis_message
from app.ai.dependencies import get_ai_dependencies

def code_analysis_agent(state: AgentState):
    """
    Agent that analyzes code in the user query.
    Extracts code blocks, performs AST analysis, and adds analysis results to the state.
    """
    # Log agent start
    log_agent_start("CODE ANALYSIS", state)
    
    # Store original state for comparison
    original_state = state.copy()
    
    messages = state["messages"]
    query = state["latest_user_message"]
    context = state.get("context", {})
    
    # Check for code
    has_code = detect_code_in_query(query)
    log_debug(f"Code detection result: {has_code}", level=LOG_LEVEL_INFO)
    
    if not has_code:
        log_debug("No code detected in query, skipping AST analysis", level=LOG_LEVEL_INFO)
        # Log agent end (no changes)
        log_agent_end("CODE ANALYSIS", original_state, state)
        return state
    
    log_debug("Code detected, performing AST analysis", level=LOG_LEVEL_INFO)
    
    try:
        # Extract all code blocks (updated to handle multiple blocks)
        code_blocks = extract_code_blocks(query)
        log_debug(f"Extracted {len(code_blocks)} code blocks", level=LOG_LEVEL_DEBUG)
        
        # For each code block, log a preview (first 5 lines)
        for i, block in enumerate(code_blocks):
            lines = block.split('\n')[:5]
            preview = '\n'.join(lines)
            if len(lines) < len(block.split('\n')):
                preview += "\n..."
            log_debug(f"Code block {i+1} preview:", level=LOG_LEVEL_DEBUG, data=preview)
        
        # Get configuration from dependencies
        deps = get_ai_dependencies()
        
        # Analyze code blocks with centralized max_code_length from dependencies
        analysis_results, full_code = analyze_code_blocks(code_blocks, max_code_length=deps.max_code_length)
        
        # Log analysis success/failure
        if analysis_results:
            # Format for logging
            analysis_summary = format_code_analysis(analysis_results)
            log_debug("AST analysis results:", level=LOG_LEVEL_DEBUG, data=analysis_summary)
            
            # Create structured code summary with content analysis
            code_summary = create_code_summary(analysis_results, full_code)
            
            # Log summary statistics
            log_debug(
                f"Created structured code summary with {code_summary['function_count']} functions", 
                level=LOG_LEVEL_INFO
            )
            
            # Format for state
            summary = format_analysis_results(analysis_results)
            
            # Create analysis message
            analysis_message = create_analysis_message(summary)
            
            # Update context with analysis results and structured summary
            context["code_analysis"] = analysis_results
            context["full_code"] = full_code
            context["code_summary"] = code_summary
            
            # Count functions found
            function_count = code_summary["function_count"]
            log_debug(f"AST analysis complete, found {function_count} functions across {len(analysis_results)} code blocks", level=LOG_LEVEL_INFO)
            
            # Create updated state
            new_state = {
                "messages": messages + [analysis_message],
                "latest_user_message": query,
                "context": context
            }
            
            # Log agent end
            log_agent_end("CODE ANALYSIS", original_state, new_state)
            
            return new_state
        else:
            log_debug("No functions found in detected code", level=LOG_LEVEL_INFO)
            # Log agent end (no changes)
            log_agent_end("CODE ANALYSIS", original_state, state)
            return state
            
    except Exception as e:
        log_debug(f"Error during AST analysis: {str(e)}", level=LOG_LEVEL_ERROR)
        # Log agent end (no changes due to error)
        log_agent_end("CODE ANALYSIS", original_state, state)
        return state