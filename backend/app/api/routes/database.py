from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_db_manager
from app.core.security import verify_api_key
from app.ai.database.database_manager import DatabaseManager

router = APIRouter(prefix="/database", tags=["database"])


@router.get("/stats", dependencies=[Depends(verify_api_key)])
def get_database_stats(db_manager: DatabaseManager = Depends(get_db_manager)):
    try:
        return db_manager.get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clear", dependencies=[Depends(verify_api_key)])
def clear_database(db_manager: DatabaseManager = Depends(get_db_manager)):
    try:
        result = db_manager.clear_collection()
        return {"status": "success", **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
