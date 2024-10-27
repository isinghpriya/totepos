from fastapi import APIRouter, HTTPException, Depends
from pymongo.collection import Collection
from typing import List, Dict
from app.models.baskets import BasketResponse
from database import get_db, db
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from app.models.payment import PaymentDetails
from database import get_db, db
from datetime import datetime

baskets = {
    "basket_1": {"items": [{"name": "apple", "price": 2.5}], "subtotal": 2.5, "paid": False} #it will be taken from DB for now it is static
}
router = APIRouter()
@router.post("/complete_payment/{basket_id}")
async def complete_payment(basket_id: str, payment: PaymentDetails):
    # Check if the basket exists
    if basket_id not in baskets:
        raise HTTPException(status_code=404, detail="Basket not found")
    
    basket = baskets[basket_id]
    
    # Check if the basket has already been paid for
    if basket.get("paid"):
        raise HTTPException(status_code=400, detail="Payment already completed for this basket")
    
    # Check if the amount paid is sufficient
    if payment.amount_paid < basket["subtotal"]:
        raise HTTPException(status_code=400, detail="Insufficient payment amount")
    
    # Mark the basket as paid and add a payment timestamp
    basket["paid"] = True
    basket["payment_method"] = payment.payment_method
    basket["amount_paid"] = payment.amount_paid
    basket["payment_timestamp"] = datetime.now()
    
    # Generate a receipt (for demonstration)
    receipt = {
        "basket_id": basket_id,
        "items": basket["items"],
        "subtotal": basket["subtotal"],
        "payment_method": basket["payment_method"],
        "amount_paid": basket["amount_paid"],
        "payment_timestamp": basket["payment_timestamp"],
        "status": "Payment successful"
    }
    
    return receipt

