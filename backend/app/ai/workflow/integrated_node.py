from langchain_core.messages import SystemMessage
from app.models import AgentState

def integrated_analysis_agent(state: AgentState):
    """Agent that combines document context with code analysis."""
    from app.ai.workflow.graph_config import log_debug
    
    messages = state["messages"]
    query = state["latest_user_message"]
    context = state.get("context", {})
    
    # Check if we have code analysis results
    code_analysis = context.get("code_analysis", [])
    has_code_analysis = len(code_analysis) > 0
    
    # Check if we have retrieved documents
    retrieved_docs = context.get("retrieved_docs", [])
    has_documents = len(retrieved_docs) > 0
    
    # Get document sources
    doc_sources = context.get("doc_sources", [])
    
    log_debug(f"Integrated analysis: Code analysis: {has_code_analysis}, Documents: {has_documents}")
    
    if not has_code_analysis and not has_documents:
        log_debug("No code analysis or documents to integrate")
        return state
    
    # Create an integration of code analysis and standards
    integration_content = ""
    
    if has_code_analysis:
        # Extract function details to make them more prominent
        integration_content += "## Code Structure Summary\n\n"
        for analysis_idx, analysis in enumerate(code_analysis):
            for func_name, details in analysis.items():
                params = ', '.join(details['params'])
                returns = []
                for ret in details.get('returns', []):
                    if isinstance(ret, dict):
                        returns.append(f"{ret.get('value', 'unknown')} ({ret.get('type', 'unknown')})")
                
                returns_str = ", ".join(returns) if returns else "None"
                
                integration_content += f"- Function: `{func_name}({params})` → Returns: {returns_str}\n"
    
    if has_documents:
        # Extract relevant standards from documents with citation markers
        integration_content += "\n## Relevant Security Standards\n\n"
        
        for i, doc in enumerate(retrieved_docs):
            metadata = getattr(doc, 'metadata', {})
            source = metadata.get('source', 'unknown')
            citation_id = f"[{i+1}]"
            
            # Add source with citation marker
            integration_content += f"### From {source} {citation_id}\n"
            integration_content += f"{doc.page_content}\n\n"
    
    if has_code_analysis and has_documents:
        # Add specific instructions for analysis
        integration_content += "\n## Integration Instructions\n\n"
        integration_content += "Compare the code structure with the security standards to identify:\n"
        integration_content += "1. Potential security vulnerabilities based on function parameters and returns\n"
        integration_content += "2. Missing security controls required by the standards\n"
        integration_content += "3. Compliance violations in the implementation approach\n\n"
        integration_content += "When referencing security standards in your analysis, please use the citation markers ([1], [2], etc.).\n"
    
    # Add source reference guide
    if has_documents:
        integration_content += "\n## Source References\n\n"
        for i, source in enumerate(doc_sources):
            if isinstance(source, dict):
                # New format with detailed source info
                page_info = f", page {source.get('page', '')}" if source.get('page', '') else ""
                integration_content += f"[{i+1}] {source.get('source', 'unknown')}{page_info}\n"
            else:
                # Old format with just source name
                integration_content += f"[{i+1}] {source}\n"
    
    # Create a message linking code analysis with documentation
    integration_message = SystemMessage(content=integration_content)
    
    log_debug("Created integrated analysis with combined context and source attribution")
    
    return {
        "messages": messages + [integration_message],
        "latest_user_message": query,
        "context": context
    }