# app/models.py

from pydantic import BaseModel

class Employee(BaseModel):
    username: str
    hashed_password: str
    name: str
    role: str
    is_logged_in: bool = False