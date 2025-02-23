from app.ai.agent.base_agent import BaseAgent
from app.ai.doc_loader.web_doc_loader import load_pdfs_from_directory
from app.ai.doc_loader.doc_chunker import process_and_store_documents
from app.ai.database.database_manager import DatabaseManager
import os

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
print("Finished all initialization")


def get_db_manager():
    return db_manager


def get_agent():
    return agent
