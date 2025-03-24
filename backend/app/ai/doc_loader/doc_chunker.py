from langchain_text_splitters import RecursiveCharacterTextSplitter


def process_and_store_documents(vector_store, docs):
    print("Proceeding with text splitting...")
    # PERFORMANCE: Larger chunks (3000) and smaller overlap (100) reduce embedding operations
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000, chunk_overlap=100)
    all_splits = text_splitter.split_documents(docs)
    print("Text splitting successful")
    print("Total number of splits:", len(all_splits))
    print("Adding documents to DB")
    vector_store.add_documents(all_splits)
    print("DB data insertion successful")

    return all_splits