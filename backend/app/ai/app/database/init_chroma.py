
from langchain_chroma import Chroma 
from langchain_ollama import OllamaEmbeddings


def initialize_vector_store(model: str="nomic-embed-text", collection: str="general_docs") -> Chroma:
    print(f"Embedding Model: {model}")
    print(f"Collection: {collection}")
    embeddings = OllamaEmbeddings(base_url="http://localhost:11434", model=model)
    print("Initialising vectorDB")
    vector_store = Chroma(
        collection_name=collection,
        embedding_function= embeddings,
        persist_directory="./chroma",
    )
    return vector_store

