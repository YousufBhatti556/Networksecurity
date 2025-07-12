import os, sys, json
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca = certifi.where()

from networksecurity.exeptionhandling.exception_handling import NetworkSecurityException
from networksecurity.logging.logger import logging
import pandas as pd
import numpy as np
import pymongo


class ExtractNetworkData:
    def __init__(self):
        try:
            pass
        except Exception as e:
            logging.info(NetworkSecurityException(e, sys))
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json(self, file_path):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace=True)
            records = list(json.loads(df.T.to_json()).values())
            return records
        except Exception as e:
            logging.info(NetworkSecurityException(e, sys))
            raise NetworkSecurityException(e, sys)
        
    def insert_data_to_mongo_db(self, database_name, collection_name, data):
        try:
            client = pymongo.MongoClient(MONGO_DB_URL)
            db = client[database_name]
            collection = db[collection_name]
            collection.insert_many(data)
            logging.info("Data inserted into MongoDB")
            return len(data)
        except Exception as e:
            logging.info(NetworkSecurityException(e, sys))
            raise NetworkSecurityException(e, sys)
        

if __name__ == "__main__":
    obj = ExtractNetworkData()
    FILE_PATH = r"NetworkData/phisingData.csv"
    db_name = "yousufbhatti99"
    collection_name = "NETWORKDATA"
    data = obj.csv_to_json(FILE_PATH)
    print(obj.insert_data_to_mongo_db(db_name, collection_name, data))