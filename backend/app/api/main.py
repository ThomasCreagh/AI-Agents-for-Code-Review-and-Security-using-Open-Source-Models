from fastapi import APIRouter

from app.api.routes import (
    code_review,
    database,
    documents,
    graph,
    ast_analysis
)

api_router = APIRouter()


@api_router.get("/")
def read_root():
    return {"Hello": "World"}


api_router.include_router(code_review.router)
api_router.include_router(database.router)
api_router.include_router(documents.router)
api_router.include_router(graph.router)
api_router.include_router(ast_analysis.router)
