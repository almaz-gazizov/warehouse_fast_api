from typing import List, Optional
from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class OrderStatus(str, Enum):
    in_process = "в процессе"
    sent = "отправлен"
    delivered = "доставлен"


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    in_stock: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[int] = None


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int
    product: Product

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    status: OrderStatus


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class Order(OrderBase):
    id: int
    created_at: datetime
    items: List[OrderItem]

    class Config:
        orm_mode = True
