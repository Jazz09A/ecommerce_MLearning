from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.ml.recommendation_engine import recommend_products
import sqlite3

DB_PATH = "C:/Users/yuher/OneDrive/Escritorio/proyecto-ecommerce/backend/db/database.db"

router = APIRouter()

@router.get("/recommended-products")
async def get_recommended_products(current_user: User = Depends(get_current_user)):
    """Obtener los productos recomendados para un usuario."""
    try:
        # Obtener los IDs de productos recomendados
        recommended_product_ids = recommend_products(current_user.user_id)
        print("recommended_product_ids", recommended_product_ids)

        # Conectar a la base de datos
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # Obtener detalles de los productos recomendados
        query = '''
        SELECT product_id, name, category, price, stock, image, description
        FROM products
        WHERE product_id IN ({})
        '''.format(','.join('?' for _ in recommended_product_ids))

        cursor.execute(query, recommended_product_ids)
        products = cursor.fetchall()

        # Convertir los resultados a una lista de diccionarios
        product_list = [
            {
                "product_id": product[0],
                "name": product[1],
                "category": product[2],
                "price": product[3],
                "stock": product[4],
                "image": product[5],
                "description": product[6]
            }
            for product in products
        ]

        connection.close()

        print("recommended_products to frontend", product_list)
        return {"recommended_products": product_list}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
