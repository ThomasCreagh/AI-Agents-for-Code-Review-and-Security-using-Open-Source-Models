from fastapi import APIRouter, File, UploadFile, Form, Depends
from typing import List

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
    name = None
    suggestion = ""
    if code_files:
        text = str(code_files[0].file.read())
        suggestion = str(
            scan_text(text, load_patterns(), code_files[0].filename))
        name = code_files[0].filename
    return CodeReviewResponse(
        filename=name,
        language=language,
        error_description=error_description,
        suggestion=suggestion,
    )
