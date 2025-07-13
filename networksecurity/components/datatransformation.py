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
from networksecurity.constants.training_pipeline import TARGET_COLUMN

class Data_Transformation:
    def __init__(self, data_validation_artifact:Data_Validation_Artifact, data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
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
        
    def get_data_transformer_object(self)->Pipeline:
        logging.info("Entered the get_data_transformer_object function")
        try:
            imputer =  KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor:Pipeline = Pipeline([
                ("imputer", imputer)
            ])
            return processor
        except Exception as e:
            logging.info(NetworkSecurityException(e, sys))
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self)->Data_Transformation_Artifacts:
        try:
            logging.info("Started the data transformation")
            train_df = Data_Transformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = Data_Transformation.read_data(self.data_validation_artifact.valid_test_file_path)

            logging.info("Separating input and output features")
            input_train_features = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            train_target_feature = train_df[TARGET_COLUMN]
            train_target_feature = train_target_feature.replace(-1, 0)

            input_test_features = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            test_target_feature = test_df[TARGET_COLUMN]
            test_target_feature = test_target_feature.replace(-1, 0)
            
            preprocessor_obj = self.get_data_transformer_object()
            train_input_features_transformed_array = preprocessor_obj.fit_transform(input_train_features)
            test_input_features_transformed_array = preprocessor_obj.transform(input_test_features)

            logging.info("Transformation on train and test input features done.")
            train_arr = np.c_[train_input_features_transformed_array, np.array(train_target_feature)]
            test_arr = np.c_[test_input_features_transformed_array, np.array(test_target_feature)]

            logging.info("Saving array and preprocessor object")
            save_data_to_array(self.data_transformation_config.train_data_transformed_dir, train_arr)
            save_data_to_array(self.data_transformation_config.test_data_transformed_dir, test_arr)
            save_obj_to_pickle_file(self.data_transformation_config.transformed_obj_dir, preprocessor_obj)

            return Data_Transformation_Artifacts(transformed_train_file_path=self.data_transformation_config.train_data_transformed_dir,
                                                 transformed_test_file_path=self.data_transformation_config.test_data_transformed_dir,
                                                 transformed_obj_file_path=self.data_transformation_config.transformed_obj_dir)
            

        except Exception as e:
            logging.info(NetworkSecurityException(e,sys))
            raise NetworkSecurityException(e, sys)