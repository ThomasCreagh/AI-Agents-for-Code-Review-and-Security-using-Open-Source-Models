import re
from typing import List, Dict, Any, Tuple
from app.ai.workflow.utils import log_debug, LOG_LEVEL_DEBUG
from app.ai.code_analysis.ast_analyser import analyze_python_code
from app.ai.dependencies import AIDependencies, get_ai_dependencies

def extract_code_blocks(query: str) -> List[str]:
    """
    Extract all code blocks from a query or use the query itself if no blocks found.
    Returns all code blocks instead of just the first one.
    """
    # Look for Python code blocks
    code_blocks = re.findall(r'```python\n(.*?)\n```', query, re.DOTALL)
    
    # Look for generic code blocks if no Python blocks found
    if not code_blocks:
        code_blocks = re.findall(r'```\n(.*?)\n```', query, re.DOTALL)
    
    # If no code blocks found at all, use the whole query as a potential code block
    if not code_blocks:
        potential_code = query
        code_blocks = [potential_code]
    
    log_debug(f"Extracted {len(code_blocks)} code blocks", level=LOG_LEVEL_DEBUG)
    return code_blocks

def detect_code_in_query(query: str) -> bool:
    """
    Detect if a query likely contains code based on common indicators.
    """
    code_indicators = ["def ", "class ", "import ", "```python", "from "]
    return any(indicator in query for indicator in code_indicators)

def analyze_code_blocks(code_blocks: List[str], max_code_length: int = None) -> Tuple[List[Dict], List[str]]:
    """
    Analyze all code blocks using AST parser.
    Returns analysis results and the full code.
    """
    deps = get_ai_dependencies()
    if max_code_length is None:
        max_code_length = deps.max_code_length
    
    analysis_results = []
    full_code = []
    
    for code in code_blocks:
        # Store the full code (either the whole code or the maximum allowed length)
        if len(code) > max_code_length:
            log_debug(f"Code block truncated from {len(code)} to {max_code_length} characters", level=LOG_LEVEL_DEBUG)
            code = code[:max_code_length]
            
        full_code.append(code)
        analysis = analyze_python_code(code)
        if analysis:
            analysis_results.append(analysis)
    
    return analysis_results, full_code

def format_analysis_results(analysis_results: List[Dict]) -> str:
    """
    Format analysis results for human-readable output.
    """
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
            params = details['params'][:3] if len(details['params']) > 3 else details['params']
            summary += f"- {func_name}({', '.join(params)})\n"
            
            # Check for sensitive parameters
            for param in params:
                param_lower = param.lower()
                if any(word in param_lower for word in deps.sensitive_param_patterns):
                    summary += f"  Parameter `{param}` may accept sensitive data\n"
    
    return summary

# Extract imports from code
def extract_imports(code_blocks: List[str]) -> List[str]:
    """Extract import statements from code blocks."""
    imports = []
    
    for code in code_blocks:
        # Find import statements
        import_lines = re.findall(r'^(?:import|from)\s+([a-zA-Z0-9_.]+)', code, re.MULTILINE)
        imports.extend(import_lines)
    
    # Remove duplicates and return
    return list(set(imports))

# Extract classes from code
def extract_classes(code_blocks: List[str]) -> List[str]:
    """Extract class definitions from code blocks."""
    classes = []
    
    for code in code_blocks:
        # Find class definitions
        class_names = re.findall(r'class\s+([a-zA-Z0-9_]+)', code)
        classes.extend(class_names)
    
    # Remove duplicates and return
    return list(set(classes))

def create_code_summary(analysis_results: List[Dict], full_code: List[str]) -> Dict[str, Any]:
    """
    Create a structured summary of code analysis results.
    Focuses on structure and metrics rather than hardcoded pattern detection.
    
    Args:
        analysis_results: Results from analyze_code_blocks
        full_code: The full code blocks being analyzed
        
    Returns:
        A dictionary with structured code summary information
    """
    deps = get_ai_dependencies()
    
    # Calculate function statistics
    function_count = sum(len(analysis) for analysis in analysis_results if analysis)
    all_functions = []
    sensitive_functions = []
    
    for analysis in analysis_results:
        for func_name, details in analysis.items():
            all_functions.append(func_name)
            
            # Check if function has sensitive parameters
            has_sensitive_params = False
            for param in details.get('params', []):
                param_lower = param.lower()
                if any(word in param_lower for word in deps.sensitive_param_patterns):
                    has_sensitive_params = True
                    break
                    
            if has_sensitive_params:
                sensitive_functions.append(func_name)
    
    # Extract classes and imports
    classes = extract_classes(full_code)
    imports = extract_imports(full_code)
    
    # Basic structural information without hardcoded pattern detection
    security_operations = {
        "user_input": [],
        "file_operations": [],
        "database": [],
        "network": []
    }
    
    # Categorize functions based on name patterns (simplified approach)
    for analysis in analysis_results:
        for func_name, details in analysis.items():
            func_lower = func_name.lower()
            
            # Simple categorization based on function names
            if any(word in func_lower for word in ["input", "parse", "read", "get", "request", "form"]):
                security_operations["user_input"].append(func_name)
                
            if any(word in func_lower for word in ["file", "save", "load", "open", "read", "write"]):
                security_operations["file_operations"].append(func_name)
                
            if any(word in func_lower for word in ["sql", "query", "db", "database", "cursor"]):
                security_operations["database"].append(func_name)
                
            if any(word in func_lower for word in ["http", "request", "api", "url", "endpoint"]):
                security_operations["network"].append(func_name)
    
    # Create the summary with structural information only
    summary = {
        "function_count": function_count,
        "class_count": len(classes),
        "import_count": len(imports),
        "functions": all_functions,
        "classes": classes,
        "imports": imports,
        "sensitive_functions": sensitive_functions,
        "security_operations": security_operations,
        "line_count": sum(len(code.split('\n')) for code in full_code)
    }
    
    return summary