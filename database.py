
from pymongo import MongoClient
import os

MONGO_URI =  os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["pos-sample"]

def get_db():
    return db
