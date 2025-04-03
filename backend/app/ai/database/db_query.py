from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from typing import List
import logging

# Set up logging
logger = logging.getLogger(__name__)

DEFAULT_TEMPLATE = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know. 
Don't try to make up an answer.

Context: {context}

Question: {question}

Answer in a helpful and detailed way.
Provide the output in a markdown format."""


def create_rag_prompt(template=DEFAULT_TEMPLATE):
    return ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", "{question}")
    ])


def query_database(vector_store, query, k=1):
    """
    Retrieve relevant documents from the vector store with fallback options.
    """
    try:
        # Log the retrieval attempt
        logger.info(f"Attempting to retrieve documents with query: {query[:50]}...")
        
        # Try standard similarity search first
        logger.debug("Attempting standard similarity search")
        results = vector_store.similarity_search(query, k=k)
        
        if results:
            logger.info(f"Standard similarity search returned {len(results)} documents")
        else:
            logger.warning("Standard similarity search returned no documents, trying with more lenient parameters")
            
            # If no results, try with different search parameters
            try:
                # Try with more lenient parameters
                results = vector_store.similarity_search(
                    query,
                    k=k,
                    search_kwargs={"k": k, "fetch_k": k*4, "score_threshold": 0.3}
                )
                
                if results:
                    logger.info(f"Lenient search returned {len(results)} documents")
                else:
                    logger.warning("Lenient search still returned no documents")
            except Exception as e:
                logger.error(f"Alternative search failed: {str(e)}")
                
        # If still no results, try getting any documents
        if not results:
            logger.warning("All similarity searches failed, trying direct collection access")
            try:
                # Direct collection access as last resort
                collection = getattr(vector_store, "_collection", None)
                if collection:
                    logger.info("Accessing collection directly")
                    collection_data = collection.get(limit=k)
                    results = []
                    
                    if collection_data and 'documents' in collection_data:
                        for i, text in enumerate(collection_data.get('documents', [])):
                            if text:
                                metadata = {}
                                if 'metadatas' in collection_data and i < len(collection_data['metadatas']):
                                    metadata = collection_data['metadatas'][i] or {}
                                
                                results.append(Document(page_content=text, metadata=metadata))
                        
                        logger.info(f"Direct collection access returned {len(results)} documents")
                    else:
                        logger.warning("Collection appears empty or has no documents")
                else:
                    logger.warning("No _collection attribute available on vector_store")
            except Exception as e:
                logger.error(f"Direct access failed: {str(e)}")
                
        # Log document metadata if any were found
        if results:
            sources = []
            for doc in results:
                metadata = getattr(doc, 'metadata', {})
                source = metadata.get('source', 'unknown')
                sources.append(source)
            logger.info(f"Retrieved document sources: {sources}")
        
        return results
    except Exception as e:
        logger.error(f"Query database error: {str(e)}")
        return []


def rag_query(vector_store, llm, query: str, template=DEFAULT_TEMPLATE, k: int = 1):
    try:
        docs = query_database(vector_store, query, k)
        
        if not docs:
            # Return a response indicating no documents were found
            logger.warning("No relevant documents found for RAG")
            return llm.invoke(f"No relevant security standards found for the query: {query}")
        
        context = "\n".join(doc.page_content for doc in docs)
        prompt = create_rag_prompt(template)
        final_prompt = prompt.format(context=context, question=query)
        return llm.invoke(final_prompt)
        
    except Exception as e:
        logger.error(f"Error in rag_query: {str(e)}")
        # Return a fallback response
        return llm.invoke(f"I encountered an error while retrieving relevant information for: {query}. Please try again or rephrase your question.")