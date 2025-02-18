from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
# from dotenv import load_dotenv
import os
import shutil

# load_dotenv()


def load_and_process_pdfs():
    """Load PDFs from directory and split into chunks."""
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    loader = DirectoryLoader(
        data_dir,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )
    documents = loader.load()

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    return chunks


class RagDB:
    def __init__(self):
        # Initialize HuggingFace embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2",
            model_kwargs={'device': 'cpu'}
        )
        # make vector store
        self.chroma_db = self.create_vector_store()

    def create_vector_store(self):
        """Create and persist Chroma vector store."""
        # persist_directory = os.path.join(
        #     os.path.dirname(__file__), "chroma_db")
        persist_directory = "app/ai/llm_rag_database/chroma_db"
        os.makedirs(persist_directory, exist_ok=True)

        # # Clear existing vector store
        # if os.path.exists(persist_directory):
        #     print(f"Clearing existing vector store at {persist_directory}")
        #     shutil.rmtree(persist_directory)

        print("Creating new vector store...")

        db = Chroma(
            embedding_function=self.embeddings,
            persist_directory=persist_directory,
            collection_name="document_collection"
        )

        if not db.get()["ids"]:  # Check if collection is empty
            print("⚠️ Collection is empty. Make sure to add documents.")
        return db

    def add_documents(self, document):
        # content_to_vectorize = document.get('content')
        content_to_vectorize = str(document.model_dump_json())
        vectors = self.embeddings.embed_documents(
            [content_to_vectorize])  # Assuming this produces vectors
        # Use first vector
        documents_to_add = [
            {"content": content_to_vectorize, "vector": vectors[0]}]
        self.chroma_db.add_documents(documents_to_add)

    # def init():
    #     print("Creating vector store...")
    #     create_vector_store(chunks, db_dir)
    #     print(f"Vector store created and persisted at {db_dir}")
