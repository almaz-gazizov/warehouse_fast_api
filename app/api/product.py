from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import services
from app.database import get_db
from app.schemas import Product, ProductCreate, ProductUpdate

router = APIRouter()


@router.post("/products/", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return services.create_product(db, product)


@router.get("/products/", response_model=list[Product])
def get_products(
    skip: int = 0, limit: int = 10,
    db: Session = Depends(get_db)
):
    return services.get_products(db, skip=skip, limit=limit)


@router.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = services.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(
            status_code=404,
            detail="Продукт {db_product} не найден."
        )
    return db_product


@router.put("products/{product_id}", response_model=Product)
def update_product(
    product_id: int, product: ProductUpdate,
    db: Session = Depends(get_db)
):
    return services.update_product(db, product_id, product)


@router.delete("products/{product_id}", response_model=Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return services.delete_product(db, product_id)
