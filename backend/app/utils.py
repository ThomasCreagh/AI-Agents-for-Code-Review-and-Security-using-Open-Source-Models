from fastapi import Depends

from app.ai.agent.base_agent import BaseAgent
from app.dependencies import get_agent


def process_query(request: str, agent: BaseAgent = Depends(get_agent)):
    try:
        return agent.process_message(request.query)
        # return {"response": response}
    except Exception as e:
        print("ERROR in functon process_query:", e)
