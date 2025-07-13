import os
import sys
import pandas as pd
import numpy as np


DATA_INGESTION_COLLECTION_NAME = "NETWORKDATA"
DATA_INGESTION_DATABASE_NAME = "yousufbhatti99"
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR = "featue_store"
DATA_INGESTION_INGESTED_STORE = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = 0.2

SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

DATA_VALIDATION_DIR_NAME = "data_validation"
DATA_VALIDATION_VALID_DIR = "valid"
DATA_VALIDATION_INVALID_DIR = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR = "drift_report" 
DATA_VALIDATION_DRIFT_REPORT_NAME = "report.yaml" 

DATA_TRANSFORMATION_DIR_NAME = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR_NAME = "data_transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR_NAME = 'object_transformed'
DATA_TRANSFORMATION_PREPROCESSING_OBJ_FILE_NAME = "preprocessor.pkl"
DATA_TRANSFORMATION_IMPUTER_PARAMS:dict = {
    "missing_values":np.nan,
    "n_neighbors":3,
    "weights":"uniform"
}


TARGET_COLUMN = "Result"
PIPELINENAME = "NetworkSecurity"
ARTIFACT_DIR = "Artifacts"
FILENAME = "Phishing_data.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"