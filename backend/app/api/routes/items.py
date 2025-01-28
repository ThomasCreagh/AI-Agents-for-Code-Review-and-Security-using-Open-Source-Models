from fastapi import APIRouter
from typing import Union

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/{id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
