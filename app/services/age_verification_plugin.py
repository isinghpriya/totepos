from app.models.plugins import Plugin
from database import get_db, db
from typing import List

# Age verification function
def requires_age_verification(item):
    age_restricted_categories = ['alcohol', 'tobacco', 'fireworks'] # Data will be taken from DB in future
    existing_plugin = db["plugins"].find_one({"name": "Age Verification"})
    if existing_plugin and existing_plugin.get("active") == True:
        # customer data can be taken from some db or any other resource and we can check if age is greater than 18 or not
        return item.get('category') in age_restricted_categories