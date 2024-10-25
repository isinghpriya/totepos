# main.py

from fastapi import FastAPI, HTTPException
from typing import List
from app.models.products import Products
from fastapi import APIRouter, HTTPException, Depends


router = APIRouter()

# In-memory storage for products
products: List[Products] = []

@router.post("/products/", response_model=List[Products])
def add_products(new_products: List[Products]):
    added_products = []
    
    for product in new_products:
        # Check if the product already exists
        for p in products:
            if p.id == product.id:
                raise HTTPException(status_code=400, detail=f"Product with ID {product.id} already exists.")
        
        products.append(product)
        added_products.append(product)
    
    return added_products

@router.get("/products/", response_model=List[Products])
def get_products():
    return products


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


    