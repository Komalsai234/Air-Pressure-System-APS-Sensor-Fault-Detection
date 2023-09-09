import os

PIPELINE_NAME = "sensor"
PREDICTION_DIR = "prediction"
MODEL_FILE_NAME = "model.joblib"

S3_BUCKET_NAME = "my-sensor-pipeline"
S3_BUCKET_SAVED_MODELS_DIR_NAME = "/SAVED_MODEL_DIR/"

SAVED_MODELS_S3_BUCKET = "S3_BUCKET_MODELS"

SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")
SCHEMA_DROP_COLS = "drop_columns"

PREDICTION_FILE_NAME = "prediction.csv"
