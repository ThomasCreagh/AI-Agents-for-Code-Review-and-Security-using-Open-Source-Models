from fastapi import APIRouter, File, UploadFile, Form, Depends
from typing import List

from app.docling.processor import convert_bytes_to_docling
from app.ai.security_scanner.plugins.credential_scanner import (
    scan_text, load_patterns
)
from app.core.security import verify_api_key
from app.models import (
    CodeReviewRequest,
    CodeReviewResponse
)

router = APIRouter(prefix="/code-review", tags=["code-review"])


def add_to_suggestion_temp(
        file_list: List[str],
        names: List[str],
        suggestion: str
) -> (str, List[str]):
    if not file_list:
        return (suggestion, names)
    for file in file_list:
        names.append(file.filename)
        suggestion += str(convert_bytes_to_docling(
            file.filename,
            file.file.read()).model_dump())
    return (suggestion, names)


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

# api-documentation
# security-documentation
# library-dependency
# code-documentation
# version-control


@router.post(
    "/file",
    response_model=CodeReviewResponse,
    dependencies=[Depends(verify_api_key)],
)
async def review_code_file(
        code_files: List[UploadFile] = File(None),
        api_documentation: List[UploadFile] = File(None),
        security_documentation: List[UploadFile] = File(None),
        library_dependency: List[UploadFile] = File(None),
        code_documentation: List[UploadFile] = File(None),
        version_control: List[UploadFile] = File(None),
        model: str | None = Form(None),
        error_description: str | None = Form(None),
        language: str = Form(None),
) -> CodeReviewResponse:
    names = []
    suggestion = ""
    if code_files:
        for code_file in code_files:
            names.append(code_file.filename)
            suggestion += str(scan_text(str(code_file.file.read()),
                              load_patterns(), code_file.filename))
    suggestion, names = add_to_suggestion_temp(
        api_documentation, names, suggestion)
    suggestion, names = add_to_suggestion_temp(
        security_documentation, names, suggestion)
    suggestion, names = add_to_suggestion_temp(
        library_dependency, names, suggestion)
    suggestion, names = add_to_suggestion_temp(
        code_documentation, names, suggestion)
    suggestion, names = add_to_suggestion_temp(
        version_control, names, suggestion)
    name = str(names)
    return CodeReviewResponse(
        filename=name,
        language=language,
        error_description=error_description,
        suggestion=suggestion,
    )
