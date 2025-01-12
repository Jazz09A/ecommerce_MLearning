from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.models.product import Product
from app.models.recommendation import Recommendation
from app.db.fake_db import products_db, featured_products, recommendations_db

router = APIRouter()

@router.get("/")
async def get_products():
    products = [Product(**product) for product in products_db]
    if not products:
        raise HTTPException(status_code=404, detail="Products not found")
    return products

@router.get("/featured", response_model=List[Product])
async def get_featured_products():
    featured = [Product(**product) for product in featured_products]
    if not featured:
        raise HTTPException(status_code=404, detail="Featured products not found")
    return featured

@router.get("/recommendations", response_model=List[Recommendation])
async def get_recommendations(user_id: int = Query(..., description="The ID of the user to get recommendations for")):
    recommendations = [r for r in recommendations_db if r["user_id"] == user_id]
    if not recommendations:
        raise HTTPException(status_code=404, detail="Recommendations not found")
    return recommendations

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int):
    product = next((p for p in products_db if p["product_id"] == product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**product)
