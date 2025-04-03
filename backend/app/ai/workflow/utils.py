import os
import json
import time
import inspect
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

# Configure log directory
DEBUG_LOG_PATH = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(DEBUG_LOG_PATH, exist_ok=True)
DEBUG_LOG_FILE = os.path.join(DEBUG_LOG_PATH, "rag_debug.log")

# Define log levels
LOG_LEVEL_INFO = "INFO"
LOG_LEVEL_DEBUG = "DEBUG"
LOG_LEVEL_ERROR = "ERROR"
LOG_LEVEL_WARN = "WARN"

# Define section markers
SECTION_SEPARATOR = "=" * 80
SUBSECTION_SEPARATOR = "-" * 60

def log_debug(message, level=LOG_LEVEL_INFO, format_json=False, data=None):
    """
    Enhanced debug logging with support for levels and structured data.
    
    Args:
        message: The log message
        level: Log level (INFO, DEBUG, ERROR, WARN)
        format_json: Whether to format the data as JSON
        data: Optional data to log in structured format
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    # Get calling function name for better context
    caller_frame = inspect.currentframe().f_back
    caller_name = caller_frame.f_code.co_name if caller_frame else "unknown"
    
    # Format log entry
    log_entry = f"[{timestamp}] [{level}] [{caller_name}] {message}"
    
    # Add formatted data if provided
    if data is not None:
        if format_json:
            try:
                formatted_data = json.dumps(data, indent=2, default=str)
                log_entry += f"\n{formatted_data}"
            except:
                log_entry += f"\n{data}"
        else:
            log_entry += f"\n{data}"
    
    # Print to console
    print(f"[RAG DEBUG] {log_entry}")
    
    # Write to log file
    with open(DEBUG_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{log_entry}\n")

def log_agent_start(agent_name: str, state: Dict[str, Any]):
    """Log the start of an agent's execution with input state summary"""
    log_debug(f"{SECTION_SEPARATOR}", level=LOG_LEVEL_INFO)
    log_debug(f"AGENT START: {agent_name}", level=LOG_LEVEL_INFO)
    
    # Log user query
    query = state.get("latest_user_message", "")
    if query:
        # Truncate long queries in log
        truncated = query[:100] + "..." if len(query) > 100 else query
        log_debug(f"Input query: {truncated}", level=LOG_LEVEL_INFO)
    
    # Log message count
    messages = state.get("messages", [])
    log_debug(f"Current message count: {len(messages)}", level=LOG_LEVEL_DEBUG)
    
    # Log context summary
    context = state.get("context", {})
    context_summary = {}
    
    if "code_analysis" in context:
        code_analysis = context.get("code_analysis", [])
        if code_analysis:
            function_count = sum(len(analysis) for analysis in code_analysis if analysis)
            context_summary["code_analysis"] = f"{function_count} functions analyzed"
    
    if "retrieved_docs" in context:
        retrieved_docs = context.get("retrieved_docs", [])
        context_summary["retrieved_docs"] = f"{len(retrieved_docs)} documents"
    
    if context_summary:
        log_debug("Context summary:", level=LOG_LEVEL_DEBUG, data=context_summary)

def log_agent_end(agent_name: str, original_state: Dict[str, Any], new_state: Dict[str, Any]):
    """Log the end of an agent's execution with state changes"""
    log_debug(f"AGENT END: {agent_name}", level=LOG_LEVEL_INFO)
    
    # Calculate what changed in the state
    changes = {}
    
    # Check context changes
    orig_context = original_state.get("context", {})
    new_context = new_state.get("context", {})
    
    # Message count changes
    orig_msg_count = len(original_state.get("messages", []))
    new_msg_count = len(new_state.get("messages", []))
    
    if new_msg_count > orig_msg_count:
        changes["messages"] = f"Added {new_msg_count - orig_msg_count} new messages"
    
    # Context key changes
    new_keys = set(new_context.keys()) - set(orig_context.keys())
    if new_keys:
        changes["new_context_keys"] = list(new_keys)
    
    # Log routing decision if present
    if "route_to" in new_state:
        changes["route_to"] = new_state["route_to"]
    
    if changes:
        log_debug("State changes:", level=LOG_LEVEL_DEBUG, data=changes)
    
    log_debug(f"{SECTION_SEPARATOR}\n", level=LOG_LEVEL_INFO)

def format_document_preview(docs: List[Any]) -> str:
    """Format document preview for logs"""
    if not docs:
        return "No documents"
    
    preview = []
    for i, doc in enumerate(docs):
        if hasattr(doc, 'page_content') and hasattr(doc, 'metadata'):
            content = doc.page_content
            truncated = content[:100] + "..." if len(content) > 100 else content
            metadata = getattr(doc, 'metadata', {})
            source = metadata.get('source', 'unknown')
            preview.append(f"Doc {i+1}: {source} - {truncated}")
    
    return "\n".join(preview)

def format_code_analysis(analysis_results: List[Dict]) -> str:
    """Format code analysis for logs"""
    if not analysis_results:
        return "No code analysis"
    
    preview = []
    for i, result in enumerate(analysis_results):
        functions = list(result.keys())
        truncated = functions[:5]
        if len(functions) > 5:
            truncated.append("...")
        preview.append(f"Analysis {i+1}: {', '.join(truncated)}")
    
    return "\n".join(preview)