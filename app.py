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
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")
from uvicorn import run as app_run
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.exeptionhandling.exception_handling import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import Training_Pipeline
from networksecurity.constants.training_pipeline import (
    DATA_INGESTION_COLLECTION_NAME,
    DATA_INGESTION_DATABASE_NAME,
)
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

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


@app.post("/predict")
async def predict(request:Request, file:UploadFile=File(...)):
    try:
        df = pd.read_csv(file.file)
        preprocessor_obj = load_object("final_models/preprocessor.pkl")
        model_obj = load_object("final_models/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor_obj, model=model_obj)
        y_pred = network_model.predict(df)
        df["predicted_col"] = y_pred
        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes='table table-striped')
        #print(table_html)
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
    except Exception as e:
        logging.info(NetworkSecurityException(e, sys))
        raise NetworkSecurityException(e, sys)

# Run the app
if __name__ == "__main__":
    app_run("app:app", host="127.0.0.1", port=8000, reload=True)
