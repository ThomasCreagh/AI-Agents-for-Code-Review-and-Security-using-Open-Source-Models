from pydantic import BaseModel


class TestOuput(BaseModel):
    returned_message: str
    input_value: dict


class CodeReviewForm(BaseModel):
    programming_language: str
    error: str | None = None


class CodeReviewFormTextBox(CodeReviewForm):
    raw_code: str
