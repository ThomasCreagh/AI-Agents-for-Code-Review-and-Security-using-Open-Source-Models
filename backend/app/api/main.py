from fastapi import APIRouter

from app.api.routes import code_review_form

api_router = APIRouter()


@api_router.get("/")
def read_root():
    return {"Hello": "World"}


api_router.include_router(code_review_form.router)
