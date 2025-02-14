from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException

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


# TODO: check if i need "| None" for the documentation file
@router.post(
    "/file",
    response_model=CodeReviewResponse,
    dependencies=[Depends(verify_api_key)],
)
async def review_code_file(
        code_file: UploadFile = File(...),
        documentation_file: UploadFile = File(...),
        model: str | None = Form(None),
        error_description: str | None = Form(None),
        language: str = Form(...),
) -> CodeReviewResponse:
    if not code_file:
        raise HTTPException(
            status_code=400, detail="Invalid input: code file must be given")

    text = str(code_file.file.read())
    suggestion = str(scan_text(text, load_patterns(), code_file.filename))
    return CodeReviewResponse(
        filename=code_file.filename,
        language=language,
        error_description=error_description,
        suggestion=suggestion,
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
        filename=file.filename,
        language=language,
        error_description=error_description,
        suggestion="No threat found",
        line_nums=[0, 0]     # nothing should be edited if no errors found
    )
