from fastapi import APIRouter
from app.api.v1.endpoints import cart, checkout, products, auth


api_router = APIRouter()

api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(products.router, prefix="/products", tags=["products"]) 
api_router.include_router(cart.router, prefix="/cart", tags=["cart"])
api_router.include_router(checkout.router, prefix="/checkout", tags=["checkout"])
