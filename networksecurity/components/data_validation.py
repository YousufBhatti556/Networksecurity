from networksecurity.exeptionhandling.exception_handling import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import Data_Ingestion_Artifact, Data_Validation_Artifact
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from networksecurity.components.dataingestion import Data_ingestion
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp
import os, sys
import pandas as pd

class DataValidation:
    def __init__(self, data_ingestion_artifact: Data_Ingestion_Artifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            logging.info(NetworkSecurityException(e, sys))
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path)-> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            logging.info(NetworkSecurityException(e,sys))
            raise NetworkSecurityException(e, sys)

    def validate_num_of_columns(self, df: pd.DataFrame)->bool:
        try:
            num_of_cols = len(self._schema_config)
            logging.info(f"Number of columns {num_of_cols}")
            logging.info(f"Dataframe has {len(df.columns)} number of columns")
            if len(df.columns) == num_of_cols:
                return True
            return False
        except Exception as e:
            logging.info(NetworkSecurityException(e,sys))
            raise NetworkSecurityException(e,sys)


    def detect_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame,threshold = 0.05)->bool:
        try:
            status = True
            report = {}
            
            for col in base_df.columns:
                df1 = base_df[col]
                df2 = current_df[col]
                is_sample_distance = ks_2samp(df1, df2)
                if threshold <= is_sample_distance.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({"column":{
                    "p-value":float(is_sample_distance.pvalue),
                    "drift_status":bool(is_found)
                }})
            drift_report_file_path = self.data_validation_config.drift_report_path
            dir_path = os.makedirs(drift_report_file_path, exist_ok=True)
            write_yaml_file(drift_report_file_path, content=report)

            return status
        except Exception as e:
            logging.info(NetworkSecurityException(e,sys))
            raise NetworkSecurityException(e,sys)
    
    def initiate_data_validation(self)->Data_Validation_Artifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_data = DataValidation.read_data(file_path=train_file_path)
            test_data = DataValidation.read_data(file_path=test_file_path)

            ## validate num of columns
            train_status = self.validate_num_of_columns(train_data)
            if not train_status:
                error_message = f"Train dataframe doesnot have all the columns"
            test_status = self.validate_num_of_columns(test_data)
            if not test_status:
                error_message = f"Test dataframe doesnot have all the columns"
            status = self.detect_drift(base_df=train_data, current_df=test_data)
            if status:
                train_dir_path = os.path.dirname(self.data_validation_config.train_valid_data_path)
                os.makedirs(train_dir_path, exist_ok=True)
                train_data.to_csv(self.data_validation_config.train_valid_data_path, index=False, header=None)
                test_dir_path = os.path.dirname(self.data_validation_config.test_valid_data_path)
                os.makedirs(test_dir_path, exist_ok=True)
                test_data.to_csv(self.data_validation_config.test_valid_data_path, index=False, header=None)
            data_validation_artifact = Data_Validation_Artifact(
                status= status,
                valid_train_file_path=self.data_validation_config.train_valid_data_path,
                valid_test_file_path = self.data_validation_config.test_valid_data_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_file_report=self.data_validation_config.drift_report_path
            )
                
        except Exception as e:
            logging.info(NetworkSecurityException(e, sys))
            raise NetworkSecurityException(e ,sys)
