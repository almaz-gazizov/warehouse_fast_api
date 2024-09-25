from sqlalchemy.orm import Session
from fastapi import HTTPException

from app import schemas
from app.models import Product, Order, OrderItem


def create_product(db: Session, product: schemas.ProductCreate):
    """Создает новый продукт в базе данных."""
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: int):
    """Получает продукт по его ID из базы данных."""
    return db.query(Product).filter(
        Product.id == product_id
    ).first()


def get_products(db: Session, skip: int = 0, limit: int = 10):
    """Получает список продуктов с учетом пагинации."""
    return db.query(Product).offset(skip).limit(limit).all()


def update_product(
    db: Session, product_id: int,
    product: schemas.ProductUpdate
):
    """Обновляет информацию о продукте по его ID."""
    db_product = get_product(db, product_id)
    if db_product:
        for key, value in product.model_dump(exclude_unset=True).items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    """Удаляет продукт из базы данных по его ID."""
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product


def create_order(db: Session, order: schemas.OrderCreate):
    """Создает новый заказ в базе данных."""
    db_order = Order(status="в процессе")
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order.items:
        product = get_product(db, item.product_id)
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f'Продукт {item.product_id} не найден'
            )
        if product.quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=(
                    f'На складе недостаточно продукта. '
                    f'Доступно: {product.quantity}. '
                    f'Запрошено: {item.quantity}.'
                )
            )
        product.quantity -= item.quantity
        db.commit()
        db_order_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(db_order_item)

    db.commit()
    return db_order


def get_order(db: Session, order_id: int):
    """Получает заказ по его ID из базы данных."""
    return db.query(Order).filter(Order.id == order_id).first()


def get_orders(db: Session, skip: int = 0, limit: int = 10):
    """Получает список заказов с учетом пагинации."""
    return db.query(Order).offset(skip).limit(limit).all()


def update_order_status(db: Session, order_id: int, status: str):
    """Обновляет статус заказа по его ID."""
    db_order = get_order(db, order_id)
    if db_order:
        db_order.status = status
        db.commit()
        db.refresh(db_order)
    return db_order
