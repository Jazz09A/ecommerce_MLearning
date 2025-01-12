from pydantic import BaseModel
from typing import List

class CartItem(BaseModel):
    cart_item_id: int
    cart_id: int
    product_id: int
    quantity: int
    price_at_time: float

class Cart(BaseModel):
    cart_id: int
    user_id: int
    created_at: str
    status: str
    items: List[CartItem] 