from fastapi import APIRouter, File, UploadFile, Form
from git_analyser import print_hello_world

from app.models import (
    CodeSourceType,
    CodeReviewRequest,
    CodeReviewResponse
)

router = APIRouter(prefix="/code-review", tags=["code-review"])


@router.post("/text", response_model=CodeReviewResponse)
def review_code_text(request: CodeReviewRequest) -> CodeReviewResponse:
    print_hello_world.run()
    return CodeReviewResponse(
        code_source_type=CodeSourceType.text,
        language=request.language,
        error_description=request.error_description,
        filename=None,
        suggestion="test",
    )


@router.post("/file", response_model=CodeReviewResponse)
async def review_code_file(
        file: UploadFile = File(...),
        error_description: str | None = Form(None),
        language: str = Form(...),
) -> CodeReviewResponse:
    return CodeReviewResponse(
        code_source_type=CodeSourceType.file,
        filename=file.filename,
        language=language,
        error_description=error_description,
        suggestion="test",
    )
