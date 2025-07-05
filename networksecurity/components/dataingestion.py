from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from networksecurity.exeptionhandling.exception_handling import NetworkSecurityException
from networksecurity.logging.logger import logging
import pandas as pd
import numpy as np
import os, sys
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class Data_ingestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            logging.info(NetworkSecurityException(e, sys))
            raise NetworkSecurityException(e, sys)
        
    def get_dataframe_from_collection(self):
        try:
            db_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[db_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns().to_list():
                df.drop(columns="_id", axis=1, inplace=True)
            df.replace({"na":np.nan})
            return df
        except Exception as e:
            logging.info(NetworkSecurityException(e,sys))
            raise NetworkSecurityException(e,sys)
    
    def export_collection_to_csv(self, df: pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            df.to_csv(feature_store_file_path, index=False, header=True)
            return df
        except Exception as e:
            logging.info(NetworkSecurityException(e,sys))
            raise NetworkSecurityException(e,sys)

    def split_data_as_train_test(self, df: pd.DataFrame):
        try:
            logging.info("Spliiting the data as train and test set started")
            train_data, test_data = train_test_split(df, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42)
            logging.info("Spliiting the data as train and test set ended")

            logging.info("Exporting train and test file path")
            train_data.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_data.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)
            logging.info("Exported train and test file path")


        except Exception as e:
            logging.info(NetworkSecurityException(e,sys))
            raise NetworkSecurityException(e,sys)

    def initiate_data_ingestion(self):
        try:
            logging.info("Started data ingestion")
            df = self.get_dataframe_from_collection()
            df = self.export_collection_to_csv(df)
            self.split_data_as_train_test(df)
            
        except Exception as e:
            logging.info(NetworkSecurityException(e,sys))
            raise NetworkSecurityException(e,sys)