import os

TARGET_COLUMN = "class"
PIPELINE_NAME = "sensor"
ARTIFACT_DIR = "artifact"

FILE_NAME = "sensor.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.joblib"

MODEL_FILE_NAME = "model.joblib"

SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")

SCHEMA_DROP_COLS = "drop_columns"

SAVED_MODEL_DIR = os.path.join("saved_models")

# Data Ingestion related variables

DATA_INGESTION_COLLECTION_NAME: str = "My_Collection"

DATA_INGESTION_DIR_NAME: str = "data_ingestion"

DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"

DATA_INGESTION_INGESTED_DIR: str = "ingested"

DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2

# Data Validation related variable declaration

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"


# Data transformation related variables
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"

# Model Trainer related variable

MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_OBJ: str = "model.joblib"
MODEL_TRAINER_EXCEPTED_SCORE: int = 0.6
MODEL_TRAINER_UNDER_AND_OVERFIT_THRESHOLD: int = 0.5


# Variable related to Model Evalution

MODEL_EVALUTION_DIR_NAME: str = "model_evalution"
MODEL_EVALATION_BETTER_MODEL_THRESHOLD: float = 0.02
MODEL_EVALTION_REPORT_FILE_NAME: str = "model_report.yaml"

# Variables related to Model Pusher
MODEL_PUSHER_DIR_NAME = "model_pusher"
MODEL_PUSHER_SAVED_DIR_NAME = SAVED_MODEL_DIR
