from app.ai.agent.base_agent import BaseAgent
from app.ai.dependencies import get_ai_dependencies, get_vector_store
from app.ai.database.database_manager import DatabaseManager
import os

print("Initializing AI dependencies...")
ai_deps = get_ai_dependencies()

print("Initializing agent...")
agent = BaseAgent(deps=ai_deps)
print("Finished all initialization")

def get_db_manager():
    db_manager = DatabaseManager(
        collection_name=os.getenv("COLLECTION_NAME", "general_docs"),
        embedding_model=os.getenv("EMBEDDING_MODEL", "nomic-embed-text"),
        persist_directory=os.getenv("PERSIST_DIRECTORY", "./chroma")
    )
    return db_manager

def get_agent():
    return agent