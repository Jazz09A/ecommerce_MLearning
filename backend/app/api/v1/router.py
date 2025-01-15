from fastapi import APIRouter
from app.api.v1.endpoints import cart, products, auth
from app.api.v1.endpoints import interactions
from app.api.v1.endpoints import checkout
from app.api.v1.endpoints import recommendations


api_router = APIRouter()

api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(products.router, prefix="/products", tags=["products"]) 
api_router.include_router(cart.router, prefix="/cart", tags=["cart"])
api_router.include_router(checkout.router, prefix="/checkout", tags=["checkout"])
api_router.include_router(interactions.router, prefix="/interactions", tags=["interactions"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
