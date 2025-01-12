from pydantic import BaseModel

class Interaction(BaseModel):
    interaction_id: int
    user_id: int
    product_id: int
    event_type: str
    timestamp: str
    rating: int 