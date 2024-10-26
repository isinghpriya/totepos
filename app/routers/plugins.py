from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from app.models.plugins import Plugin
from database import get_db, db
from typing import List

from fastapi import APIRouter, HTTPException, Depends

router = APIRouter()

# Sample plugins data


@router.post('/register_plugin', response_model=Plugin)
async def register_plugin(name: str, active: bool,):
    """Register a new plugin by name."""
    if not name:
        raise HTTPException(status_code=400, detail="Plugin name is required")

    # Check if the plugin already exists
    existing_plugin = db["plugins"].find_one({"name": name})
    if existing_plugin:
        raise HTTPException(status_code=400, detail="Plugin already exists")

    # Register the new plugin
    new_plugin = {"name": name, "active": True}
    result = db["plugins"].insert_one(new_plugin)
    new_plugin["_id"] = str(result.inserted_id)  
    return JSONResponse(content=new_plugin)


@router.get("/plugins/", response_model=List[Plugin])
async def get_plugins(db=Depends(get_db)):
    collection: Collection = db["plugins"]
    plugins = list(collection.find())  # Retrieve all plugins from the collection
    return plugins


