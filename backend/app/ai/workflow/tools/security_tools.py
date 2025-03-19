from typing import List, Dict, Any
from app.ai.workflow.utils import log_debug
from app.ai.dependencies import get_ai_dependencies

def format_document_sources(doc_sources: List[Dict]) -> List[str]:
    if not doc_sources:
        return []
        
    source_names = []
    for src in doc_sources:
        if isinstance(src, dict):
            source_names.append(src.get('source', 'unknown'))
        else:
            source_names.append(src)
    
    log_debug(f"Security analysis using documents from: {', '.join(source_names)}")
    return source_names

def create_security_prompt(has_code_analysis: bool) -> str:
    deps = get_ai_dependencies()
    
    security_prompt_content = """
    Identify security vulnerabilities and provide assessment. Use citation markers ([1], [2]) 
    when referencing documents. Be concise.
    """
    
    focus_areas = ", ".join(deps.security_focus_areas)
    security_prompt_content += f"""
    Focus your analysis on these security areas: {focus_areas}.
    """
    
    if has_code_analysis:
        security_prompt_content += """
        Check code for: user input validation, sensitive data exposure, and security vulnerabilities.
        """
        
        sensitive_params = ", ".join(deps.sensitive_param_patterns)
        security_prompt_content += f"""
        Pay special attention to parameters that might handle sensitive data: {sensitive_params}.
        """
    
    return security_prompt_content

def create_final_response_prompt() -> str:
    deps = get_ai_dependencies()
    
    prompt = """
    Answer the security question concisely. Use references when referencing documents.
    End with ## Sources listing referenced documents.
    """
    
    # Add focus areas from dependencies
    focus_areas = ", ".join(deps.security_focus_areas)
    prompt += f"""
    Ensure your response addresses these key security areas if relevant: {focus_areas}.
    """
    
    return prompt