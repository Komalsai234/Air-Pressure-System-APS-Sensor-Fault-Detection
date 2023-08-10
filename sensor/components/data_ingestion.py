import os
import sys
import pandas as pd
from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from sensor.constant.training_pipeline import SCHEMA_DROP_COLS, SCHEMA_FILE_PATH
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.data_access.sensor_data import SensorData
from sensor.logger import logging
from sensor.exception import exception
from sklearn.model_selection import train_test_split
from sensor.untils.main_unitls import read_yaml_file


class DataIngestion:

    def __init__(self, data_ingestion_config=DataIngestionConfig()):

        self.data_ingestion_config = data_ingestion_config

    def export_data_into_feature_store(self) -> pd.DataFrame:

        try:
            logging.info("started exporting data from mongodb")

            sensor_data = SensorData()

            dataframe = sensor_data.export_collection_as_dataframe(
                collection_name=self.data_ingestion_config.collection_name)

            feature_store_dir = self.data_ingestion_config.feature_store_file_path

            path = os.path.dirname(feature_store_dir)

            os.makedirs(path, exist_ok=True)

            logging.info(
                "Saving the dataframe as csv file in feature store directory")

            dataframe.to_csv(feature_store_dir, header=True, index=False)

            return dataframe

        except Exception as e:
            pass

    def split_data_as_train_test(self, dataframe: pd.DataFrame) -> None:

        try:

            logging.info("Starting the train and test split of the Data")

            train_data, test_data = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)

            traning_file_path = os.path.dirname(
                self.data_ingestion_config.training_file_path)

            os.makedirs(traning_file_path, exist_ok=True)

            train_data.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True)

            test_file_path = os.path.dirname(
                self.data_ingestion_config.testing_file_path)

            os.makedirs(test_file_path, exist_ok=True)

            test_data.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True)

        except Exception as e:
            exception(e, sys)

    def initiate_data_ingestion(self):

        try:

            dataframe = self.export_data_into_feature_store()

            schema = read_yaml_file(SCHEMA_FILE_PATH)

            dataframe = dataframe.drop(schema[SCHEMA_DROP_COLS], axis=1)

            self.split_data_as_train_test(dataframe=dataframe)

            data_ingestion_artifact = DataIngestionArtifact(
                self.data_ingestion_config.training_file_path, self.data_ingestion_config.testing_file_path)

            return data_ingestion_artifact

        except Exception as e:
            exception(e, sys)
