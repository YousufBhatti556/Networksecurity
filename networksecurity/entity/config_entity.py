import os 
import sys
from networksecurity.constants import training_pipeline
from datetime import datetime

class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        self.timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name = training_pipeline.PIPELINENAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name, self.timestamp)
        

class DataIngestionConfig:
    def __init__(self, trainingpipelineconfig: TrainingPipelineConfig):
        self.data_ingestion_dir = os.path.join(trainingpipelineconfig.artifact_dir,
                                               training_pipeline.DATA_INGESTION_DIR_NAME)
        self.feature_store_file_path = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, training_pipeline.FILENAME)
        self.training_file_path = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_STORE, training_pipeline.TRAIN_FILE_NAME)
        self.test_file_path = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_STORE, training_pipeline.TEST_FILE_NAME)
        self.train_test_split_ratio = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name = training_pipeline.DATA_INGESTION_DATABASE_NAME        
        

class DataValidationConfig:
    def __init__(self, trainingpipelineconfig: TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(trainingpipelineconfig.artifact_dir, training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.valid_data_path = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_path = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.train_valid_data_path = os.path.join(self.valid_data_path, training_pipeline.TRAIN_FILE_NAME)
        self.test_valid_data_path = os.path.join(self.valid_data_path, training_pipeline.TEST_FILE_NAME)
        self.train_invalid_data_path = os.path.join(self.invalid_data_path, training_pipeline.TRAIN_FILE_NAME)
        self.test_invalid_data_path = os.path.join(self.invalid_data_path, training_pipeline.TEST_FILE_NAME)
        
        self.drift_report_path = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR, training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR)
        