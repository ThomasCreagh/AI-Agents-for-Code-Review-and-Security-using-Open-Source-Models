from fastapi import APIRouter

from app.api.routes import review_code

api_router = APIRouter()


@api_router.get("/")
def read_root():
    return {"Hello": "World"}


api_router.include_router(review_code.router)
