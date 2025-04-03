from typing import List, Dict, Any
from app.ai.workflow.utils import log_debug, LOG_LEVEL_INFO, LOG_LEVEL_DEBUG
from app.ai.dependencies import get_ai_dependencies

def format_document_sources(doc_sources: List[Dict]) -> List[str]:
    """
    Format document sources for security analysis.
    """
    if not doc_sources:
        return []
        
    source_names = []
    for src in doc_sources:
        if isinstance(src, dict):
            source_names.append(src.get('source', 'unknown'))
        else:
            source_names.append(src)
    
    log_debug(f"Security analysis using documents from: {', '.join(source_names)}", level=LOG_LEVEL_INFO)
    return source_names

def create_security_prompt(has_code_analysis: bool, code_summary: Dict = None) -> str:
    """
    Create a structured prompt for security analysis based on available information.
    
    Args:
        has_code_analysis: Whether code analysis is available
        code_summary: Structured code summary if available
    
    Returns:
        Security prompt content
    """
    deps = get_ai_dependencies()
    
    security_prompt_content = """
    Analyze the code for security vulnerabilities and provide a structured assessment.
    
    Structure your analysis into these sections:
    1. SUMMARY: Brief overview of critical security issues
    2. GENERAL CONCERNS: Security issues affecting the entire codebase
    3. FUNCTION-SPECIFIC VULNERABILITIES: Analysis by individual function
    4. RECOMMENDED FIXES: Specific remediation steps
    
    Use citation markers ([1], [2]) when referencing documents. 
    IMPORTANT: Only cite sources that are explicitly provided in the context. Do not reference external security standards that were not provided.
    """
    
    # Limit to 3 focus areas to reduce token usage
    focus_areas = ", ".join(deps.security_focus_areas[:3])
    security_prompt_content += f"""
    Focus your analysis on these security areas: {focus_areas}.
    """
    
    if has_code_analysis:
        security_prompt_content += """
        For each function, identify concrete vulnerabilities with specific code references.
        Explicitly name the vulnerable functions and parameters in your analysis.
        """
        
        # Add more specific security guidance if code_summary is available
        if code_summary:
            # Add all function names for targeted analysis - limit to 5 functions
            if code_summary.get('functions'):
                functions = code_summary.get('functions', [])
                function_list = ", ".join(functions[:5])  # Limit to first 5 if there are many
                security_prompt_content += f"""
                Analyze each of these functions for security issues: {function_list}
                """
            
            # Add information about sensitive functions - limit to 3
            if code_summary.get('sensitive_functions'):
                sensitive_funcs = code_summary.get('sensitive_functions', [])[:3]
                security_prompt_content += f"""
                Pay special attention to these functions that handle sensitive parameters: {', '.join(sensitive_funcs)}
                """
            
            # Limit security operations categories to 2
            op_count = 0
            for op_type, funcs in code_summary.get('security_operations', {}).items():
                if funcs and op_count < 2:
                    op_count += 1
                    op_name = op_type.replace("_", " ")
                    func_examples = ', '.join(funcs[:2])
                    security_prompt_content += f"""
                    Analyze {op_name} operations like {func_examples} for security weaknesses.
                    """
        else:
            # Use default sensitive parameters if no code_summary - limit to 5
            sensitive_params = ", ".join(deps.sensitive_param_patterns[:5])
            security_prompt_content += f"""
            Pay special attention to parameters that might handle sensitive data: {sensitive_params}
            """
    
    # Ensure the prompt doesn't exceed 1000 characters
    if len(security_prompt_content) > 1000:
        security_prompt_content = security_prompt_content[:1000]
    
    return security_prompt_content

def create_final_response_prompt() -> str:
    """
    Create a prompt for generating the final structured response.
    """
    deps = get_ai_dependencies()
    
    prompt = """
    Provide a comprehensive security analysis of the code with the following structure:
    
    # Security Analysis of the Provided Code
    
    ## Summary
    Brief overview of the most critical security issues found.
    
    ## General Concerns
    List overall security issues affecting the entire codebase.
    
    ## Function-Specific Vulnerabilities
    Organize vulnerabilities by function name, using specific code references.
    
    ## Recommended Fixes
    Provide specific remediation steps for each vulnerability identified.
    
    ## Sources
    List ONLY the documents provided in the context with their citation numbers.
    
    CRITICAL INSTRUCTION: Your analysis MUST be based solely on the security standards that were retrieved from the knowledge base and provided in the context. Do NOT reference or use any other security standards or documents. At the end of your response, include a Sources section that lists only the documents that were provided in the context with their citation numbers.
    
    If no documents were provided in the context, state "No specific security standards referenced."
    
    Example format:
    ## Sources
    [1] OWASP Application Security Verification Standard
    [2] NIST Special Publication 800-53
    """
    
    # Add focus areas from dependencies - limit to 3
    focus_areas = ", ".join(deps.security_focus_areas[:3])
    prompt += f"""
    Ensure your response addresses these key security areas when relevant: {focus_areas}.
    """
    
    # Limit prompt length to 1200 characters to accommodate the new instructions
    if len(prompt) > 1200:
        prompt = prompt[:1200]
    
    return prompt