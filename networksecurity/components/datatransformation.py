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

class Data_Validation:
    def __init__(self, data_validation_artifact:Data_Validation_Artifact, data_transformation_artifact: Data_Transformation_Artifacts):
        self.data_validation_artifact = data_validation_artifact
        self.data_transformation_artifact = data_transformation_artifact