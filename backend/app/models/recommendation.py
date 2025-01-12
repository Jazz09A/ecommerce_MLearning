from pydantic import BaseModel

class Recommendation(BaseModel):
    recommendation_id: int
    user_id: int
    product_id: int
    score: float 