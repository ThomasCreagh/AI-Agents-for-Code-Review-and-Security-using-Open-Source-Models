from fastapi import APIRouter, File, UploadFile, Form, Depends
from typing import List

from app.docling.processor import convert_bytes_to_docling, add_bytes_to_rag_db
from app.ai.security_scanner.plugins.credential_scanner import (
    scan_text, load_patterns
)
import app.ai.llm_rag_database.launch as launch
from app.core.security import verify_api_key
from app.models import (
    CodeReviewRequest,
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
    full_text += f"LANGUAGE: {language}"
    full_text += f"ERROR DESCRIPTION: {error_description}"
    if not file_list:
        return (full_text, names)
    for file in file_list:
        names.append(file.filename)
        full_text += f"FILE:{file.filename}:\n"
        full_text += f"{str(file.file.read())}\n\n"
    return (full_text, names)


@router.post(
    "/text",
    response_model=CodeReviewResponse,
    dependencies=[Depends(verify_api_key)],
)
def review_code_text(request: CodeReviewRequest) -> CodeReviewResponse:
    suggestion = str(scan_text(request.code, load_patterns()))
    return CodeReviewResponse(
        language=request.language,
        error_description=request.error_description,
        filename=None,
        suggestion=suggestion,
    )

# api_documentation
# security_documentation
# library_dependency
# code_documentation
# version_control?

# async def review_code_file(
#         code_files: List[UploadFile] = File(None),
#         api_documentation: List[UploadFile] = File(None),
#         security_documentation: List[UploadFile] = File(None),
#         library_dependency: List[UploadFile] = File(None),
#         code_documentation: List[UploadFile] = File(None),
#         version_control: List[UploadFile] = File(None),
#         model: str | None = Form(None),
#         error_description: str | None = Form(None),
#         language: str = Form(None),
# ) -> CodeReviewResponse:


@router.post(
    "/file",
    response_model=CodeReviewResponse,
    dependencies=[Depends(verify_api_key)],
)
async def review_code_file(
        code_files: List[UploadFile] = File(...),
        api_documentation: List[UploadFile] = File(None),
        security_documentation: List[UploadFile] = File(None),
        library_dependency: List[UploadFile] = File(None),
        code_documentation: List[UploadFile] = File(None),
        model: str | None = Form(None),
        error_description: str | None = Form(None),
        language: str = Form(None),
) -> CodeReviewResponse:
    names = []
    suggestion = ""
    prompt = ""
    if code_files:
        prompt, names = compile_code_to_str(
            code_files, names, prompt, language, error_description)

    if api_documentation:
        for documentation_file in api_documentation:
            add_bytes_to_rag_db(documentation_file.filename,
                                documentation_file.file.read())

    if security_documentation:
        for documentation_file in security_documentation:
            add_bytes_to_rag_db(documentation_file.filename,
                                documentation_file.file.read())

    if library_dependency:
        for documentation_file in library_dependency:
            add_bytes_to_rag_db(documentation_file.filename,
                                documentation_file.file.read())

    if code_documentation:
        for documentation_file in code_documentation:
            add_bytes_to_rag_db(documentation_file.filename,
                                documentation_file.file.read())

    print("RAG REASONER...")
    suggestion = launch.rag_with_reasoner(prompt)

    return CodeReviewResponse(
        suggestion=suggestion
    )
