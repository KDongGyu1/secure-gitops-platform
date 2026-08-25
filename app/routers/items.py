from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.schemas import ItemCreate, ItemUpdate, ItemResponse, ItemModel

router = APIRouter(prefix="/items", tags=["items"])


@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, db: Session = Depends(get_db)) -> ItemResponse:
    db_item = ItemModel(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("", response_model=list[ItemResponse])
def get_items(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[ItemResponse]:
    items = db.query(ItemModel).offset(skip).limit(limit).all()
    return items


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)) -> ItemResponse:
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {item_id} not found"
        )
    return item


@router.patch("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int, item: ItemUpdate, db: Session = Depends(get_db)
) -> ItemResponse:
    db_item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {item_id} not found"
        )
    if item.name is not None:
        db_item.name = item.name
    if item.description is not None:
        db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> None:
    db_item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {item_id} not found"
        )
    db.delete(db_item)
    db.commit()
