from pydantic import BaseModel


class BasketResponse(BaseModel):
    basket_id: str
    subtotal: float
