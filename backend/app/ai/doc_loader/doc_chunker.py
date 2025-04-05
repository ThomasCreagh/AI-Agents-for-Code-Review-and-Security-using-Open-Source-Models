from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import logging
import re

logger = logging.getLogger(__name__)

def process_and_store_documents(vector_store, docs):
    print("Proceeding with text splitting...")
    # PERFORMANCE: Larger chunks (3000) and smaller overlap (100) reduce embedding operations
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000, chunk_overlap=100)
    all_splits = text_splitter.split_documents(docs)
    print("Text splitting successful")
    print("Total number of splits:", len(all_splits))
    
    # Improve document source names before storage
    for doc in all_splits:
        # Check if source exists
        source = doc.metadata.get('source', '')
        
        # Try to extract a meaningful title from the content
        title = ""
        if doc.page_content:
            # Get first non-empty line from content
            lines = [line.strip() for line in doc.page_content.split('\n') if line.strip()]
            if lines:
                title = lines[0]
                # If title is longer than 50 chars, truncate it
                if len(title) > 50:
                    title = title[:50] + "..."
        
        # Always save title if we found one
        if title:
            doc.metadata['title'] = title
        
        # Clean up source if it's a path or temporary filename
        if source:
            # First, try to get original filename from path
            orig_filename = os.path.basename(source)
            
            # Look for patterns like "tmp123456_actual-filename.pdf"
            tmp_match = re.match(r'tmp[^_]*_(.+)', orig_filename)
            if tmp_match:
                # Extract the part after tmp prefix
                orig_filename = tmp_match.group(1)
            
            # If the filename is still not good (like "n_.pdf")
            if len(orig_filename) <= 6 or orig_filename.startswith("n_"):
                # Use a better name based on content
                if title:
                    # Create a filename from title
                    clean_title = re.sub(r'[^\w\s-]', '', title.lower())
                    clean_title = re.sub(r'[\s-]+', '-', clean_title)
                    file_ext = os.path.splitext(orig_filename)[1] or '.pdf'
                    orig_filename = f"{clean_title[:30]}{file_ext}"
                else:
                    # Generic name
                    orig_filename = "security-standard.pdf"
            
            # Update metadata with better filename
            doc.metadata['source'] = orig_filename
            print(f"Updated document source name: {source} → {orig_filename}")

    print("Adding documents to DB")
    vector_store.add_documents(all_splits)
    print("DB data insertion successful")

    return all_splits