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
        code_blocks = re.findall(r'```python\n(.*?)\n```', query, re.DOTALL)
        
        if not code_blocks:
            code_blocks = re.findall(r'```\n(.*?)\n```', query, re.DOTALL)
            
        if not code_blocks:
            potential_code = query
            code_blocks = [potential_code]
        
        analysis_results = []
        full_code = []  
        
        for code in code_blocks:
            full_code.append(code)
            analysis = analyze_python_code(code)
            if analysis:
                analysis_results.append(analysis)
        
        if analysis_results:
            summary = "# Code Analysis Results\n\n"
            
            summary += "## Code Purpose Analysis\n\n"
            
            has_http = any("http" in code or "request" in code or "api" in code for code in full_code)
            has_file_ops = any("open(" in code or "file" in code or "read" in code or "write" in code for code in full_code)
            has_db = any("database" in code or "sql" in code or "query" in code for code in full_code)
            has_auth = any("auth" in code or "password" in code or "login" in code or "token" in code for code in full_code)
            
            if has_http:
                summary += "- Code includes HTTP/API operations that may handle external input\n"
            if has_file_ops:
                summary += "- Code performs file operations that may involve sensitive data\n"
            if has_db:
                summary += "- Code interacts with databases which may require injection protection\n"
            if has_auth:
                summary += "- Code appears to handle authentication or sensitive credentials\n"
            
            summary += "\n## Detected Functions\n\n"
            
            for idx, result in enumerate(analysis_results):
                summary += f"### Code Block {idx+1}\n\n"
                if not result:
                    summary += "No functions detected in this code block.\n\n"
                    continue
                    
                for func_name, details in result.items():
                    summary += f"Function: `{func_name}`\n"
                    summary += f"Parameters: `{', '.join(details['params'])}`\n"
                    
                    for param in details['params']:
                        param_lower = param.lower()
                        if any(word in param_lower for word in ["user", "input", "data", "request", "file", "path"]):
                            summary += f"⚠️ Parameter `{param}` may accept user input and should be validated\n"
                            
                    if details['returns']:
                        returns_str = ", ".join([f"{r.get('value', 'unknown')} ({r.get('type', 'unknown')})" 
                                              for r in details['returns']])
                        summary += f"Returns: {returns_str}\n"
                    summary += "\n"
            
            code_content = "## Full Code:\n\n"
            for idx, code_block in enumerate(full_code):
                code_content += f"### Block {idx+1}:\n```python\n{code_block}\n```\n\n"
            
            summary += code_content
            
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