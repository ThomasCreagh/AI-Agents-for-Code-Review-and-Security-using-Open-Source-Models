from typing import List, Dict, Any, Optional, Tuple
from langchain_core.documents import Document
from app.ai.database.db_query import query_database
from app.ai.workflow.utils import log_debug, LOG_LEVEL_INFO, LOG_LEVEL_DEBUG, LOG_LEVEL_ERROR, LOG_LEVEL_WARN
import os

def retrieve_documents(vector_store, query: str, k: int = 1) -> List[Document]:
    """
    Retrieve relevant documents from the vector store with diagnostics.
    """
    # Initialize a fallback documents list
    fallback_docs = []
    total_docs = 0
    
    # Get collection stats before querying
    try:
        log_debug("Checking collection state before query", level=LOG_LEVEL_INFO)
        collection = getattr(vector_store, "_collection", None)
        if collection:
            collection_data = collection.get()
            total_docs = len(collection_data['ids']) if 'ids' in collection_data else 0
            log_debug(f"Collection has {total_docs} documents before querying", level=LOG_LEVEL_INFO)
            
            # Log the first few document sources for verification
            if total_docs > 0 and 'metadatas' in collection_data:
                sources = []
                for metadata in collection_data['metadatas'][:3]:  # First 3 docs
                    if metadata and 'source' in metadata:
                        sources.append(metadata['source'])
                    else:
                        sources.append("No source metadata")
                log_debug(f"Sample document sources in collection: {sources}", level=LOG_LEVEL_INFO)
            else:
                log_debug("Collection has documents but no metadata or empty", level=LOG_LEVEL_WARN)
        else:
            log_debug("No _collection attribute available on vector_store", level=LOG_LEVEL_WARN)
    except Exception as e:
        log_debug(f"Error checking collection: {str(e)}", level=LOG_LEVEL_ERROR)

    # Try direct collection access to get ALL documents
    try:
        direct_docs = []
        if collection and total_docs > 0:
            log_debug("Attempting direct collection access", level=LOG_LEVEL_INFO)
            all_data = collection.get(include=["documents", "metadatas"])
            
            if all_data and 'documents' in all_data:
                for i, text in enumerate(all_data.get('documents', [])):
                    if text:
                        metadata = {}
                        if 'metadatas' in all_data and i < len(all_data['metadatas']):
                            metadata = all_data['metadatas'][i] or {}
                        
                        direct_docs.append(Document(page_content=text, metadata=metadata))
                
                log_debug(f"Direct access found {len(direct_docs)} documents", level=LOG_LEVEL_INFO)
                
                # If we found documents directly, store them for fallback
                if direct_docs:
                    fallback_docs = direct_docs[:k]
                    # Log the contents of fallback documents
                    for i, doc in enumerate(fallback_docs):
                        metadata = getattr(doc, 'metadata', {})
                        source = metadata.get('source', 'unknown')
                        preview = doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
                        log_debug(f"Fallback doc {i+1} - Source: {source}", level=LOG_LEVEL_DEBUG, data=preview)
            else:
                log_debug("Direct access returned no documents data", level=LOG_LEVEL_WARN)
    except Exception as e:
        log_debug(f"Error in direct collection access: {str(e)}", level=LOG_LEVEL_ERROR)
    
    # Attempt normal retrieval
    try:
        # Regular similarity search
        log_debug(f"Attempting similarity search with query: {query[:50]}...", level=LOG_LEVEL_INFO)
        docs = query_database(vector_store, query, k=k)
        log_debug(f"Retrieved {len(docs)} documents via similarity search", level=LOG_LEVEL_INFO)
        
        # Log the retrieved documents
        if docs:
            for i, doc in enumerate(docs):
                metadata = getattr(doc, 'metadata', {})
                source = metadata.get('source', 'unknown')
                preview = doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
                log_debug(f"Retrieved doc {i+1} - Source: {source}", level=LOG_LEVEL_DEBUG, data=preview)
        
        # If no documents found but we have fallback docs, use them
        if not docs and fallback_docs:
            log_debug("Using fallback documents since similarity search returned nothing", level=LOG_LEVEL_INFO)
            docs = fallback_docs
            
        return docs
    except Exception as e:
        log_debug(f"Error in retrieve_documents: {str(e)}", level=LOG_LEVEL_ERROR)
        # Return fallback docs if available
        if fallback_docs:
            log_debug("Returning fallback docs after error", level=LOG_LEVEL_INFO)
            return fallback_docs
        return []

