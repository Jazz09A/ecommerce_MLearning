import sqlite3
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.cart import AddToCartRequest, Cart, CartItem
from app.models.product import Product
from pydantic import BaseModel
import stripe
from dotenv import load_dotenv
import os


load_dotenv()

stripe.api_key = os.getenv("Stripe_apikey")


DB_PATH = "db/database.db"

router = APIRouter()


class UpdateQuantityRequest(BaseModel):
    quantity: int


@router.post("/add", response_model=Cart)
async def add_to_cart(request: AddToCartRequest, current_user: User = Depends(get_current_user)):
    print("request: ", request) 
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        # Verificar si el carrito ya existe para el usuario
        cursor.execute("SELECT cart_id FROM carts WHERE user_id = ? AND status = 'active'", (current_user.user_id,))
        cart = cursor.fetchone()

        # Si no existe un carrito activo, crear uno
        if not cart:
            cursor.execute("INSERT INTO carts (user_id, status) VALUES (?, 'active')", (current_user.user_id,))
            connection.commit()
            cart_id = cursor.lastrowid
        else:
            cart_id = cart[0]

        # Buscar el producto
        cursor.execute("SELECT price FROM products WHERE product_id = ?", (request.product_id,))
        product = cursor.fetchone()

        # Si el producto no existe, lanzar una excepción HTTP
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        # Agregar el producto al carrito
        cursor.execute('''
        INSERT INTO cart_items (cart_id, product_id, quantity, price_at_time)
        VALUES (?, ?, ?, ?)
        ''', (cart_id, request.product_id, request.quantity, product[0]))
        connection.commit()

        # Obtener el carrito actualizado
        cursor.execute("SELECT * FROM carts WHERE cart_id = ?", (cart_id,))
        cart_data = cursor.fetchone()

        cursor.execute("SELECT * FROM cart_items WHERE cart_id = ?", (cart_id,))
        items_data = cursor.fetchall()
        print("items_data: ", items_data)
        items = [CartItem(cart_item_id=item[0], cart_id=item[1], product_id=item[2], quantity=item[3], price_at_time=item[4]) for item in items_data]

        return Cart(cart_id=cart_data[0], user_id=cart_data[1], created_at=cart_data[2], status=cart_data[3], items=items)

    finally:
        connection.close()


@router.get("/", response_model=List[CartItem])
async def get_cart(current_user: User = Depends(get_current_user)):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()


    # Obtener el carrito activo para el usuario
    cursor.execute("SELECT cart_id FROM carts WHERE user_id = ? AND status = 'active'", (current_user.user_id,))
    cart = cursor.fetchone()

    if not cart:
        return []

    # Obtener los items del carrito
    cursor.execute("SELECT * FROM cart_items WHERE cart_id = ?", (cart[0],))
    cart_items = cursor.fetchall()

    connection.close()
    return cart_items


@router.get("/carts", response_model=List[Cart])
async def get_carts():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM carts")
        carts_data = cursor.fetchall()

        carts = []
        for cart in carts_data:
            cart_id = cart[0]
            cursor.execute("SELECT * FROM cart_items WHERE cart_id = ?", (cart_id,))
            items_data = cursor.fetchall()
            items = [CartItem(cart_item_id=item[0], cart_id=item[1], product_id=item[2], quantity=item[3], price_at_time=item[4]) for item in items_data]
            carts.append(Cart(cart_id=cart[0], user_id=cart[1], created_at=cart[2], status=cart[3], items=items))

        return carts

    finally:
        connection.close()
    

@router.delete("/{cart_id}", response_model=None)
async def delete_cart(cart_id: int):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        # Verificar si el carrito existe antes de eliminarlo
        cursor.execute("SELECT * FROM carts WHERE cart_id = ?", (cart_id,))
        cart = cursor.fetchone()

        if not cart:
            raise HTTPException(status_code=404, detail="Carrito no encontrado")

        # Eliminar el carrito
        cursor.execute("DELETE FROM carts WHERE cart_id = ?", (cart_id,))
        connection.commit()

        return {"message": "Carrito eliminado exitosamente"}

    finally:
        connection.close()


@router.delete("/{cart_id}/items/{cart_item_id}", response_model=None)
async def delete_item_from_cart(cart_id: int, cart_item_id: int):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        # Verificar si el item existe antes de intentar eliminarlo
        cursor.execute("SELECT * FROM cart_items WHERE cart_id = ? AND cart_item_id = ?", (cart_id, cart_item_id))
        item = cursor.fetchone()

        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado en el carrito")

        # Eliminar el item del carrito
        cursor.execute("DELETE FROM cart_items WHERE cart_id = ? AND cart_item_id = ?", (cart_id, cart_item_id))
        connection.commit()

        return {"message": "Item eliminado exitosamente"}

    finally:
        connection.close()


@router.post("/checkout")
async def checkout(current_user: User = Depends(get_current_user)):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    # Obtener carrito del usuario
    cursor.execute('''SELECT cart_id FROM carts WHERE user_id = ? AND status = 'active' ''', (current_user.user_id,))
    cart = cursor.fetchone()

    if not cart:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")

    # Calcular total del carrito
    cursor.execute('''SELECT SUM(price_at_time * quantity) FROM cart_items WHERE cart_id = ?''', (cart[0],))
    subtotal = cursor.fetchone()[0]
    
    # Agregar costo de envío
    shipping = 5.99
    total = subtotal + shipping

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(total * 100),  # Stripe espera el monto en centavos
            currency='usd',
            metadata={
                'integration_check': 'accept_a_payment',
                'shipping_cost': shipping
            },
        )

        connection.close()

        return {
            "client_secret": payment_intent.client_secret,
            "subtotal": subtotal,
            "shipping": shipping,
            "total": total
        }

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/cart_by_user_id", response_model=Cart)
async def get_cart_by_user_id(current_user: User = Depends(get_current_user)):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute('''SELECT cart_id FROM carts WHERE user_id = ? AND status = 'active' ''', (current_user.user_id,))
    cart = cursor.fetchone()

    if not cart:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")

    cursor.execute('''SELECT ci.product_id, ci.quantity, ci.price_at_time, p.name, p.description, p.price
                     FROM cart_items ci
                     JOIN products p ON ci.product_id = p.product_id
                     WHERE ci.cart_id = ?''', (cart[0],))
    cart_items = cursor.fetchall()

    items = []
    for item in cart_items:
        items.append(CartItem(product_id=item[0], quantity=item[1], price_at_time=item[2]))

    cursor.execute("SELECT created_at, status FROM carts WHERE cart_id = ?", (cart[0],))
    cart_info = cursor.fetchone()

    cart_model = Cart(cart_id=cart[0], user_id=current_user.user_id, created_at=cart_info[0], status=cart_info[1], items=items)

    if cart_model:
        return cart_model
    else:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")


@router.put("/items/{cart_item_id}/update", response_model=None)
async def update_item_quantity(request: UpdateQuantityRequest, cart_item_id: int):
    print(request.quantity, cart_item_id)
    if request.quantity < 0:
        raise HTTPException(status_code=400, detail="La cantidad no puede ser menor que 0")

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute('''UPDATE cart_items SET quantity = ? WHERE product_id = ?''', (request.quantity, cart_item_id))
        connection.commit()  # Asegúrate de que esta línea esté siendo ejecutada
        print(f"Updated cart_item_id={cart_item_id} to quantity={request.quantity}")
    except Exception as e:
        connection.rollback()  # Si hay un error, revertimos la transacción
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        connection.close()
    
    return {"message": "Cantidad actualizada exitosamente"}

