from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
import sqlite3
from datetime import datetime
from app.api.v1.endpoints.auth import get_current_user
from app.models.interaction import Interaction
from app.models.user import User 
router = APIRouter()


@router.post("/interactions/")
async def create_interaction(interaction: Interaction, current_user: User = Depends(get_current_user)):
    DB_PATH = "db/database.db"
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        # # Generar un timestamp en formato UTC
        # timestamp = datetime.utcnow().isoformat()

        # # Insertar la interacción en la base de datos
        # cursor.execute('''
        #     INSERT INTO interactions (user_id, product_id, event_type, rating, timestamp)
        #     VALUES (?, ?, ?, ?, ?)
        # ''', (current_user.id, interaction.product_id, interaction.event_type, interaction.rating, timestamp))

        # connection.commit()
        # connection.close()

        message = {"username": current_user, "status": "success", "message": "Interacción registrada exitosamente", "interaction": interaction.model_dump()}
        print(message)
        return message

    except Exception as e:
        connection.rollback()  # Deshacer cambios en caso de error
        connection.close()
        raise HTTPException(status_code=400, detail=str(e))
