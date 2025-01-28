from fastapi import APIRouter

from app.models import Item

router = APIRouter(prefix="/items")


@router.get("/{id}")
def read_item(item_id: int, q: Item):
    return {"item_id": item_id, "q": q}
