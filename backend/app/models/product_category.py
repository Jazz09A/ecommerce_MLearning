from pydantic import BaseModel

class ProductCategory(BaseModel):
    product_id: int
    category_id: int 