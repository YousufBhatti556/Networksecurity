from networksecurity.exeptionhandling.exception_handling import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from networksecurity.components.dataingestion import Data_ingestion
import sys


if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(trainingpipelineconfig=trainingpipelineconfig)
        data_ingestion = Data_ingestion(data_ingestion_config=data_ingestion_config)
        data_artifacts = data_ingestion.initiate_data_ingestion()
        print(data_artifacts)
    except Exception as e:
        logging.info(NetworkSecurityException(e, sys))
        raise NetworkSecurityException(e, sys)