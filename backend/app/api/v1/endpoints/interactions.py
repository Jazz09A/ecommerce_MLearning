from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
import sqlite3
from datetime import datetime
from app.api.v1.endpoints.auth import get_current_user
from app.models.interaction import Interaction
from app.models.user import User 
router = APIRouter()


@router.post("/interactions/")
async def create_or_update_interaction(interaction: Interaction, current_user: User = Depends(get_current_user)):
    DB_PATH = "db/database.db"
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        # Generar un timestamp en formato UTC
        timestamp = datetime.utcnow().isoformat()

        # Verificar que el usuario tenga un carrito activo
        cursor.execute('''
            SELECT cart_id FROM carts WHERE user_id = ? AND status = 'active'
        ''', (current_user.user_id,))
        active_cart = cursor.fetchone()

        if not active_cart:
            raise HTTPException(status_code=404, detail="No active cart found for user")

        cart_id = active_cart[0]

        # Obtener los productos del carrito activo
        cursor.execute('''
            SELECT ci.product_id FROM cart_items ci WHERE ci.cart_id = ?
        ''', (cart_id,))
        product_ids = cursor.fetchall()

        if not product_ids:
            raise HTTPException(status_code=404, detail="No products found in the cart")

        # Registrar o actualizar la interacción para cada producto
        for (product_id,) in product_ids:
            cursor.execute('''
                SELECT * FROM interactions WHERE user_id = ? AND product_id = ?
            ''', (current_user.user_id, product_id))
            existing_interaction = cursor.fetchone()

            if existing_interaction:
                # Si ya existe la interacción, actualizarla
                cursor.execute('''
                    UPDATE interactions SET event_type = ?, rating = ?, timestamp = ?
                    WHERE user_id = ? AND product_id = ?
                ''', (interaction.event_type, interaction.rating, timestamp, current_user.user_id, product_id))
            else:
                # Si no existe la interacción, insertarla
                cursor.execute('''
                    INSERT INTO interactions (user_id, product_id, event_type, rating, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                ''', (current_user.user_id, product_id, interaction.event_type, interaction.rating, timestamp))

        connection.commit()

        message = {
            "username": current_user.username,
            "status": "success",
            "message": "Interacciones registradas o actualizadas exitosamente",
            "product_ids": [product_id for (product_id,) in product_ids]
        }
        return message

    except Exception as e:
        connection.rollback()  # Deshacer cambios en caso de error
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        connection.close()
