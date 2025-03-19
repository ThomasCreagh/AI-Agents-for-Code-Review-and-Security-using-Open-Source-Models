from langchain_core.messages import SystemMessage
from app.models import AgentState
from app.ai.workflow.utils import log_debug
from app.ai.workflow.tools.message_tools import create_integration_message

def integrated_analysis_agent(state: AgentState):
    messages = state["messages"]
    query = state["latest_user_message"]
    context = state.get("context", {})
    
    code_analysis = context.get("code_analysis", [])
    has_code_analysis = len(code_analysis) > 0
    
    retrieved_docs = context.get("retrieved_docs", [])
    has_documents = len(retrieved_docs) > 0
    
    doc_sources = context.get("doc_sources", [])
    
    log_debug(f"Integrated analysis: Code analysis: {has_code_analysis}, Documents: {has_documents}")
    
    if not has_code_analysis and not has_documents:
        log_debug("No code analysis or documents to integrate")
        return state
    
    integration_content = ""
    
    if has_code_analysis:
        integration_content += "Functions: "
        function_list = []
        for analysis_idx, analysis in enumerate(code_analysis):
            if analysis_idx >= 2:
                break
            for func_name, details in analysis.items():
                if len(function_list) >= 5:
                    break
                params = ', '.join(details['params'][:3])
                function_list.append(f"{func_name}({params})")
        
        integration_content += ", ".join(function_list)
        integration_content += "\n\n"
    
    if has_documents:
        integration_content += "Security standards: "
        
        total_doc_length = 0
        for i, doc in enumerate(retrieved_docs):
            if i >= 1:
                break
                
            metadata = getattr(doc, 'metadata', {})
            source = metadata.get('source', 'unknown')
            citation_id = f"[{i+1}]"
            
            doc_content = doc.page_content
            if len(doc_content) > 500:
                doc_content = doc_content[:500] + "..."
                
            integration_content += f"{source} {citation_id}: {doc_content}\n\n"
            total_doc_length += len(doc_content)
            
            if total_doc_length > 1000:
                break
    
    if has_documents:
        integration_content += "Sources: "
        sources = []
        for i, source in enumerate(doc_sources):
            if i >= 2:
                break
            if isinstance(source, dict):
                sources.append(f"[{i+1}] {source.get('source', 'unknown')}")
            else:
                sources.append(f"[{i+1}] {source}")
        integration_content += ", ".join(sources)
    
    integration_message = create_integration_message(integration_content)
    
    log_debug("Created integrated analysis with minimal content")
    
    return {
        "messages": messages + [integration_message],
        "latest_user_message": query,
        "context": context
    }