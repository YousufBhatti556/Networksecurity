from networksecurity.components.data_validation import DataValidation
from networksecurity.components.dataingestion import Data_ingestion
from networksecurity.components.datatransformation import Data_Transformation
from networksecurity.components.model_training import Model_Training
from networksecurity.entity.config_entity import DataIngestionConfig, DataTransformationConfig, DataValidationConfig, ModelTrainerConfig, TrainingPipelineConfig
from networksecurity.entity.artifact_entity import Data_Ingestion_Artifact, Data_Transformation_Artifacts, Data_Validation_Artifact, Model_Trainer_Artifacts, ClassificationMetricArtifact
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from networksecurity.logging.logger import logging
from networksecurity.constants.training_pipeline import TRAINING_BUCKET_NAME
from networksecurity.exeptionhandling.exception_handling import NetworkSecurityException
import sys, os
from networksecurity.cloud.syncer import S3Sync
class Training_Pipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.s3_sync = S3Sync()
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)
            logging.info("Start data ingestion")
            data_ingestion = Data_ingestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed.")
            logging.info(f"Data ingestion artifacts {data_ingestion_artifacts}")
            return data_ingestion_artifacts
        except Exception as e:
            logging.info(NetworkSecurityException(e, sys))
            raise NetworkSecurityException(e, sys)
        
    def start_data_validation(self, data_ingestion_artifacts):
        try:
            self.data_validation_config = DataValidationConfig(trainingpipelineconfig=self.training_pipeline_config)
            logging.info("Data validation started")
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifacts, data_validation_config=self.data_validation_config)
            data_validation_artifacts = data_validation.initiate_data_validation()
            logging.info("Data validation completed")
            logging.info(f"Data validation artifacts {data_ingestion_artifacts}")
            return data_validation_artifacts
        except Exception as e:
            logging.info(NetworkSecurityException(e, sys))
            raise NetworkSecurityException(e, sys)
        
    def start_data_transformation(self, data_validation_artifacts):
        try:
            self.data_transformation_config = DataTransformationConfig(trainingpipelineconfig=self.training_pipeline_config)
            logging.info("Data transformation started")
            data_transformation = Data_Transformation(data_transformation_config=self.data_transformation_config, data_validation_artifact=data_validation_artifacts)
            data_transformation_artifacts = data_transformation.initiate_data_transformation()
            logging.info("Data transformation completed")
            logging.info(f"Data transformation artifacts {data_transformation_artifacts}")
            return data_transformation_artifacts
        except Exception as e:
            logging.info(NetworkSecurityException(e, sys))
            raise NetworkSecurityException(e, sys)

    def start_model_training(self, data_transformation_artifacts:Data_Transformation_Artifacts):
        try:
            self.model_training_config = ModelTrainerConfig(trainingpipelineconfig=self.training_pipeline_config)
            model_trainer = Model_Training(data_transformation_artifacts=data_transformation_artifacts, model_trainer_config=self.model_training_config)
            model_training_artifacts = model_trainer.inititae_model_training()
            return model_training_artifacts
        except Exception as e:
            logging.info(NetworkSecurityException(e, sys))
            raise NetworkSecurityException(e, sys)

    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.artifact_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    ## local final model is going to s3 bucket     
        
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.model_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def run_pipeline(self):
        try:
            data_ingestion_artifacts = self.start_data_ingestion()
            data_validation_artifacts = self.start_data_validation(data_ingestion_artifacts=data_ingestion_artifacts)
            data_transformation_artifacts = self.start_data_transformation(data_validation_artifacts=data_validation_artifacts)
            model_trainer_artifacts = self.start_model_training(data_transformation_artifacts=data_transformation_artifacts)
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
            return model_trainer_artifacts
        except Exception as e:
            logging.info(NetworkSecurityException(e, sys))
            raise NetworkSecurityException(e, sys)    
        
