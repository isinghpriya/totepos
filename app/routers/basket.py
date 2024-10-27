from fastapi import APIRouter, HTTPException, Depends
from pymongo.collection import Collection
from typing import List, Dict
from app.models.baskets import BasketResponse
from database import get_db, db
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from app.models.products import Products
from database import get_db, db

router = APIRouter()

baskets: Dict[str, Dict] = {}  # Declare the baskets dictionary globally



@router.post("/start_basket", response_model=BasketResponse)
async def start_basket():
    basket_id = f'basket_{len(baskets) + 1}'  # Generate a unique basket ID
    baskets[basket_id] = {"items": [], "subtotal": 0.0}  # Initialize the basket
    return {"basket_id": basket_id, "subtotal": 0.0}  


@router.post("/add_items_to_basket/{basket_id}")
async def add_items_to_basket(basket_id: str, items: List[Products], db=Depends(get_db)):
    # Check if the basket exists in the in-memory store
    if basket_id not in baskets:
        raise HTTPException(status_code=404, detail="Basket not found")

    # Initialize the list for items that are added successfully
    added_items = []
    
    # Iterate over the list of items and check if each one exists in the MongoDB inventory
    for item in items:
        item_doc =  db["products"].find_one({"name": item.name.lower()})
        
        if not item_doc:
            raise HTTPException(status_code=404, detail=f"Item '{item.name}' not found in inventory")
        
        # Retrieve item details from the MongoDB document
        item_details = {
            "id": str(item_doc["_id"]),  # Ensure ObjectId is converted to a string
            "name": item_doc["name"],
            "price": item_doc["price"],
            "category": item_doc["category"]
        }
        
        # Add the item to the basket and update the subtotal
        baskets[basket_id]["items"].append(item_details)
        baskets[basket_id]["subtotal"] += item_details["price"]
        added_items.append(item_details)  # Track successfully added items

    return {
        "message": "Items added to basket",
        "basket_id": basket_id,
        "subtotal": baskets[basket_id]["subtotal"],
        "items": baskets[basket_id]["items"]
    }


