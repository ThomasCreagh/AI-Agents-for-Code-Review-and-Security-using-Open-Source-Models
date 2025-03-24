from pydantic import BaseModel
from langchain_core.messages import BaseMessage
from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict):
    messages: List[BaseMessage]  # All conversation messages
    latest_user_message: str     # The most recent user message
    context: Dict[str, Any]      # Holds retrieved context and other data


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    response: str


class DocumentLoadRequest(BaseModel):
    directory_path: str="app/data"


class CodeReviewResponse(BaseModel):
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
