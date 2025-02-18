from fastapi import APIRouter

from app.api.routes import code_review

api_router = APIRouter()


@api_router.get("/")
def read_root():
    # print("LAUNCH??")
    # launch.main()
    return {"Hello": "World"}


api_router.include_router(code_review.router)
