from networksecurity.exeptionhandling.exception_handling import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import Data_Ingestion_Artifact, Data_Validation_Artifact
from networksecurity.entity.config_entity import DataValidationConfig, TrainingPipelineConfig
from networksecurity.constants import training_pipeline
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp
import os, sys
import pandas as pd

class DataValidation:
    def __init__(self, data_ingestion_artifact: Data_Ingestion_Artifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(training_pipeline.SCHEMA_FILE_PATH)
        except Exception as e:
            logging.info(NetworkSecurityException(e, sys))
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            logging.info(NetworkSecurityException(e, sys))
            raise NetworkSecurityException(e, sys)

    def validate_num_of_columns(self, df: pd.DataFrame) -> bool:
        try:
            expected_columns = self._schema_config.get("columns", [])
            num_expected_columns = len(expected_columns)
            logging.info(f"Expected columns: {num_expected_columns}, Found: {len(df.columns)}")
            return len(df.columns) == num_expected_columns
        except Exception as e:
            logging.info(NetworkSecurityException(e, sys))
            raise NetworkSecurityException(e, sys)

    def detect_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold=0.05) -> bool:
        try:
            status = True
            report = {}

            for col in base_df.columns:
                df1 = base_df[col]
                df2 = current_df[col]
                is_sample_distance = ks_2samp(df1, df2)
                if is_sample_distance.pvalue < threshold:
                    drift_found = True
                else:
                    drift_found = False
                report[col] = {
                    "p-value": float(is_sample_distance.pvalue),
                    "drift_status": drift_found
                }
                if drift_found:
                    status = False

            write_yaml_file(self.data_validation_config.drift_report_path, content=report)
            return status
        except Exception as e:
            logging.info(NetworkSecurityException(e, sys))
            raise NetworkSecurityException(e, sys)
    
    def initiate_data_validation(self) -> Data_Validation_Artifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_data = self.read_data(file_path=train_file_path)
            test_data = self.read_data(file_path=test_file_path)

            if not self.validate_num_of_columns(train_data):
                logging.info("Train dataframe does not have all the expected columns")
                return "Train dataframe does not have all the expected columns"

            if not self.validate_num_of_columns(test_data):

                logging.info("Test dataframe does not have all the expected columns")
                return "Test dataframe does not have all the expected columns"

            status = self.detect_drift(base_df=train_data, current_df=test_data)

            if status:
                os.makedirs(os.path.dirname(self.data_validation_config.train_valid_data_path), exist_ok=True)
                os.makedirs(os.path.dirname(self.data_validation_config.test_valid_data_path), exist_ok=True)
                train_data.to_csv(self.data_validation_config.train_valid_data_path, index=False)
                test_data.to_csv(self.data_validation_config.test_valid_data_path, index=False)

            return Data_Validation_Artifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.train_valid_data_path,
                valid_test_file_path=self.data_validation_config.test_valid_data_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_file_report=self.data_validation_config.drift_report_path
            )
        except Exception as e:
            logging.info(NetworkSecurityException(e, sys))
            raise NetworkSecurityException(e, sys)
