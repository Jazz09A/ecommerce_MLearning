# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.models.database_models import Interaction
# from app.schemas.interaction import InteractionCreate
# from app.db.base import get_db

# router = APIRouter()

# @router.post("/interactions/")
# async def create_interaction(interaction: InteractionCreate, db: Session = Depends(get_db)):
#     new_interaction = Interaction(
#         user_id=interaction.user_id,
#         product_id=interaction.product_id,
#         event_type=interaction.event_type,
#         rating=interaction.rating
#     )
#     db.add(new_interaction)
#     db.commit()
#     db.refresh(new_interaction)
#     return {"message": "Interaction recorded successfully", "interaction": new_interaction}