def format_documents(docs: List[Document], code_summary: Dict = None) -> Tuple[str, List[Dict]]:
    """
    Format documents for context, adding citation markers.
    """
    if not docs or len(docs) == 0:
        return "No relevant information found in the knowledge base.", []
    
    formatted_docs = []
    doc_sources = []
    
    log_debug(f"Formatting {len(docs)} documents for context", level=LOG_LEVEL_INFO)
    
    for i, doc in enumerate(docs):
        metadata = getattr(doc, 'metadata', {})
        
        # Prefer title over source for display name
        title = metadata.get('title', '')
        source = metadata.get('source', 'Security Standard')
        display_name = title if title else source
        
        # Clean up source if it's a temporary path
        if '/tmp/' in source or '\\tmp\\' in source:
            source = os.path.basename(source)
        
        page = metadata.get('page_number', '')
        
        log_debug(f"Formatting document {i+1} from source: {display_name}", level=LOG_LEVEL_DEBUG)
        
        # Limit document content to 500 characters to reduce token usage
        doc_content = doc.page_content
        if len(doc_content) > 500:
            doc_content = doc_content[:500] + "..."
        
        citation_id = f"[{i+1}]"
        
        formatted_content = f"{doc_content} {citation_id}"
        formatted_docs.append(formatted_content)
        
        doc_sources.append({
            'id': citation_id,
            'source': display_name,  # Use the better display name
            'page': page
        })
        
        # Log preview
        preview_length = min(100, len(doc_content))
        preview = doc_content[:preview_length] + "..." if len(doc_content) > preview_length else doc_content
        log_debug(f"Document {i+1} from '{display_name}':\n{preview}", level=LOG_LEVEL_DEBUG)
    
    context_text = "\n\n".join(formatted_docs)
    
    # Limit the overall context text to 1000 characters to prevent memory issues
    if len(context_text) > 1000:
        context_text = context_text[:1000] + "..."
    
    # Make the source information more prominent and explicitly instruct to only use these sources
    source_guide = "\n\nREFERENCE SOURCES (MUST BE CITED):\n"
    for src in doc_sources:
        page_info = f", page {src['page']}" if src['page'] else ""
        source_guide += f"{src['id']} {src['source']}{page_info}\n"
    
    context_text += source_guide
    
    # Add explicit instruction to only use these sources
    context_text += "\n\nIMPORTANT: Base all security recommendations ONLY on these sources. Do not reference any security standards not listed above."
    
    log_debug(f"Total context length: {len(context_text)} characters", level=LOG_LEVEL_INFO)
    log_debug(f"Formatted document sources:", level=LOG_LEVEL_INFO, data=[src for src in doc_sources])
    
    return context_text, doc_sources

def enhance_query_with_code_summary(query: str, code_summary: Dict) -> str:
    """
    Enhance a query with information from a structured code summary.
    
    Args:
        query: The original query
        code_summary: The structured code summary
    
    Returns:
        Enhanced query string
    """
    if not code_summary:
        return query
    
    # Build enhancement components
    components = []
    
    # Basic statistics
    components.append(f"Code contains {code_summary.get('function_count', 0)} functions and {code_summary.get('class_count', 0)} classes")
    
    # Add sensitive functions if any
    if code_summary.get('sensitive_functions'):
        sensitive_funcs = code_summary['sensitive_functions'][:3]  # Limit to first 3
        components.append(f"Functions with sensitive parameters: {', '.join(sensitive_funcs)}")
    
    # Add security operations if any
    security_ops = []
    for op_type, funcs in code_summary.get('security_operations', {}).items():
        if funcs:
            security_ops.append(f"{op_type} ({funcs[0]})")
    
    if security_ops:
        components.append(f"Security-related operations: {', '.join(security_ops[:3])}")
    
    # Create enhanced query
    context_info = "; ".join(components)
    enhanced_query = f"{query}\n\nCode context: {context_info}"
    
    # Limit the enhanced query length to prevent memory issues
    if len(enhanced_query) > 1500:
        enhanced_query = enhanced_query[:1500]
    
    log_debug(f"Enhanced query with code summary: '{enhanced_query}'")
    return enhanced_query