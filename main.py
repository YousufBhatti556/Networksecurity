from networksecurity.exeptionhandling.exception_handling import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig
from networksecurity.entity.artifact_entity import Data_Ingestion_Artifact, Data_Validation_Artifact, Data_Transformation_Artifacts
from networksecurity.components.dataingestion import Data_ingestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.datatransformation import Data_Transformation
from networksecurity.components.model_training import Model_Training
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
        data_transformation_config = DataTransformationConfig(trainingpipelineconfig=trainingpipelineconfig)
        data_transformation = Data_Transformation(data_validation_artifact=data_validation_artifacts, data_transformation_config=data_transformation_config)
        data_transformation_artifacts = data_transformation.initiate_data_transformation()
        print(data_transformation_artifacts)
        model_trainer_config = ModelTrainerConfig(trainingpipelineconfig)
        model_trainer = Model_Training(data_transformation_artifacts=data_transformation_artifacts, model_trainer_config=model_trainer_config)
        model_trainer_artifacts = model_trainer.inititae_model_training()
        print(model_trainer_artifacts)
    except Exception as e:
        logging.info(NetworkSecurityException(e, sys))
        raise NetworkSecurityException(e, sys)