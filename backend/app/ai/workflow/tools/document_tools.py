from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from app.ai.database.db_query import query_database
from app.ai.workflow.utils import log_debug

def retrieve_documents(vector_store, query: str, k: int = 1) -> List[Document]:
    docs = query_database(vector_store, query, k=k)
    log_debug(f"Retrieved {len(docs)} documents")
    return docs

def format_documents(docs: List[Document]) -> tuple[str, List[Dict]]:
    if not docs or len(docs) == 0:
        return "No relevant information found in the knowledge base.", []
    
    formatted_docs = []
    doc_sources = []
    
    for i, doc in enumerate(docs):
        metadata = getattr(doc, 'metadata', {})
        source = metadata.get('source', 'unknown')
        page = metadata.get('page_number', '')
        
        citation_id = f"[{i+1}]"
        formatted_content = f"{doc.page_content} {citation_id}"
        formatted_docs.append(formatted_content)
        
        doc_sources.append({
            'id': citation_id,
            'source': source,
            'page': page
        })
        
        # Log preview
        preview_length = min(100, len(doc.page_content))
        preview = doc.page_content[:preview_length] + "..." if len(doc.page_content) > preview_length else doc.page_content
        log_debug(f"Document {i+1} from '{source}':\n{preview}")
    
    context_text = "\n\n".join(formatted_docs)
    
    source_guide = "\n\nSources:\n"
    for src in doc_sources:
        page_info = f", page {src['page']}" if src['page'] else ""
        source_guide += f"{src['id']} {src['source']}{page_info}\n"
    
    context_text += source_guide
    log_debug(f"Total context length: {len(context_text)} characters")
    
    return context_text, doc_sources

def enhance_query_with_code_analysis(query: str, code_analysis: List[Dict]) -> str:
    if not code_analysis:
        return query
        
    function_info = []
    count = 0
    for analysis in code_analysis:
        for func_name, details in analysis.items():
            if count >= 3:
                break
            params = ', '.join(details['params'])
            function_info.append(f"{func_name}({params})")
            count += 1
        if count >= 3:
            break
    
    if function_info:
        enhanced_query = f"{query} Functions analyzed: {', '.join(function_info)}"
        log_debug(f"Enhanced query with code analysis: '{enhanced_query}'")
        return enhanced_query
    
    return query