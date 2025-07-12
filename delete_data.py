from dotenv import load_dotenv
import os, sys
import certifi
ca = certifi.where()

from networksecurity.exeptionhandling.exception_handling import NetworkSecurityException
from networksecurity.logging.logger import logging
import pandas as pd
import numpy as np
import pymongo
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

client = pymongo.MongoClient(MONGO_DB_URL)  # change URI if using MongoDB Atlas

# Step 2: Choose your database and collection
db = client["yousufbhatti99"]
collection = db["NETWORKDATA"]

# Step 3: Delete all documents in the collection
delete_result = collection.delete_many({})  # {} means delete everything

print(f"Deleted {delete_result.deleted_count} documents.")