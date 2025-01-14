from pydantic import BaseModel
from typing import List, Optional

class CartItem(BaseModel):
    product_id: int
    quantity: int
    price_at_time: float

class Cart(BaseModel):
    cart_id: int
    user_id: int
    created_at: Optional[str] = None
    status: str
    items: List[CartItem] 
    
class AddToCartRequest(BaseModel):
    product_id: int
    quantity: int