from fastapi import APIRouter, Depends, HTTPException

from app.dependancies import get_agent
from app.core.security import verify_api_key

router = APIRouter(prefix="/graph", tags=["graph"])


@router.get("/", dependencies=[Depends(verify_api_key)])
def visualize_graph(agent: Depends(get_agent)):
    try:
        graph = agent.graph
        mermaid_syntax = graph.get_graph().draw_mermaid()
        return {"mermaid": mermaid_syntax}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
