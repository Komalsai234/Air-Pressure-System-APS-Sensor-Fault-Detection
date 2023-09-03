from fastapi import FastAPI, File, UploadFile
from uvicorn import run
from starlette.responses import RedirectResponse, FileResponse
from fastapi.responses import Response
from sensor.constant.application import *
from sensor.pipeline.training_pipeline import TrainPipeline
from sensor.ml.model.estimator import TrainedModelResolver
from sensor.untils.main_unitls import load_obj_file
from sensor.constant.training_pipeline import *
from sensor.logger import logging
from sensor.exception import exception
import pandas as pd

import os
import sys

app = FastAPI()


@app.get("/")
def index():
    return RedirectResponse(url="/docs")


@app.post("/train")
def run_training_pipeline():
    training_pipeline = TrainPipeline()
    try:
        if TrainPipeline.is_training_pipeline_running:
            return Response("The Training Pipeline is already running")

        training_pipeline.run_pipeline()
        return Response("Training Pipeline started")

    except Exception as e:
        raise exception(e, sys)


@app.post("/predict")
def predict_pipeline(csv_file: UploadFile):
    if not csv_file.filename.endswith(".csv"):
        return Response("The Upload file should be .csv format")

    df = pd.read_csv(csv_file.file)

    model_resolver = TrainedModelResolver(saved_model_dir=SAVED_MODEL_DIR)

    best_model = load_obj_file(
        file_path=model_resolver.get_best_model_file_path())

    y_pred = best_model.predict(df)
    prediction = pd.DataFrame(y_pred)

    prediction.to_csv('prediction.csv')

    return FileResponse('prediction.csv', filename='prediction.csv')


if __name__ == "__main__":
    run(app, host=APP_HOST, port=APP_PORT)
