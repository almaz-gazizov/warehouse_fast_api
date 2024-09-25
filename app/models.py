from datetime import datetime
from enum import Enum

import pytz
from sqlalchemy import (
    Column, DateTime, Enum as SQLAlchemyEnum,
    Float, ForeignKey, Integer, String
)
from sqlalchemy.orm import relationship

from .database import Base


class OrderStatus(str, Enum):
    in_process = "in_process"
    sent = "sent"
    delivered = "delivered"

    @classmethod
    def to_russian(cls, status):
        translations = {
            "in_process": "в процессе",
            "sent": "отправлен",
            "delivered": "доставлен"
        }
        return translations.get(status, status)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    in_stock = Column(Integer)


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(
        DateTime, default=datetime.now(pytz.timezone('Europe/Moscow'))
    )
    status = Column(
        SQLAlchemyEnum(OrderStatus), default=OrderStatus.in_process
    )
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    order = relationship("Order", back_populates="items")
    product = relationship("Product")
