import os, sys
import pickle, yaml
import numpy as np
from networksecurity.exeptionhandling.exception_handling import NetworkSecurityException
from networksecurity.logging.logger import logging
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

def read_yaml_file(file_path):
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.info(NetworkSecurityException(e, sys))
        raise NetworkSecurityException(e, sys)

def write_yaml_file(file_path: str, content, replace: bool = True):
    try:
        if replace and os.path.exists(file_path):
            os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        logging.info(NetworkSecurityException(e, sys))
        raise NetworkSecurityException(e, sys)

def save_data_to_array(file_path: str, array: np.ndarray):
    try:
        # Fix: Ensure parent directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file:
            np.save(file, array)
    except Exception as e:
        logging.info(NetworkSecurityException(e, sys))
        raise NetworkSecurityException(e, sys)

def save_obj_to_pickle_file(file_path: str, obj: object):
    try:
        # Fix: Ensure parent directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file:
            pickle.dump(obj, file)
    except Exception as e:
        logging.info(NetworkSecurityException(e, sys))
        raise NetworkSecurityException(e, sys)
    
def load_object(file_path: str):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file path: {file_path} does not exist")
        
        with open(file_path, "rb") as file:
            return pickle.load(file)
        
    except Exception as e:
        logging.info(NetworkSecurityException(e, sys))
        raise NetworkSecurityException(e, sys)
        
def load_numpy_array(file_path:str)->np.array:
    try:
        array = np.load(file_path)
        return array
    except Exception as e:
        logging.info(NetworkSecurityException(e, sys))
        raise NetworkSecurityException(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models, params):
    try:
        report = {}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            para =params[list(models.keys())[i]]

            gs = GridSearchCV(model, param_grid=para, cv=3)
            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_true=y_train, y_pred=y_train_pred)
            test_model_score = r2_score(y_true=y_test, y_pred=y_test_pred)
            
            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        logging.info(NetworkSecurityException(e, sys))
        raise NetworkSecurityException(e,sys)