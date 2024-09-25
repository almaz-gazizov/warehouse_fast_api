from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import services
from app.database import get_db
from app.schemas import Order, OrderCreate

router = APIRouter()


@router.post("/orders/", response_model=Order)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return services.create_product(db, order)


@router.get("/orders/", response_model=list[Order])
def get_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return services.get_products(db, skip=skip, limit=limit)


@router.get("orders/{order_id}", response_model=Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = services.get_product(db, order_id)
    if db_order is None:
        raise HTTPException(
            status_code=404,
            detail="Заказ {db_order} не найден."
        )
    return db_order


@router.patch("/orders/{order_id}/status", response_model=Order)
def update_order_status(
    order_id: int, status: str,
    db: Session = Depends(get_db)
):
    return services.update_order_status(db, order_id, status)
