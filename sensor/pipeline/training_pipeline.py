import os
import sys
from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig
from sensor.logger import logging
from sensor.exception import exception
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation


class TrainPipeline:

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

    def run_pipeline(self) -> None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()

        except Exception as e:
            raise exception(e, sys)
