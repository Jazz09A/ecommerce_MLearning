from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.base import get_db
from app.models.order import Order, OrderItem 

router = APIRouter()


@router.post("/orders/")
async def create_order(order: Order, db: Session = Depends(get_db)):


    # Crear el pedido
    new_order = Order(
        user_id=order.user_id,
        status=order.status,
        total=order.total,
        date=order.date
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Agregar productos del pedido
    for item in order.items:
        order_item = OrderItem(
            order_id=new_order.order_id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_time=item.price_at_time
        )
        db.add(order_item)
    
    db.commit()
    return {"message": "Order created successfully", "order": new_order}


