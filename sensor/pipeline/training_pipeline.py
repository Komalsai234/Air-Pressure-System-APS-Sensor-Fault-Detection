import os
import sys

from sensor.logger import logging
from sensor.exception import exception

from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvalutionConfig, ModelPusherConfig
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTranformationArtifact, ModelTrainerArtifact, ModelEvalutionArtifact, ModelPusherArtifact

from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evalution import ModelEvalution
from sensor.components.model_pusher import ModelPusher


class TrainPipeline:

    is_training_pipeline_running = False

    def __init__(self):

        self.training_pipeline_config = TrainingPipelineConfig()
        self.data_ingestion_config = DataIngestionConfig(
            self.training_pipeline_config)

    def start_data_ingestion(self) -> DataIngestionArtifact:

        try:

            logging.info("Start Data Ingestion")

            data_ingestion = DataIngestion(self.data_ingestion_config)

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info("Data Ingestion completed")

            return data_ingestion_artifact

        except Exception as e:
            raise exception(e, sys)

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            logging.info("Start Data Validation")
            data_validation = DataValidation(
                data_ingestion_artifact, DataValidationConfig)

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Data Validation completed")
            return data_validation_artifact

        except Exception as e:
            exception(e, sys)

    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact) -> DataTranformationArtifact:
        try:
            logging.info("Starting Data Transformation")

            data_transformation = DataTransformation(
                data_validation_artifact, DataTransformationConfig)
            data_transformation_artifact = data_transformation.initiate_data_transformation()

            logging.info("Successfully completed Data Transformation")

            return data_transformation_artifact

        except Exception as e:
            exception(e, sys)

    def start_model_training(self, data_transformation_artifact: DataTranformationArtifact) -> ModelTrainerArtifact:
        try:
            start_model_train = ModelTrainer(
                data_transformation_artifact, ModelTrainerConfig)

            model_trainer_artifact = start_model_train.intiaite_model_trainer()

            return model_trainer_artifact

        except Exception as e:
            raise exception(e, sys)

    def start_model_evalution(self, model_trainer_artifact: ModelTrainerArtifact, data_validation_artifact: DataValidationArtifact) -> ModelEvalutionArtifact:
        try:
            logging.info("Starting Model Evalution")
            start_model_eval = ModelEvalution(
                model_trainer_artifact, ModelEvalutionConfig, data_validation_artifact)

            model_evalution_artifact = start_model_eval.initiate_model_evalution()

            return model_evalution_artifact

        except Exception as e:
            raise exception(e, sys)

    def start_model_pusher(self, model_evalution_artifact: ModelEvalutionArtifact) -> ModelPusherArtifact:
        try:
            logging.info("Starting Model Pusher")

            model_pusher = ModelPusher(
                model_evalution_artifact, ModelPusherConfig)

            model_pusher_artifact = model_pusher.initiate_model_pusher()

            return model_pusher_artifact

        except Exception as e:
            raise exception(e, sys)

    def run_pipeline(self) -> None:
        try:
            TrainPipeline.is_training_pipeline_running = True

            data_ingestion_artifact = self.start_data_ingestion()

            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact)

            data_transformation_artifact = self.start_data_transformation(
                data_validation_artifact)

            model_training_artifact = self.start_model_training(
                data_transformation_artifact)

            model_evalution_artifact = self.start_model_evalution(
                model_training_artifact, data_validation_artifact)

            model_pusher_artifact = self.start_model_pusher(
                model_evalution_artifact)

        except Exception as e:
            TrainPipeline.is_training_pipeline_running = False
            raise exception(e, sys)
