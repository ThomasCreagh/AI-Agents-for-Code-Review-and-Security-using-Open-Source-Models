from langchain_core.messages import SystemMessage
from app.models import AgentState
from app.ai.workflow.utils import log_debug
from app.ai.workflow.tools.code_tools import detect_code_in_query, extract_code_blocks, analyze_code_blocks, format_analysis_results
from app.ai.workflow.tools.message_tools import create_analysis_message

def code_analysis_agent(state: AgentState):
    messages = state["messages"]
    query = state["latest_user_message"]
    context = state.get("context", {})
    
    log_debug(f"Checking for code in query for AST analysis")
    
    if not detect_code_in_query(query):
        log_debug("No code detected in query, skipping AST analysis")
        return state
    
    log_debug("Code detected, performing AST analysis")
    
    try:
        code_blocks = extract_code_blocks(query)
        
        analysis_results, full_code = analyze_code_blocks(code_blocks)
        
        if analysis_results:
            summary = format_analysis_results(analysis_results)
            
            analysis_message = create_analysis_message(summary)
            
            context["code_analysis"] = analysis_results
            context["full_code"] = full_code
            
            log_debug(f"AST analysis complete, found {len(analysis_results)} code blocks with functions")
            
            return {
                "messages": messages + [analysis_message],
                "latest_user_message": query,
                "context": context
            }
        else:
            log_debug("No functions found in detected code")
            return state
            
    except Exception as e:
        log_debug(f"Error during AST analysis: {str(e)}")
        return state