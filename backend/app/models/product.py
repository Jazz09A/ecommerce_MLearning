from pydantic import BaseModel

class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: float
    stock: int
    image: str
    description: str
    created_at: str
