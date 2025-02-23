from fastapi import APIRouter, File, UploadFile, Form, Depends

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
        line_nums=[1, 5]  # placeholder
    )


@router.post(
    "/file",
    response_model=CodeReviewResponse,
    dependencies=[Depends(verify_api_key)],
)
async def review_code_file(
        file: UploadFile = File(...),
        error_description: str | None = Form(None),
        language: str = Form(...),
) -> CodeReviewResponse:
    text = str(file.file.read())
    suggestion = str(scan_text(text, load_patterns(), file.filename))
    return CodeReviewResponse(
        filename=file.filename,
        language=language,
        error_description=error_description,
        suggestion=suggestion,
        line_nums=[1, 5]  # placeholder
    )
