import os, sys
import pickle, yaml
import numpy as np
from networksecurity.exeptionhandling.exception_handling import NetworkSecurityException
from networksecurity.logging.logger import logging

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
    
def save_data_to_array(file_path:str, array:np.array):
    try:
        with open(file_path, "wb") as file:
            np.save(file, array)
    except Exception as e:
        logging.info(NetworkSecurityException(e, sys))
        raise NetworkSecurityException(e, sys)
    
def save_obj_to_pickle_file(file_path:str, obj:object):
    try:
        with open(file_path, "wb") as file:
            pickle.dump(obj, file)
    except Exception as e:
        logging.info(NetworkSecurityException(e, sys))
        raise NetworkSecurityException(e, sys)