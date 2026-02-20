from pydantic import BaseModel
from datetime import datetime


class Order(BaseModel):
    """Single order response model."""

    order_id: str
    customer_name: str
    email: str
    product: str
    price: float
    quantity: int
    city: str
    status: str
    order_time: str


class SalesPerCity(BaseModel):
    """Sales summary per city."""

    city: str
    total_sales: float
