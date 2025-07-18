import sys
import os
import certifi
import pymongo
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from starlette.responses import RedirectResponse
from uvicorn import run as app_run

from networksecurity.exeptionhandling.exception_handling import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import Training_Pipeline
from networksecurity.constants.training_pipeline import (
    DATA_INGESTION_COLLECTION_NAME,
    DATA_INGESTION_DATABASE_NAME,
)

# Load environment variables
load_dotenv()
ca = certifi.where()

# MongoDB setup
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
if not MONGO_DB_URL:
    raise ValueError("Environment variable 'MONGO_DB_URL' not found")

client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
db = client[DATA_INGESTION_DATABASE_NAME]
collection = db[DATA_INGESTION_COLLECTION_NAME]

# FastAPI app setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train():
    try:
        logging.info("Starting the training pipeline.")
        train_pipeline = Training_Pipeline()
        train_pipeline.run_pipeline()
        logging.info("Training completed successfully.")
        return JSONResponse(content={"message": "Training is successful"}, status_code=200)
    except Exception as e:
        logging.error(NetworkSecurityException(e, sys))
        raise NetworkSecurityException(e, sys)

# Run the app
if __name__ == "__main__":
    app_run("app:app", host="127.0.0.1", port=8000, reload=True)
