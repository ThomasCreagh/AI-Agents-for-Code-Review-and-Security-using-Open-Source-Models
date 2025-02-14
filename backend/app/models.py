from pydantic import BaseModel


class CodeReviewResponse(BaseModel):
    filename: str | None = None
    error_description: str | None = None
    language: str
    suggestion: str


class CodeReviewRequest(BaseModel):
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
