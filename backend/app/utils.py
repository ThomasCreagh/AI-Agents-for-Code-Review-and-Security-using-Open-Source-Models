from fastapi import Depends

from app.dependancies import get_agent


def process_query(request: str, agent: Depends(get_agent)):
    try:
        response = agent.process_message(request.query)
        return {"response": response}
    except Exception as e:
        print("ERROR in functon process_query:", e)
