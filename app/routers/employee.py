# app/routers/employee.py

from fastapi import APIRouter, HTTPException, Depends
from pymongo.collection import Collection
from typing import List
from app.models.employee import Employee
from database import get_db, db
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from app.utils import hash_password, verify_password


router = APIRouter()

@router.post("/employee/register")
async def register_employee(username: str, password: str, name: str, role: str):
    # Check if the username already exists
    if db["employees"].find_one({"username": username}):
        raise HTTPException(status_code=400, detail="Username already taken")

    # Hash the password
    hashed_password = hash_password(password)

    # Create employee data
    employee_data = {
        "username": username,
        "hashed_password": hashed_password,
        "name": name,
        "role": role,
        "is_logged_in": False
    }

    # Save to database
    result = db["employees"].insert_one(employee_data)
    return {"message": "Employee registered successfully", "employee_id": str(result.inserted_id)}

@router.get("/employees/", response_model=List[Employee])
async def get_employees(db=Depends(get_db)):
    collection: Collection = db["employees"]
    employees = list(collection.find())  # Retrieve all employees from the collection

    # Convert ObjectId back to string for the response and ensure it's included
    for employee in employees:
        employee["id"] = str(employee["_id"])  # Convert _id to id for the response
        del employee["_id"]  # Optionally delete _id to avoid sending it in the response

    return employees

@router.get("/employees/{employee_id}", response_model=Employee)
async def get_employee(employee_id: str, db=Depends(get_db)):
    collection: Collection = db["employees"]

    try:
        emp_id = ObjectId(employee_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")

    employee = collection.find_one({"_id": emp_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee["id"] = str(employee["_id"])  # Convert _id to id for the response
    del employee["_id"]  # Optionally delete _id to avoid sending it in the response
    return employee

@router.put("/employees/{employee_id}", response_model=Employee)
async def update_employee(employee_id: str, employee: Employee, db=Depends(get_db)):
    collection: Collection = db["employees"]

    try:
        emp_id = ObjectId(employee_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")

    # Convert the employee Pydantic model to a dictionary and remove 'id'
    update_data = jsonable_encoder(employee)
    update_data.pop("id", None)  # Remove 'id' field from the update data if present

    result = collection.update_one({"_id": emp_id}, {"$set": update_data})

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found or no changes made")

    # Return the updated employee
    updated_employee = collection.find_one({"_id": emp_id})
    updated_employee["id"] = str(updated_employee["_id"])  # Convert _id to id for the response
    del updated_employee["_id"]  # Optionally delete _id
    return updated_employee

@router.delete("/employees/{employee_id}", response_model=dict)
async def delete_employee(employee_id: str, db=Depends(get_db)):
    collection: Collection = db["employees"]

    try:
        emp_id = ObjectId(employee_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")

    result = collection.delete_one({"_id": emp_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")

    return {"message": "Employee deleted successfully"}

@router.post("/employee/login")
async def login(username: str, password: str):
    employee = db["employees"].find_one({"username": username})
    if not employee or not verify_password(password, employee["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    db["employees"].update_one({"_id": employee["_id"]}, {"$set": {"is_logged_in": True}})
    return {"message": "Login successful", "employee_id": str(employee["_id"])}

@router.post("/employee/logout")
async def logout(employee_id: str):
    # Verify if the employee exists and is logged in
    employee = db["employees"].find_one({"_id": ObjectId(employee_id)})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    if not employee.get("is_logged_in", False):
        raise HTTPException(status_code=400, detail="Employee is already logged out")

    # Update the employee's login status to False
    db["employees"].update_one({"_id": employee["_id"]}, {"$set": {"is_logged_in": False}})
    return {"message": "Logout successful"}














