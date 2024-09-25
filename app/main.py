from fastapi import FastAPI

from app.api import product, order


app = FastAPI()

app.include_router(product.router)
app.include_router(order.router)
