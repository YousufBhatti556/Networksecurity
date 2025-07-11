import os, sys
import pickle, yaml
from networksecurity.exeptionhandling.exception_handling import NetworkSecurityException
from networksecurity.logging.logger import logging

def read_yaml_file(file_path):
    try:
        with open(file_path, "rb") as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.info(NetworkSecurityException(e, sys))
        raise(NetworkSecurityException(e, sys))
    
def write_yaml_file(file_path:str, content, replace:bool = True):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(file)
    except Exception as e:
        logging.info(NetworkSecurityException(e,sys))
        raise NetworkSecurityException(e, sys)
