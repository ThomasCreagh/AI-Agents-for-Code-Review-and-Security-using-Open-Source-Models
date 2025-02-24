from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_agent
from app.core.security import verify_api_key
from app.ai.agent.base_agent import BaseAgent

router = APIRouter(prefix="/graph", tags=["graph"])


@router.get("/", dependencies=[Depends(verify_api_key)])
def visualize_graph(agent: BaseAgent = Depends(get_agent)):
    try:
        graph = agent.graph
        mermaid_syntax = graph.get_graph().draw_mermaid()
        return {"mermaid": mermaid_syntax}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
