from fastapi import APIRouter
from app.api.v1.endpoints import products, auth

api_router = APIRouter()

api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(products.router, prefix="/products", tags=["products"]) 