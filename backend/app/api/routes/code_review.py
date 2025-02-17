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


@router.post(
    "/file",
    response_model=CodeReviewResponse,
    dependencies=[Depends(verify_api_key)],
)
async def review_code_file(
        code_files: List[UploadFile] = File(None),
        documentation_files: List[UploadFile] = File(None),
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
    if documentation_files:
        for documentation_file in documentation_files:
            names.append(documentation_file.filename)
            suggestion += str(convert_bytes_to_docling(
                documentation_file.filename,
                documentation_file.file.read()).model_dump())
    name = str(names)
    return CodeReviewResponse(
        filename=name,
        language=language,
        error_description=error_description,
        suggestion=suggestion,
    )
