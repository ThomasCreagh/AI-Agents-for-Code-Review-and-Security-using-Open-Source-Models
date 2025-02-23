from fastapi import HTTPException, APIRouter, Depends, UploadFile, File
from langchain_community.document_loaders import PyPDFLoader
import os
from tempfile import NamedTemporaryFile
import shutil

from app.ai.doc_loader.web_doc_loader import load_pdfs_from_directory
from app.ai.doc_loader.doc_chunker import process_and_store_documents
from app.models import DocumentLoadRequest
from app.dependancies import get_db_manager
from app.core.security import verify_api_key


router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/load", dependencies=[Depends(verify_api_key)])
def load_documents(
        request: DocumentLoadRequest,
        db_manager: Depends(get_db_manager)
):
    try:
        docs = load_pdfs_from_directory(request.directory_path)
        if not docs:
            return {"status": "error", "message": "No documents were found"}

        splits = process_and_store_documents(db_manager.vector_store, docs)

        return {
            "status": "success",
            "document_count": len(docs),
            "chunk_count": len(splits)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload", dependencies=[Depends(verify_api_key)])
def upload_document(
        db_manager: Depends(get_db_manager),
        file: UploadFile = File(...)
):
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400, detail="Only PDF files are supported")

        with NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        try:
            loader = PyPDFLoader(tmp_path)
            docs = loader.load()

            if not docs:
                raise HTTPException(
                    status_code=400, detail="Could not load document")

            splits = process_and_store_documents(db_manager.vector_store, docs)

            db_manager._collection.persist()
            db_manager._collection.get()

            return {
                "status": "success",
                "filename": file.filename,
                "pages_processed": len(docs),
                "chunk_count": len(splits)
            }

        finally:
            os.unlink(tmp_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
