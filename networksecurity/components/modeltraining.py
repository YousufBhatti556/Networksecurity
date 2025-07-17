import pandas as pd
import numpy as np
import sys
import os
from networksecurity.exeptionhandling.exception_handling import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constants import training_pipeline
from networksecurity.entity.config_entity import DataTransformationConfig, ModelTrainerConfig
from networksecurity.entity.artifact_entity import Data_Transformation_Artifacts, Model_Trainer_Artifacts, ClassificationMetricArtifact
from networksecurity.utils.main_utils.utils import save_data_to_array, save_obj_to_pickle_file, load_object, load_numpy_array, evaluate_models
from networksecurity.utils.ml_utils.model.estimator import NetworkModel as NetworkModelClass
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
import mlflow

class Model_Training:
    def __init__(self, data_transformation_artifacts: Data_Transformation_Artifacts, model_trainer_config: ModelTrainerConfig):
        self.data_transformation_artifacts = data_transformation_artifacts
        self.model_trainer_config = model_trainer_config

    def track_ml_flow(self, best_model, classification_train_metric):
        f1_score = classification_train_metric.f1_score
        precision_score = classification_train_metric.precision_score
        recall_score = classification_train_metric.recall_score

        mlflow.log_metric("f1_score", f1_score)
        mlflow.log_metric("precision_score", precision_score)
        mlflow.log_metric("recall_score", recall_score)
        mlflow.sklearn.log_model(best_model, "model")        

    def train_model(self, X_train, y_train, X_test, y_test):
        try:
            models = {
                "RandomForestClassifier": RandomForestClassifier(),
                "AdaBoostClassifier": AdaBoostClassifier(),
                "GradientBoostingClassifier": GradientBoostingClassifier(),
                "LogisticRegression": LogisticRegression(),
                "SVC": SVC(),
                "KNeighborsClassifier": KNeighborsClassifier(),
                "DecisionTreeClassifier": DecisionTreeClassifier()
            }

            params = {
                "RandomForestClassifier": {
                    "n_estimators": [100, 200, 300],
                    # "max_depth": [None, 10, 20, 30],
                    "min_samples_split": [2, 5, 10],
                    "min_samples_leaf": [1, 2, 4],
                    "bootstrap": [True, False]
                },
                "AdaBoostClassifier": {
                    "n_estimators": [50, 100, 200],
                    "learning_rate": [0.01, 0.1, 1.0]
                },
                "GradientBoostingClassifier": {
                    "n_estimators": [100, 200],
                    "learning_rate": [0.01, 0.1],
                    "max_depth": [3, 5, 10],
                    # "subsample": [0.8, 1.0]
                },
                "LogisticRegression": {},
                "SVC": {
                    "C": [0.1, 1, 10],
                    "kernel": ["linear", "rbf", "poly"],
                    "gamma": ["scale", "auto"]
                },
                "KNeighborsClassifier": {
                    "n_neighbors": [3, 5, 7, 9],
                    "weights": ["uniform", "distance"],
                    "algorithm": ["auto", "ball_tree", "kd_tree"]
                },
                "DecisionTreeClassifier": {
                    "criterion": ["gini", "entropy"],
                    # "max_depth": [None, 10, 20, 30],
                    "min_samples_split": [2, 5, 10],
                    "min_samples_leaf": [1, 2, 4]
                }
            }

            model_report: dict = evaluate_models(X_train, y_train, X_test, y_test, models, params)
            logging.info("Evaluate model function done")

            best_model_score = max(model_report.values())
            best_model_name = max(model_report, key=model_report.get)
            best_model = models[best_model_name]
            logging.info("Got the best model.")

            y_train_pred = best_model.predict(X_train)
            classification_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)
            logging.info("Tracking the experiment for train classification metrics")
            self.track_ml_flow(best_model, classification_train_metric)
            y_test_pred = best_model.predict(X_test)
            classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)
            logging.info("Tracking the experiment for train classification metrics")
            self.track_ml_flow(best_model, classification_test_metric)
            
            logging.info("Got ClassificationMetricArtifact")


            logging.info("Loading preprocessor object")
            preprocessor = load_object(self.data_transformation_artifacts.transformed_obj_file_path)

            model_dir_path = self.model_trainer_config.model_trainer_trained_model_path
            os.makedirs(os.path.dirname(model_dir_path), exist_ok=True)

            # ✅ Use a different variable name to avoid masking the class
            network_model_instance = NetworkModelClass(preprocessor=preprocessor, model=best_model)
            save_obj_to_pickle_file(self.model_trainer_config.model_trainer_trained_model_path, obj=network_model_instance)

            return Model_Trainer_Artifacts(
                trained_model_file_path=self.model_trainer_config.model_trainer_trained_model_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
            )

        except Exception as e:
            logging.info(NetworkSecurityException(e, sys))
            raise NetworkSecurityException(e, sys)

    def inititae_model_training(self) -> Model_Trainer_Artifacts:
        try:
            logging.info("Getting train and test arrays file path")
            train_array_file_path = self.data_transformation_artifacts.transformed_train_file_path
            test_array_file_path = self.data_transformation_artifacts.transformed_test_file_path

            logging.info("Loading train and test array")
            train_array = load_numpy_array(train_array_file_path)
            test_array = load_numpy_array(test_array_file_path)

            logging.info("Separating independent and dependent variables")
            X_train, y_train = train_array[:, :-1], train_array[:, -1]
            X_test, y_test = test_array[:, :-1], test_array[:, -1]

            logging.info("Training model")
            model_trainer_artifacts = self.train_model(X_train, y_train, X_test, y_test)
            return model_trainer_artifacts

        except Exception as e:
            logging.info(NetworkSecurityException(e, sys))
            raise NetworkSecurityException(e, sys)
