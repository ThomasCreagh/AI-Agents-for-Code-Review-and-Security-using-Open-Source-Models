from langchain_core.messages import SystemMessage
from app.models import AgentState
from app.ai.workflow.utils import (
    log_debug, log_agent_start, log_agent_end,
    LOG_LEVEL_INFO, LOG_LEVEL_DEBUG, LOG_LEVEL_WARN,
    format_document_preview, format_code_analysis
)
from app.ai.workflow.tools.message_tools import create_integration_message

def integrated_analysis_agent(state: AgentState):
    """
    Integrates code analysis and retrieved documents to create a consolidated view
    for security analysis.
    """
    # Log agent start
    log_agent_start("INTEGRATION", state)
    
    # Store original state for comparison
    original_state = state.copy()
    
    messages = state["messages"]
    query = state["latest_user_message"]
    context = state.get("context", {})
    
    # Check if we have code analysis or documents
    code_analysis = context.get("code_analysis", [])
    has_code_analysis = len(code_analysis) > 0
    
    # Check for structured code summary
    code_summary = context.get("code_summary", None)
    has_code_summary = code_summary is not None
    
    retrieved_docs = context.get("retrieved_docs", [])
    has_documents = len(retrieved_docs) > 0
    
    doc_sources = context.get("doc_sources", [])
    
    # Log integration inputs
    log_debug(
        "Integration inputs:", 
        level=LOG_LEVEL_INFO,
        data={
            "has_code_analysis": has_code_analysis,
            "has_code_summary": has_code_summary,
            "code_analysis_blocks": len(code_analysis) if has_code_analysis else 0,
            "has_documents": has_documents,
            "document_count": len(retrieved_docs) if has_documents else 0
        }
    )
    
    # If nothing to integrate, return state unchanged
    if not (has_code_analysis or has_documents):
        log_debug("No code analysis or documents to integrate", level=LOG_LEVEL_WARN)
        # Log agent end (no changes)
        log_agent_end("INTEGRATION", original_state, state)
        return state
    
    # Build integration content
    integration_content = ""
    
    # If we have code summary, use it for integration
    if has_code_summary:
        log_debug(
            "Using structured code summary for integration", 
            level=LOG_LEVEL_INFO
        )
        
        # Build function information using the structured summary
        integration_content += "Code Overview:\n"
        integration_content += f"- {code_summary['function_count']} functions, {code_summary['class_count']} classes\n"
        
        integration_content = integration_content[:1000]  # Limit to 1000 characters
        # Add sensitive functions if any
        if code_summary.get('sensitive_functions'):
            sensitive_funcs = code_summary['sensitive_functions'][:3]  # Limit to first 3
            integration_content += f"- Functions with sensitive parameters: {', '.join(sensitive_funcs)}\n"
        
        # Add security operations categorization
        for op_type, funcs in code_summary.get('security_operations', {}).items():
            if funcs:
                op_name = op_type.replace("_", " ").title()
                integration_content += f"- {op_name}: {', '.join(funcs[:2])}\n"
        
        integration_content += "\n"
        
    # If we have code analysis but no summary, use the analysis directly
    elif has_code_analysis:
        log_debug(
            "Integrating code analysis:", 
            level=LOG_LEVEL_DEBUG,
            data=format_code_analysis(code_analysis)
        )
        
        # Build function list
        integration_content += "Functions: "
        function_list = []
        function_count = 0
        
        for analysis_idx, analysis in enumerate(code_analysis):
            if analysis_idx >= 2:  # Limit to first 2 analyses
                break
            for func_name, details in analysis.items():
                if function_count >= 5:  # Limit to first 5 functions
                    break
                function_count += 1
                params = ', '.join(details['params'][:3])  # Limit to first 3 params
                function_list.append(f"{func_name}({params})")
        
        integration_content += ", ".join(function_list)
        integration_content += "\n\n"
        
        log_debug(f"Added {function_count} functions to integration", level=LOG_LEVEL_DEBUG)
    
    # If we have documents, add them to the integration
    if has_documents:
        log_debug(
            "Integrating documents:", 
            level=LOG_LEVEL_DEBUG,
            data=format_document_preview(retrieved_docs)
        )
        
        integration_content += "Security standards: "
        
        document_count = 0
        
        for i, doc in enumerate(retrieved_docs):
            if i >= 1:  # Only use first document
                break
                
            document_count += 1
            metadata = getattr(doc, 'metadata', {})
            source = metadata.get('source', 'unknown')
            citation_id = f"[{i+1}]"
            
            doc_content = doc.page_content
            
            integration_content += f"{source} {citation_id}: {doc_content}\n\n"
        
        log_debug(f"Added {document_count} documents to integration", level=LOG_LEVEL_DEBUG)
    
    # Add source references
    if has_documents:
        integration_content += "Sources: "
        sources = []
        
        for i, source in enumerate(doc_sources):
            if i >= 2:  # Limit to first 2 sources
                break
            if isinstance(source, dict):
                sources.append(f"[{i+1}] {source.get('source', 'unknown')}")
            else:
                sources.append(f"[{i+1}] {source}")
        
        integration_content += ", ".join(sources)
        log_debug(f"Added {len(sources)} source references", level=LOG_LEVEL_DEBUG)
    
    # Create integration message
    integration_message = create_integration_message(integration_content)
    
    # Log integration content length
    log_debug(
        f"Integration content created (length: {len(integration_content)} chars)", 
        level=LOG_LEVEL_INFO
    )
    
    # Create updated state
    new_state = {
        "messages": messages + [integration_message],
        "latest_user_message": query,
        "context": context  # Preserve full context including code_summary
    }
    
    # Log agent end
    log_agent_end("INTEGRATION", original_state, new_state)
    
    return new_state