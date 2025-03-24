from typing import List, Dict, Any, Union
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.ai.workflow.utils import log_debug

def create_context_message(context_text: str) -> SystemMessage:
    return SystemMessage(
        content=f"Context for the security question:\n\n{context_text}"
    )

def create_error_message(error_text: str) -> SystemMessage:
    return SystemMessage(
        content=f"Note: {error_text}"
    )

def create_analysis_message(analysis_text: str) -> SystemMessage:
    return SystemMessage(
        content=analysis_text
    )

def create_integration_message(integration_content: str) -> SystemMessage:
    return SystemMessage(
        content=integration_content
    )

def create_prompt_message(prompt_content: str) -> SystemMessage:
    return SystemMessage(
        content=prompt_content
    )

def create_query_message(query: str) -> HumanMessage:
    return HumanMessage(
        content=f"Security analysis for: {query}"
    )

def format_llm_response(response: Union[str, AIMessage]) -> AIMessage:
    if not isinstance(response, AIMessage):
        response = AIMessage(content=str(response))
    
    preview_length = min(50, len(response.content))
    log_debug(f"Response generated: {response.content[:preview_length]}...")
    
    return response