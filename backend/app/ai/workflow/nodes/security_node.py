from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.models import AgentState
import time

from app.ai.dependencies import AIDependencies
from app.ai.workflow.utils import log_debug
from app.ai.workflow.tools.security_tools import format_document_sources, create_security_prompt
from app.ai.workflow.tools.message_tools import create_prompt_message, create_query_message, format_llm_response

def security_analysis_agent(state: AgentState, deps: AIDependencies):
    messages = state["messages"]
    query = state["latest_user_message"]
    context = state.get("context", {})

    time.sleep(0.5)

    doc_sources = context.get("doc_sources", [])
    source_names = format_document_sources(doc_sources)
    
    code_analysis = context.get("code_analysis", [])
    has_code_analysis = len(code_analysis) > 0
    
    if has_code_analysis:
        log_debug("Security analysis includes code analysis results")

    security_prompt_content = create_security_prompt(has_code_analysis)
    security_prompt = create_prompt_message(security_prompt_content)

    query_message = create_query_message(query)

    agent_messages = [security_prompt] + messages + [query_message]

    log_debug(f"Sending security analysis request to LLM with {len(agent_messages)} messages")

    response = deps.llm.invoke(agent_messages)
    formatted_response = format_llm_response(response)

    return {
        "messages": messages + [formatted_response],
        "latest_user_message": query,
        "context": context  
    }