import sqlite3
from pydantic import BaseModel
import stripe
from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.endpoints.auth import get_current_user
from app.core.config import settings
from app.models.user import User


class PaymentRequest(BaseModel):
    id: str
    token: str

stripe.api_key = settings.STRIPE_API_KEY
DB_PATH = 'db/database.db'
router = APIRouter()
    
@router.post("/confirm-payment")
async def confirm_payment(payment_request: PaymentRequest, current_user: User = Depends(get_current_user)):
    print(f"Received payment request: {payment_request}")

    payment_intent_id = payment_request.id
    print(f"Payment Intent ID: {payment_intent_id}")



    try:
        # Retrieve the PaymentIntent to check its status
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        print(f"Current Payment Intent Status: {payment_intent.status}")

        if payment_intent.status == 'succeeded':
            print("Payment already succeeded, proceeding to create order.")
        else:
            # Confirm the payment if it hasn't succeeded yet
            payment_intent = stripe.PaymentIntent.confirm(payment_intent_id)
            print(f"Payment Intent Status after confirmation: {payment_intent.status}")

            if payment_intent.status != 'succeeded':
                raise HTTPException(status_code=400, detail="El pago no fue exitoso")

        # Get the cart_id from the database (because it's not in the User model)
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # Get the cart_id from the user's active cart
        cursor.execute('''SELECT cart_id FROM carts WHERE user_id = ? AND status = 'active' LIMIT 1''', (current_user.user_id,))
        cart_row = cursor.fetchone()

        if not cart_row:
            raise HTTPException(status_code=400, detail="No active cart found for the user.")

        cart_id = cart_row[0]
        print(f"Active cart_id found for user {current_user.user_id}: {cart_id}")

        # Get the total from the cart
        cursor.execute('''SELECT SUM(price_at_time * quantity) FROM cart_items WHERE cart_id = ?''', (cart_id,))
        total = round(cursor.fetchone()[0], 2)
        print(f"Total amount for cart {cart_id}: {total}")

        # Insert the order into the database
        cursor.execute('''INSERT INTO orders (user_id, total, status) VALUES (?, ?, 'completed')''', (current_user.user_id, total))
        order_id = cursor.lastrowid
        print(f"Order ID {order_id} created for user {current_user.user_id}")

        # Relate the products with the order
        cursor.execute('''INSERT INTO order_items (order_id, product_id, quantity, price_at_time)
                          SELECT ?, product_id, quantity, price_at_time FROM cart_items WHERE cart_id = ?''', 
                       (order_id, cart_id))
        connection.commit()
        print(f"Order items for order ID {order_id} have been inserted.")

        # Update the cart to "processed"
        cursor.execute('''UPDATE carts SET status = 'processed' WHERE cart_id = ?''', (cart_id,))
        connection.commit()
        print(f"Cart {cart_id} status updated to 'processed'.")

        connection.close()
        print("Database connection closed.")

        return {"message": "Pago y orden confirmados exitosamente", "order_id": order_id}
    except stripe.error.StripeError as e:
        print(f"Stripe error during payment confirmation: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

