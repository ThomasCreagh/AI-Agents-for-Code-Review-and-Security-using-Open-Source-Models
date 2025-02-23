from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from typing import List
import os
# import sys
import traceback


def debug_load_url(urls: List[str] = ["https://langchain-ai.github.io/langgraph/tutorials/introduction/"]):
    print("Starting doc debug process...")
    print("Step 1: Starting URL load process")
    try:
        print("Step 2: Initializing loader")
        loader = WebBaseLoader(urls)

        print("Step 3: Attempting to load document")
        docs = loader.load()

        print("Step 4: Document loaded successfully")
        print(f"Number of documents: {len(docs)}")

        return docs
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        print("Stack trace:")
        traceback.print_exc()
        return None


def load_pdfs_from_directory(directory_path):
    """
    Load PDF documents from a specified directory.

    Args:
        directory_path: Path to the directory containing PDF files

    Returns:
        List of loaded documents or None if an error occurs
    """
    print(f"Loading PDF files from directory: {directory_path}")
    try:
        # Get all PDF files in the directory
        pdf_files = [
            os.path.join(directory_path, filename)
            for filename in os.listdir(directory_path)
            if filename.lower().endswith('.pdf')
        ]

        if not pdf_files:
            print(f"No PDF files found in {directory_path}")
            return None

        print(f"Found {len(pdf_files)} PDF files")

        # Load each PDF file
        all_docs = []
        for pdf_path in pdf_files:
            print(f"Loading: {pdf_path}")
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            all_docs.extend(docs)

        print(f"Successfully loaded {len(all_docs)} document pages")
        return all_docs

    except Exception as e:
        print(f"Error loading PDFs: {str(e)}")
        print("Stack trace:")
        traceback.print_exc()
        return None
