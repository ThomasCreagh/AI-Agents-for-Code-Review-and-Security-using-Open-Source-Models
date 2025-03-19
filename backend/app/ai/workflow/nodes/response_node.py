from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.models import AgentState
import time

from app.ai.dependencies import AIDependencies
from app.ai.workflow.utils import log_debug
from app.ai.workflow.tools.security_tools import create_final_response_prompt
from app.ai.workflow.tools.message_tools import create_prompt_message, format_llm_response

def generate_response(state: AgentState, deps: AIDependencies):
    messages = state["messages"]
    query = state["latest_user_message"]
    context = state.get("context", {})

    time.sleep(0.5)

    response_prompt_content = create_final_response_prompt()
    response_prompt = create_prompt_message(response_prompt_content)

    query_message = HumanMessage(content=f"User question: {query}")

    agent_messages = [response_prompt] + messages + [query_message]

    log_debug(f"Sending final response request to LLM")

    response = deps.llm.invoke(agent_messages)
    formatted_response = format_llm_response(response)

    return {
        "messages": messages + [formatted_response],
        "latest_user_message": query,
        "context": context  
    }