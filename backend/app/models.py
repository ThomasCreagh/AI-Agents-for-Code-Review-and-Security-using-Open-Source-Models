from pydantic import BaseModel


class CodeReviewForm(BaseModel):
    programming_language: str
    raw_code: str
    error: str
