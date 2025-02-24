from fastapi import APIRouter, File, UploadFile, Form, Depends
from typing import List

# from app.ai.security_scanner.plugins.credential_scanner import (
#     scan_text, load_patterns
# )
from app.ai.agent.base_agent import BaseAgent
from app.dependencies import get_agent
from app.core.security import verify_api_key
from app.models import (
    # CodeReviewRequest,
    CodeReviewResponse
)

router = APIRouter(prefix="/code-review", tags=["code-review"])


def compile_code_to_str(
        file_list: List[str],
        names: List[str],
        full_text: str,
        language: str,
        error_description: str
) -> (str, List[str]):
    full_text += f"LANGUAGE: {language}\n"
    full_text += f"ERROR DESCRIPTION: {error_description}\n\n"
    if not file_list:
        return (full_text, names)
    for file in file_list:
        names.append(file.filename)
        full_text += f"FILE:{file.filename}:\n"
        full_text += f"{str(file.file.read())}\n\n"
    return (full_text, names)


@router.post(
    "/file",
    response_model=CodeReviewResponse,
    dependencies=[Depends(verify_api_key)],
)
def review_code_file(
        code_files: List[UploadFile] = File(...),
        model: str | None = Form(None),
        error_description: str | None = Form(None),
        language: str = Form(None),
        agent: BaseAgent = Depends(get_agent),
) -> CodeReviewResponse:
    names = []
    suggestion = ""
    prompt = ""
    if code_files:
        prompt, names = compile_code_to_str(
            code_files, names, prompt, language, error_description)

    print("PROCESS QUERY...")
    suggestion = agent.process_message(prompt)

    return CodeReviewResponse(
        suggestion=suggestion
    )
