import os, sys
from networksecurity.exeptionhandling.exception_handling import NetworkSecurityException
from networksecurity.logging.logger import logging
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.entity.artifact_entity import Data_Validation_Artifact, Data_Transformation_Artifacts
from networksecurity.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.config_entity import DataTransformationConfig, DataValidationConfig
from networksecurity.constants import training_pipeline
from networksecurity.utils.main_utils.utils import save_data_to_array, save_obj_to_pickle_file

class Data_Transformation:
    def __init__(self, data_validation_artifact:Data_Validation_Artifact, data_transformation_artifact: Data_Transformation_Artifacts):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            logging.info(NetworkSecurityException(e, sys))
            raise NetworkSecurityException(e, sys)
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            logging.info(NetworkSecurityException(e, sys))
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self)->Data_Transformation_Artifacts:
        try:
            logging.info("Started the data transformation")
            train_df = Data_Transformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = Data_Transformation.read_data(self.data_validation_artifact.valid_test_file_path)

            logging.info("Separating input and output features")
            input_features = train_df.drop()
        except Exception as e:
            logging.info(NetworkSecurityException(e,sys))
            raise NetworkSecurityException(e, sys)