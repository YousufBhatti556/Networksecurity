from networksecurity.exeptionhandling.exception_handling import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig
from networksecurity.entity.artifact_entity import Data_Ingestion_Artifact, Data_Validation_Artifact
from networksecurity.components.dataingestion import Data_ingestion
from networksecurity.components.data_validation import DataValidation
import sys


if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(trainingpipelineconfig=trainingpipelineconfig)
        data_ingestion = Data_ingestion(data_ingestion_config=data_ingestion_config)
        data_artifacts = data_ingestion.initiate_data_ingestion()
        print(data_artifacts)
        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(data_ingestion_artifact=data_artifacts, data_validation_config=data_validation_config)
        data_validation_artifacts = data_validation.initiate_data_validation()
        print(data_validation_artifacts)
    except Exception as e:
        logging.info(NetworkSecurityException(e, sys))
        raise NetworkSecurityException(e, sys)