from langchain_text_splitters import RecursiveCharacterTextSplitter


def process_and_store_documents(vector_store, docs):
    print("Proceeding with text splitting...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_splits = text_splitter.split_documents(docs)
    print("Text splitting successful")
    print("Total number of splits:", len(all_splits))
    print("Adding documents to DB")
    vector_store.add_documents(all_splits)
    print("DB data insertion successful")

    return all_splits