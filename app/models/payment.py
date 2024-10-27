from pydantic import BaseModel

class PaymentDetails(BaseModel):
    payment_method: str  # e.g., "credit_card", "cash"
    amount_paid: float   # amount paid by the customer
