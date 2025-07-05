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


TARGET_COLUMN = "Result"
PIPELINENAME = "NetworkSecurity"
ARTIFACT_DIR = "Artifacts"
FILENAME = "Phishing_data.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"