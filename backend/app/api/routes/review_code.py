from fastapi import APIRouter, File, UploadFile, Form, Depends

from app.core.security import verify_api_key
from app.models import (
    CodeSourceType,
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
    return CodeReviewResponse(
        code_source_type=CodeSourceType.text,
        language=request.language,
        error_description=request.error_description,
        filename=None,
        suggestion="test",
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
    return CodeReviewResponse(
        code_source_type=CodeSourceType.file,
        filename=file.filename,
        language=language,
        error_description=error_description,
        suggestion="test",
        line_nums=[1, 5]  # placeholder
    )


# Note to Jake: you dont have a post request that tells you no security threat.
# Instead inside of the text uploads or the file upload endpoints you may
# return that there is no security threat there
@router.post(
    "/noSecurityThreat",
    response_model=CodeReviewResponse,
    dependencies=[Depends(verify_api_key)],
)
def no_vulnerabilities_found(
    file: UploadFile = File(...),
    error_description: str | None = Form(None),
    language: str = Form(...),
) -> CodeReviewResponse:
    return CodeReviewResponse(
        code_source_type=CodeSourceType.file,
        filename=file.filename,
        language=language,
        error_description=error_description,
        suggestion="No threat found",
        line_nums=[0, 0]     # nothing should be edited if no errors found
    )
