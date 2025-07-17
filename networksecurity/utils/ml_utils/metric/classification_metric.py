import pandas as pd
from sklearn.metrics import f1_score, precision_score, recall_score
import os, sys
from networksecurity.exeptionhandling.exception_handling import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import ClassificationMetricArtifact

def get_classification_score(y_true, y_pred)-> ClassificationMetricArtifact:
    try:
        f1score = f1_score(y_true, y_pred)
        precisionscore = precision_score(y_true, y_pred)
        recallscore = recall_score(y_true, y_pred)
        classificationmetricartifact =ClassificationMetricArtifact(f1_score=f1score, precision_score=precisionscore, recall_score=recallscore)
        return classificationmetricartifact
    except Exception as e:
        logging.info(NetworkSecurityException(e, sys))
        raise NetworkSecurityException(e, sys)