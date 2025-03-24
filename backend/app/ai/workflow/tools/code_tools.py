import re
from typing import List, Dict, Any, Tuple
from app.ai.workflow.utils import log_debug
from app.ai.code_analysis.ast_analyser import analyze_python_code
from app.ai.dependencies import AIDependencies, get_ai_dependencies

def extract_code_blocks(query: str) -> List[str]:
    code_blocks = re.findall(r'```python\n(.*?)\n```', query, re.DOTALL)
    
    if not code_blocks:
        code_blocks = re.findall(r'```\n(.*?)\n```', query, re.DOTALL)
        
    if not code_blocks:
        potential_code = query[:1000] if len(query) > 1000 else query
        code_blocks = [potential_code]
    else:
        code_blocks = [code_blocks[0]] 
    
    return code_blocks

def detect_code_in_query(query: str) -> bool:
    code_indicators = ["def ", "class ", "import ", "```python", "from "]
    return any(indicator in query for indicator in code_indicators)

def analyze_code_blocks(code_blocks: List[str], max_code_length: int = None) -> Tuple[List[Dict], List[str]]:
    deps = get_ai_dependencies()
    if max_code_length is None:
        max_code_length = deps.max_code_length
    
    analysis_results = []
    full_code = []
    
    for code in code_blocks:
        if len(code) > max_code_length:
            code = code[:max_code_length]
            
        full_code.append(code)
        analysis = analyze_python_code(code)
        if analysis:
            analysis_results.append(analysis)
    
    return analysis_results, full_code

def format_analysis_results(analysis_results: List[Dict]) -> str:
    deps = get_ai_dependencies()
    if not analysis_results:
        return ""
        
    summary = "Code Analysis:\n"
    
    function_count = 0
    for idx, result in enumerate(analysis_results):
        if not result:
            continue
            
        for func_name, details in result.items():
            if function_count >= deps.max_functions:  # Use max_functions from dependencies
                break
                
            function_count += 1
            summary += f"- {func_name}({', '.join(details['params'][:3])})\n"
            
            for param in details['params'][:3]:
                param_lower = param.lower()
                if any(word in param_lower for word in deps.sensitive_param_patterns):
                    summary += f" Parameter `{param}` may accept sensitive data\n"
    
    return summary