from langchain_core.messages import SystemMessage
from app.models import AgentState
import re

def code_analysis_agent(state: AgentState):
    from app.ai.code_analysis.ast_analyser import analyze_python_code
    from app.ai.workflow.graph_config import log_debug
    
    messages = state["messages"]
    query = state["latest_user_message"]
    context = state.get("context", {})
    
    log_debug(f"Checking for code in query for AST analysis")
    
    code_indicators = ["def ", "class ", "import ", "```python", "from "]
    contains_code = any(indicator in query for indicator in code_indicators)
    
    if not contains_code:
        log_debug("No code detected in query, skipping AST analysis")
        return state
    
    log_debug("Code detected, performing AST analysis")
    
    try:
        # Extract only the first code block to analyze
        code_blocks = re.findall(r'```python\n(.*?)\n```', query, re.DOTALL)
        
        if not code_blocks:
            code_blocks = re.findall(r'```\n(.*?)\n```', query, re.DOTALL)
            
        if not code_blocks:
            # Take only first 1000 chars as potential code
            potential_code = query[:1000] if len(query) > 1000 else query
            code_blocks = [potential_code]
        else:
            # Only analyze first code block
            code_blocks = [code_blocks[0]]
        
        analysis_results = []
        full_code = []  
        
        for code in code_blocks:
            # Truncate very large code blocks
            if len(code) > 2000:
                code = code[:2000]
                
            full_code.append(code)
            analysis = analyze_python_code(code)
            if analysis:
                analysis_results.append(analysis)
        
        if analysis_results:
            #Use minimal summary format
            summary = "Code Analysis:\n"
            
            # Skip detailed code purpose analysis
            
            # Only include critical function data
            function_count = 0
            for idx, result in enumerate(analysis_results):
                if not result:
                    continue
                    
                for func_name, details in result.items():
                    if function_count >= 5:  # Limit to 5 functions
                        break
                        
                    function_count += 1
                    summary += f"- {func_name}({', '.join(details['params'][:3])})\n"
                    
                    # Only check first 3 params
                    for param in details['params'][:3]:
                        param_lower = param.lower()
                        if any(word in param_lower for word in ["user", "input", "data", "request", "file", "path"]):
                            summary += f"  ⚠️ Parameter `{param}` may accept user input\n"
            
            # Skip including full code in summary
            
            analysis_message = SystemMessage(
                content=summary
            )
            
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