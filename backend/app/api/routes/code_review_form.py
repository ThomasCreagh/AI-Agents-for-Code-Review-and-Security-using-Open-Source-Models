from fastapi import APIRouter, File, UploadFile
from app.models import CodeReviewForm, TestOuput

router = APIRouter(prefix="/code-review-form", tags=["code-review-form"])


@router.post("/text-box")
def read_text_box(code_review_form: CodeReviewForm) -> dict:
    return TestOuput(
        returned_message="got the text correctly",
        input_value=code_review_form.model_dump()
    ).model_dump()


@router.post("/file-upload")
async def read_file(code_review_file: UploadFile = File(...)) -> dict:
    return TestOuput(
        returned_message="got the file correctly",
        input_value={"filename": code_review_file.filename,
                     "content_type": code_review_file.content_type}
    ).model_dump()
