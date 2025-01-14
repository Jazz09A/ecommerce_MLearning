from typing import Optional
from pydantic import BaseModel

class Product(BaseModel):
    product_id: Optional[int] = None
    name: str
    category: str
    price: float
    stock: int
    image: str
    description: str
    created_at: Optional[str] = None
