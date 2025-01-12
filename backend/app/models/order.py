from pydantic import BaseModel
from typing import List

class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price_at_time: float

class Order(BaseModel):
    order_id: int
    user_id: int
    date: str
    status: str
    total: float
    items: List[OrderItem] 