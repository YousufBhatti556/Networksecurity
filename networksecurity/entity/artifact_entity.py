from dataclasses import dataclass


@dataclass
class Data_Ingestion_Artifact:
    trained_file_path :str
    test_file_path :str


@dataclass
class Data_Validation_Artifact:
    validation_status:bool
    valid_train_file_path:str
    valid_test_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path:str
    drift_file_report:str