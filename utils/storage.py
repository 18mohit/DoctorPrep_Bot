import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "SHOTOKAN"
COLLECTION_NAME = "DoctorPrep"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def load_users():
    users = {}
    for user in collection.find():
        users[user["_id"]] = user
    return users

def save_users(users):
    collection.delete_many({})
    docs = []
    for uid, udata in users.items():
        user = udata.copy()
        user["_id"] = uid
        docs.append(user)
    if docs:
        collection.insert_many(docs)











# import json
# import os
# from config import USERS_FILE

# def load_users():
#     if os.path.exists(USERS_FILE):
#         with open(USERS_FILE, "r") as f:
#             return json.load(f)
#     return {}

# def save_users(users):
#     with open(USERS_FILE, "w") as f:
#         json.dump(users, f, indent=2)
