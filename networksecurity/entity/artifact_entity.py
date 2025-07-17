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


@dataclass
class Data_Transformation_Artifacts:
    transformed_obj_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str

@dataclass
class ClassificationMetricArtifact:
    f1_score:float
    precision_score:float
    recall_score:float

@dataclass
class Model_Trainer_Artifacts:
    trained_model_file_path: str
    train_metric_artifact:ClassificationMetricArtifact
    test_metric_artifact:ClassificationMetricArtifact
    