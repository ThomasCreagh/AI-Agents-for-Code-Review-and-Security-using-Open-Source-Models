from pydantic import BaseModel
from typing import Union


class TestOuput(BaseModel):
    returned_message: str
    input_value: dict


class CodeReviewForm(BaseModel):
    programming_language: str
    raw_code: str
    error: Union[str, None] = None
