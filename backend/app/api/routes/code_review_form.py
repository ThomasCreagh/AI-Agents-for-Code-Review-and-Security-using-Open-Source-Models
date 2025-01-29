from fastapi import APIRouter, File, UploadFile, Depends, Form

from app.models import (
    CodeReviewFormTextBox,
    CodeReviewForm,
    TestOuput,
)

router = APIRouter(prefix="/code-review-form", tags=["code-review-form"])


@router.post("/text-box")
def read_text_box(
        code_review_form_textbox: CodeReviewFormTextBox
) -> dict:
    return TestOuput(
        returned_message="got the text correctly",
        input_value=code_review_form_textbox.model_dump()
    ).model_dump()


@router.post("/file-upload")
async def read_file(
        programming_language: str = Form(...),
        error: str | None = Form(None),
        # code_review_form: CodeReviewForm,
        file: UploadFile = File(...),
) -> dict:
    return TestOuput(
        returned_message="got the file correctly",
        input_value={
            "programming_language": programming_language,
            "error": error,
            "filename": file.filename,
            "content_type": file.content_type
        }
        # input_value={"form": code_review_form.model_dump(),
        #              "filename": file.filename,
        #              "content_type": file.content_type}
    ).model_dump()
