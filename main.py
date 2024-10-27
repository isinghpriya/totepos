
from fastapi import FastAPI
from app.routers import employee,products,plugins, basket

app = FastAPI()

# Include routers
app.include_router(employee.router, prefix="/employee")
app.include_router(products.router, prefix="/products")
app.include_router(plugins.router, prefix="/plugins")
app.include_router(basket.router, prefix="/basket")

@app.get("/")
async def root():
    return {"message": "Welcome to the POS System"}
