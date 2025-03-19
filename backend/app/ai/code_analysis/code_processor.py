from langchain_core.documents import Document
from datetime import datetime
from app.ai.code_analysis.ast_analyser import analyze_python_code
import json

def process_code_for_storage(code: str, filename: str, language: str) -> Document:
    """Process code using AST analysis and prepare it for vector store storage."""
    analysis_results = analyze_python_code(code)
    
    summary = f"Code Analysis for {filename}\n\n"
    for func_name, details in analysis_results.items():
        summary += f"Function: {func_name}\n"
        summary += f"Parameters: {', '.join(details['params'])}\n"
        if details['returns']:
            summary += f"Returns: {json.dumps(details['returns'], indent=2)}\n"
        summary += "\n"

    return Document(
        page_content=summary,
        metadata={
            "type": "code_analysis",
            "filename": filename,
            "language": language,
            "timestamp": datetime.now().isoformat(),
            "raw_analysis": analysis_results
        }
    )