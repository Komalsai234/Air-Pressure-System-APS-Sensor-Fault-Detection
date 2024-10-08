import os
from dataclasses import dataclass
from datetime import datetime

from sensor.constant.training_pipeline import *

from datetime import datetime

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")


@dataclass
class TrainingPipelineConfig:
    pipeline_name: str = PIPELINE_NAME

    artifact_dir: str = os.path.join(ARTIFACT_DIR, TIMESTAMP)

    timestamp: str = TIMESTAMP


training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()


@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(
        training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME
    )

    feature_store_file_path: str = os.path.join(
        data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME
    )

    training_file_path: str = os.path.join(
        data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME
    )

    testing_file_path: str = os.path.join(
        data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME
    )

    train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATION

    collection_name: str = DATA_INGESTION_COLLECTION_NAME


@dataclass
class DataValidationConfig:
    data_validation_dir: str = os.path.join(
        training_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME
    )

    valid_data_dir: str = os.path.join(
        data_validation_dir, DATA_VALIDATION_VALID_DIR)

    invalid_data_dir: str = os.path.join(
        data_validation_dir, DATA_VALIDATION_INVALID_DIR
    )

    valid_train_file_path: str = os.path.join(valid_data_dir, TRAIN_FILE_NAME)

    valid_test_file_path: str = os.path.join(valid_data_dir, TEST_FILE_NAME)

    invalid_train_file_path: str = os.path.join(
        invalid_data_dir, TRAIN_FILE_NAME)

    invalid_test_file_path: str = os.path.join(
        invalid_data_dir, TEST_FILE_NAME)

    drift_report_file_path: str = os.path.join(
        data_validation_dir,
        DATA_VALIDATION_DRIFT_REPORT_DIR,
        DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
    )


@dataclass
class DataTransformationConfig:

    data_transformation_dir: str = os.path.join(
        training_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR_NAME)

    data_transformation_training_file_path: str = os.path.join(
        data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, TRAIN_FILE_NAME.replace('csv', 'txt'))

    data_transformation_testing_file_path: str = os.path.join(
        data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, TEST_FILE_NAME.replace('csv', 'txt'))

    data_transformation_obj_file_path = os.path.join(
        data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR, PREPROCSSING_OBJECT_FILE_NAME)


@dataclass
class ModelTrainerConfig:
    model_trainer_dir: str = os.path.join(
        training_pipeline_config.artifact_dir, MODEL_TRAINER_DIR_NAME)

    model_trainer_trained_model_dir = os.path.join(
        model_trainer_dir, MODEL_TRAINER_TRAINED_MODEL_DIR)

    model_trainer_trained_model_obj_path = os.path.join(
        model_trainer_trained_model_dir, MODEL_TRAINER_TRAINED_MODEL_OBJ)


@dataclass
class ModelEvalutionConfig:
    model_evaltion_dir = os.path.join(
        training_pipeline_config.artifact_dir, MODEL_EVALUTION_DIR_NAME)

    model_evalution_report_file_path = os.path.join(
        model_evaltion_dir, MODEL_EVALTION_REPORT_FILE_NAME)

    model_evaltion_best_model_threshold = MODEL_EVALATION_BETTER_MODEL_THRESHOLD


@dataclass
class ModelPusherConfig:
    model_pusher_dir = os.path.join(
        training_pipeline_config.artifact_dir, MODEL_PUSHER_DIR_NAME)
    pusher_saved_model_file_path = os.path.join(
        model_pusher_dir, MODEL_FILE_NAME)
    time_stamp = datetime.now()
    time_stamp = int(time_stamp.timestamp())
    saved_model_dir_file_path = os.path.join(
        SAVED_MODEL_DIR, f"{time_stamp}", MODEL_FILE_NAME)
