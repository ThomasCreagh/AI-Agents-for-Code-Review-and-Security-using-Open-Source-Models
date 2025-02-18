from fastapi import APIRouter

from app.api.routes import code_review
import app.ai.llm_rag_database.launch as launch

api_router = APIRouter()


@api_router.get("/")
def read_root():
    # print("LAUNCH??")
    # launch.main()
    print("RAG REASONER??")
    launch.rag_with_reasoner("documentation")
    return {"Hello": "World"}


api_router.include_router(code_review.router)
