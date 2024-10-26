from pydantic import BaseModel

class Plugin(BaseModel):
    name: str
    active: bool