
from fastapi import FastAPI
from app.routers import employee

app = FastAPI()

# Include routers
app.include_router(employee.router, prefix="/employee")
# app.include_router(basket.router, prefix="/basket")
# app.include_router(payment.router, prefix="/payment")

@app.get("/")
async def root():
    return {"message": "Welcome to the POS System"}
