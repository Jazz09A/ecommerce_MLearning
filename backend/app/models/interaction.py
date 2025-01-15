from pydantic import BaseModel

# Definir el modelo de base de datos de interacción (esto es solo para referencia)
class Interaction(BaseModel):
    user_id: int | None = None
    product_id: int
    event_type: str
    timestamp: str | None = None
    rating: int