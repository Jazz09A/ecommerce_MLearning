from app.core.security import get_password_hash

fake_users_db = {
    "alvaro@example.com": {
        "username": "alvaro",
        "email": "alvaro@example.com",
        "hashed_password": get_password_hash("secret123"),
        "disabled": False,
    }
}

products_db = [
    {
        "product_id": 1,
        "name": "Producto 1",
        "category": "Electronics",
        "price": 19.99,
        "stock": 10,
        "image": "https://via.placeholder.com/150",
        "description": "Descripción detallada del Producto 1.",
        "created_at": "2023-10-01T00:00:00"
    },
    {
        "product_id": 2,
        "name": "Producto 2",
        "category": "Home",
        "price": 29.99,
        "stock": 15,
        "image": "https://via.placeholder.com/150",
        "description": "Descripción detallada del Producto 2.",
        "created_at": "2023-10-02T00:00:00"
    },
    {
        "product_id": 3,
        "name": "Producto 3",
        "category": "Garden",
        "price": 39.99,
        "stock": 20,
        "image": "https://via.placeholder.com/150",
        "description": "Descripción detallada del Producto 3.",
        "created_at": "2023-10-03T00:00:00"
    }
]

featured_products = [
    {
        "product_id": 1,
        "name": "Producto Destacado 1",
        "category": "Electronics",
        "price": 19.99,
        "stock": 10,
        "image": "https://via.placeholder.com/150",
        "description": "Descripción corta del Producto Destacado 1",
        "created_at": "2023-10-01T00:00:00"
    },
    {
        "product_id": 2,
        "name": "Producto Destacado 2",
        "category": "Home",
        "price": 29.99,
        "stock": 15,
        "image": "https://via.placeholder.com/150",
        "description": "Descripción corta del Producto Destacado 2",
        "created_at": "2023-10-02T00:00:00"
    },
    {
        "product_id": 3,
        "name": "Producto Destacado 3",
        "category": "Garden",
        "price": 39.99,
        "stock": 20,
        "image": "https://via.placeholder.com/150",
        "description": "Descripción corta del Producto Destacado 3",
        "created_at": "2023-10-03T00:00:00"
    }
] 

orders_db = [
    {
        "order_id": 1,
        "user_id": 1,
        "date": "2023-10-01T00:00:00",
        "status": "pending",
        "total": 19.99,
        "items": [
            {
                "product_id": 1,
                "quantity": 1,
                "price_at_time": 19.99
            }
        ]
    }
]

recommendations_db = [
    {
        "recommendation_id": 1,
        "user_id": 1,
        "product_id": 1,
        "score": 5
    }

]   