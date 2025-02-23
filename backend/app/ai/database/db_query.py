from langchain_core.prompts import ChatPromptTemplate

DEFAULT_TEMPLATE = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know. 
Don't try to make up an answer.

Context: {context}

Question: {question}

Answer in a helpful and detailed way."""


def create_rag_prompt(template=DEFAULT_TEMPLATE):
    return ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", "{question}")
    ])


def query_database(vector_store, query, k=3):
    results = vector_store.similarity_search(query, k=k)
    return results


def rag_query(vector_store, llm, query: str, template=DEFAULT_TEMPLATE, k: int = 3):
    docs = query_database(vector_store, query, k)
    context = "\n".join(doc.page_content for doc in docs)
    prompt = create_rag_prompt(template)
    final_prompt = prompt.format(context=context, question=query)
    return llm.invoke(final_prompt)
