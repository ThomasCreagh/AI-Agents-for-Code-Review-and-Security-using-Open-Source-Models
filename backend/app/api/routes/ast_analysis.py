from fastapi import APIRouter, File, UploadFile, Form, Depends, Body
from typing import List, Optional
import json

from app.ai.code_analysis.ast_analyser import analyze_python_code
from app.core.security import verify_api_key
from app.ai.agent.base_agent import BaseAgent
from app.dependencies import get_agent, get_db_manager
from app.ai.database.database_manager import DatabaseManager

router = APIRouter(prefix="/ast-analysis", tags=["ast-analysis"])


@router.post("/analyze", dependencies=[Depends(verify_api_key)])
async def analyze_code(
    code_files: List[UploadFile] = File(...),
    language: str = Form(default="python"),
):
    results = {}
    
    for file in code_files:
        try:
            content = await file.read()
            file_content = content.decode("utf-8")
            
            if language.lower() == "python":
                analysis = analyze_python_code(file_content)
                results[file.filename] = analysis
            else:
                results[file.filename] = {"error": f"Language {language} not supported yet"}
                
        except Exception as e:
            results[file.filename] = {"error": str(e)}
        
        await file.seek(0)
    
    return {"analysis_results": results}


@router.post("/analyze-with-agent", dependencies=[Depends(verify_api_key)])
async def analyze_code_with_agent(
    code_files: List[UploadFile] = File(...),
    language: str = Form(default="python"),
    agent: BaseAgent = Depends(get_agent),
):
    analysis_results = {}
    prompt_text = f"LANGUAGE: {language}\n\n"
    
    for file in code_files:
        try:
            content = await file.read()
            file_content = content.decode("utf-8")
            
            if language.lower() == "python":
                analysis = analyze_python_code(file_content)
                analysis_results[file.filename] = analysis
                prompt_text += f"FILE: {file.filename}\n{file_content}\n\n"
            else:
                analysis_results[file.filename] = {"error": f"Language {language} not supported yet"}
                
        except Exception as e:
            analysis_results[file.filename] = {"error": str(e)}
        
        await file.seek(0)
    
    agent_response = agent.process_message(prompt_text)
    
    return {
        "analysis_results": analysis_results,
        "agent_response": agent_response
    }


@router.post("/analyze-snippet", dependencies=[Depends(verify_api_key)])
async def analyze_code_snippet(
    code: str = Body(..., description="Python code to analyze"),
    question: Optional[str] = Body(None, description="Specific question about the code"),
    language: str = Body("python", description="Programming language of the code"),
    agent: BaseAgent = Depends(get_agent),
):
    prompt = ""
    
    if question:
        prompt += f"{question}\n\n"
    
    prompt += f"```{language}\n{code}\n```\n\n"
    prompt += "Please analyze this code for security vulnerabilities and best practices."
    
    response = agent.process_message(prompt)
    
    return {
        "question": question or "General code analysis",
        "code_length": len(code),
        "language": language,
        "response": response
    }


@router.post("/submit-code-for-review", dependencies=[Depends(verify_api_key)])
async def submit_code_for_review(
    code_file: UploadFile = File(..., description="Code file to analyze"),
    security_context: Optional[str] = Body(None, description="Additional security context or requirements"),
    language: str = Body("python", description="Programming language of the code"),
    reference_docs: Optional[str] = Body(None, description="Whether to reference available documents in the database for analysis"),
    agent: BaseAgent = Depends(get_agent),
    db_manager: DatabaseManager = Depends(get_db_manager),
):
    """
    Submit code for security review. This endpoint assumes documents are already uploaded
    to the database using the /documents/upload endpoint.
    """
    # Read the code from the file
    try:
        content = await code_file.read()
        code = content.decode("utf-8")
        await code_file.seek(0)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error reading code file: {str(e)}"
        }
    
    # Check if we have documents in the database to reference
    try:
        db_stats = db_manager.get_stats()
        doc_count = db_stats.get("total_documents", 0)
        
        if reference_docs and reference_docs.lower() == "true" and doc_count == 0:
            return {
                "status": "error",
                "message": "You requested to reference documents, but no documents are available in the database. Please upload documents first using the /documents/upload endpoint."
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error checking database statistics: {str(e)}"
        }
    
    # Setup the agent's prompt with code and security context
    prompt = "Please review this code for security issues"
    
    if security_context:
        prompt += f" with a focus on: {security_context}"
    
    prompt += f"\n\n```{language}\n{code}\n```"
    
    # If reference_docs is true, explicitly instruct the agent to use the security documentation
    if reference_docs and reference_docs.lower() == "true":
        prompt += "\n\nIMPORTANT: You MUST check this code against the security documentation in the knowledge base. "
        prompt += "Look for ANY violations of security standards and explicitly mention them in your analysis. "
        prompt += "If the code violates any security standards or best practices described in the documentation, "
        prompt += "identify each violation specifically and explain why it violates the standard."
    
    # Process with the agent
    response = agent.process_message(prompt)
    
    return {
        "response": response,
        "database_stats": db_stats if reference_docs else None
    }