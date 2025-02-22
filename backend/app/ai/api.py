from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from app.agent.base_agent import BaseAgent
from app.doc_loader.web_doc_loader import load_pdfs_from_directory
from app.doc_loader.doc_chunker import process_and_store_documents
from langchain_community.document_loaders import PyPDFLoader
from app.database.database_manager import DatabaseManager
import os
from tempfile import NamedTemporaryFile
import shutil


app = FastAPI()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str

class DocumentLoadRequest(BaseModel):
    directory_path: str

print("Initializing database manager...")
db_manager = DatabaseManager(
    collection_name=os.getenv("COLLECTION_NAME", "general_docs"),
    embedding_model=os.getenv("EMBEDDING_MODEL", "nomic-embed-text"),
    persist_directory=os.getenv("PERSIST_DIRECTORY", "./chroma")
)

data_directory = os.environ.get("DOCUMENTS_DIRECTORY", "app/doc_loader/data")
if os.path.exists(data_directory):
    print(f"Loading documents from {data_directory}...")
    docs = load_pdfs_from_directory(data_directory)
    if docs:
        print("Processing and storing documents...")
        process_and_store_documents(db_manager.vector_store, docs)
        print(f"Loaded {len(docs)} documents into vector store")

print("Initializing agent...")
agent = BaseAgent(vector_store=db_manager.vector_store)

@app.get("/")
async def root():
    return {"message": "Security RAG API is running"}

@app.post("/query")
async def process_query(request: QueryRequest):
    try:
        response = agent.process_message(request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/documents/load")
async def load_documents(request: DocumentLoadRequest):
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

@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        with NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
            
        try:
            loader = PyPDFLoader(tmp_path)
            docs = loader.load()
            
            if not docs:
                raise HTTPException(status_code=400, detail="Could not load document")
            
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

@app.get("/database/stats")
async def get_database_stats():
    try:
        return db_manager.get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/database/clear")
async def clear_database():
    try:
        result = db_manager.clear_collection()
        return {"status": "success", **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/graph")
async def visualize_graph():
    try:
        graph = agent.graph
        mermaid_syntax = graph.get_graph().draw_mermaid()
        return {"mermaid": mermaid_syntax}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))