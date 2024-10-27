# main.py

from fastapi import FastAPI, HTTPException
from typing import List
from app.models.products import Products
from fastapi import APIRouter, HTTPException, Depends
from database import get_db, db


router = APIRouter()

# In-memory storage for products
products: List[Products] = []

@router.post("/products/", response_model=List[Products])
def add_products(new_products: List[Products]):
    added_products = []
    
    # Convert product names to lowercase for consistency
    products_to_insert = []
    names = []

    for product in new_products:
        lowercased_name = product.name.lower()
        names.append(lowercased_name)
        # Ensure category is included in the insertion
        products_to_insert.append({
            "name": lowercased_name,
            "price": product.price,
            "category": product.category  # Include the category here
        })

    # Check for existing products
    existing_products =  db["products"].find({"name": {"$in": names}}).to_list(None)
    existing_names = {product["name"] for product in existing_products}

    # Raise an error for any product that already exists
    if existing_names:
        raise HTTPException(status_code=400, detail=f"Products with names {', '.join(existing_names)} already exist.")

    # Insert multiple products into the MongoDB collection
    result = db["products"].insert_many(products_to_insert)

    # Retrieve the inserted products with their ObjectIds
    for product_id in result.inserted_ids:
        product = products_to_insert[result.inserted_ids.index(product_id)]
        added_products.append({**product, "id": str(product_id)})  # Append the MongoDB ObjectId as a string

    # Always return a list of added products
    return added_products if added_products else []



@router.get("/productslist/", response_model=List[Products])
async def get_plugins(db=Depends(get_db)):
    collection: Collection = db["products"]
    products = list(collection.find())  # Retrieve all plugins from the collection
    return products if products else []

@router.put("/products/{product_id}", response_model=Products)
def update_product(product_id: int, updated_product: Products):
    for index, product in enumerate(products):
        if product.id == product_id:
            products[index] = updated_product
            return updated_product
            
    raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found.")

@router.delete("/products/{product_id}", response_model=dict)
def delete_product(product_id: int):
    for index, product in enumerate(products):
        if product.id == product_id:
            del products[index]
            return {"detail": f"Product with ID {product_id} deleted."}
            
    raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found.")


    