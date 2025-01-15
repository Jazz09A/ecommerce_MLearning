import sqlite3
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.product import Product
from app.models.recommendation import Recommendation

DB_PATH = "db/database.db"

router = APIRouter()
@router.get("/", response_model=list[Product])
async def get_products():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    connection.close()

    # Map each tuple to a dictionary
    product_list = []
    for product in products:
        product_dict = {
            "product_id": product[0],
            "name": product[1],
            "category": product[2],
            "price": product[3],
            "stock": product[4],
            "image": product[5],
            "description": product[6],
            "created_at": product[7]
        }
        product_list.append(Product(**product_dict))
    if not product_list:
        raise HTTPException(status_code=404, detail="Products not found")
    return product_list

@router.get("/featured", response_model=List[Product])
async def get_featured_products():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products WHERE featured = 1")
    featured_products = cursor.fetchall()
    featured = [Product(**product) for product in featured_products]
    if not featured:
        raise HTTPException(status_code=404, detail="Featured products not found")
    return featured


@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
    product = cursor.fetchone()
    connection.close()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(
        product_id=product[0],
        name=product[1],
        category=product[2],
        price=product[3],
        stock=product[4],
        image=product[5],
        description=product[6],
        created_at=product[7]
    )

# @router.get("/recommendations", response_model=List[Recommendation])
# async def get_recommendations(user_id: int = Query(..., description="The ID of the user to get recommendations for")):
#     recommendations = [r for r in recommendations_db if r["user_id"] == user_id]
#     if not recommendations:
#         raise HTTPException(status_code=404, detail="Recommendations not found")
#     return recommendations


@router.post("/", response_model=Product)
async def add_product(product: Product):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO products (name, category, price, stock, image, description) VALUES (?, ?, ?, ?, ?, ?)",
        (product.name, product.category, product.price, product.stock, product.image, product.description)
    )
    connection.commit()
    cursor.execute("SELECT * FROM products WHERE product_id = ?", (cursor.lastrowid,))
    new_product = cursor.fetchone()
    connection.close()

    if not new_product:
        raise HTTPException(status_code=500, detail="Failed to add product")

    return Product(
        product_id=new_product[0],
        name=new_product[1],
        category=new_product[2],
        price=new_product[3],
        stock=new_product[4],
        image=new_product[5],
        description=new_product[6],
        created_at=new_product[7]
    )

@router.put("/{product_id}", response_model=Product)
async def update_product(product_id: int, product: Product):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE products SET name = ?, category = ?, price = ?, stock = ?, image = ?, description = ? WHERE product_id = ?",
        (product.name, product.category, product.price, product.stock, product.image, product.description, product_id)
    )
    connection.commit()

    cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
    updated_product = cursor.fetchone()
    connection.close()

    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Map the tuple to a dictionary
    product_dict = {
        "product_id": updated_product[0],
        "name": updated_product[1],
        "category": updated_product[2],
        "price": updated_product[3],
        "stock": updated_product[4],
        "image": updated_product[5],
        "description": updated_product[6],
        "created_at": updated_product[7]
    }
    print(product_dict)
    return Product(**product_dict)

@router.delete("/{product_id}", response_model=dict)
async def delete_product(product_id: int):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
    connection.commit()
    connection.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted successfully"}


@router.get("/recommendations/{user_id}", response_model=List[Recommendation])
async def get_recommendations(user_id: int):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute('SELECT product_id, score FROM recommendations WHERE user_id = ?', (user_id,))
    recommendations = cursor.fetchall()

    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendations found")

    return [Recommendation(product_id=r[0], score=r[1]) for r in recommendations]