from pydantic import BaseModel

class Products(BaseModel):
    name: str
    description: str = None
    price: float
    category: str
