from pydantic import BaseModel
from typing import Union


class CodeReviewForm(BaseModel):
    programming_language: str
    raw_code: str
    error: Union[str, None] = None
