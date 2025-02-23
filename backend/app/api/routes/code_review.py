from fastapi import APIRouter, File, UploadFile, Form, Depends
from typing import List

# from app.ai.security_scanner.plugins.credential_scanner import (
#     scan_text, load_patterns
# )
from app.core.security import verify_api_key
from app.models import (
    CodeReviewRequest,
    CodeReviewResponse
)

router = APIRouter(prefix="/code-review", tags=["code-review"])

#
# @router.post(
#     "/text",
#     response_model=CodeReviewResponse,
#     dependencies=[Depends(verify_api_key)],
# )
# def review_code_text(request: CodeReviewRequest) -> CodeReviewResponse:
#     suggestion = str(scan_text(request.code, load_patterns()))
#     return CodeReviewResponse(
#         language=request.language,
#         error_description=request.error_description,
#         filename=None,
#         suggestion=suggestion,
#         line_nums=[1, 5]  # placeholder
#     )
#
#
# @router.post(
#     "/file",
#     response_model=CodeReviewResponse,
#     dependencies=[Depends(verify_api_key)],
# )
# async def review_code_file(
#         code_files: List[UploadFile] = File(...),
#         api_documentation: List[UploadFile] = File(None),
#         security_documentation: List[UploadFile] = File(None),
#         library_dependency: List[UploadFile] = File(None),
#         code_documentation: List[UploadFile] = File(None),
#         model: str | None = Form(None),
#         error_description: str | None = Form(None),
#         language: str = Form(None),
#         ai_agent: RunModel = Depends(get_agent),
#         db: RunModel = Depends(get_db),
# ) -> CodeReviewResponse:
#     print("doing stuff")
#     names = []
#     suggestion = ""
#     prompt = ""
#     if code_files:
#         prompt, names = compile_code_to_str(
#             code_files, names, prompt, language, error_description)
#
#     if api_documentation:
#         for documentation_file in api_documentation:
#             add_bytes_to_rag_db(documentation_file.filename,
#                                 documentation_file.file.read(),
#                                 db)
#
#     if security_documentation:
#         for documentation_file in security_documentation:
#             add_bytes_to_rag_db(documentation_file.filename,
#                                 documentation_file.file.read(),
#                                 db)
#
#     if library_dependency:
#         for documentation_file in library_dependency:
#             add_bytes_to_rag_db(documentation_file.filename,
#                                 documentation_file.file.read(),
#                                 db)
#
#     if code_documentation:
#         for documentation_file in code_documentation:
#             add_bytes_to_rag_db(documentation_file.filename,
#                                 documentation_file.file.read(),
#                                 db)
#
#     print("RAG REASONER...")
#     suggestion = ai_agent.run_rag(prompt)
#
#     return CodeReviewResponse(
#         suggestion=suggestion
#     )
