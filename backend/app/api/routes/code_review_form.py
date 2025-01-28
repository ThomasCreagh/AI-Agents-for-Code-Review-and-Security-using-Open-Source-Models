from fastapi import APIRouter
from app.models import CodeReviewForm

router = APIRouter(prefix="/code-review-form", tags=["code-review-form"])


@router.post("/")
def read_item(code_review_form: CodeReviewForm):
    return {"code": code_review_form}
