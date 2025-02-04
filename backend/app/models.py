from pydantic import BaseModel
from enum import Enum


class CodeSourceType(str, Enum):
    file = "file"
    text = "text"


class CodeReviewResponse(BaseModel):
    code_source_type: CodeSourceType
    filename: str | None = None
    error_description: str | None = None
    language: str
    suggestion: str
    line_nums: list


class CodeReviewRequest(BaseModel):
    code_source_type: CodeSourceType
    code: str
    error_description: str | None = None
    language: str


class Login(BaseModel):
    email: str
    password: str


class Logout(BaseModel):
    response: str


class CreateAccount(BaseModel):
    email: str
    password: str
    uuid: str                   # Unique identifier for each account
