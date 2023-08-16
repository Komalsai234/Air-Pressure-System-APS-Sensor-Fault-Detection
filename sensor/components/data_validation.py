from sensor.constant.training_pipeline import *
from sensor.logger import logging
from sensor.exception import exception
from sensor.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact
from sensor.entity.config_entity import DataValidationConfig
from sensor.untils.main_unitls import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp

import os
import sys
import pandas as pd


class DataValidation:

    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):

        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_file = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            exception(e, sys)

    def validate_columns(self, dataframe: pd.DataFrame):

        try:
            status = (len(self.schema_file['columns']) == len(
                dataframe.columns))

            logging.info(f"{status} : The status of validate columns")

            return status

        except Exception as e:
            exception(e, sys)

    def is_numerical_columns_exsist(self, dataframe: pd.DataFrame) -> bool:

        try:

            df_columns = dataframe.columns
            schema_num_cols = self.schema_file['numerical_columns']

            exsist: bool = True

            for cols in schema_num_cols:
                if (cols not in df_columns):
                    exsist = False

            logging.info(f"{exsist} : The status of numerical columns exsist")

            return exsist

        except Exception as e:
            raise exception(e, sys)

    def read_data(self, file_path: str) -> pd.DataFrame:

        try:
            data_frame = pd.read_csv(file_path)

            return data_frame

        except Exception as e:
            exception(e, sys)

    def detect_data_drift(self, base_dataframe: pd.DataFrame, compare_dataframe: pd.DataFrame, report_path: str):

        try:

            report = {}

            for col in base_dataframe.columns:
                result = ks_2samp(base_dataframe[col], compare_dataframe[col])

                drift_status: bool = True

                p_value = result.pvalue

                if (p_value < 0.5):
                    is_found = True
                    report.update({col: {"statistic": result.statistic,
                                         "p-value": result.pvalue, "drift": is_found}})

                else:
                    is_found = False
                    drift_status = False
                    report.update({col: {"statistic": result.statistic,
                                         "p-value": result.pvalue, "drift": is_found}})

            report_file_dir = os.path.dirname(report_path)

            os.makedirs(report_file_dir, exist_ok=True)

            write_yaml_file(report_path, report, replace=False)

            return drift_status

        except exception as e:
            exception(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:

            logging.info("Initiating Data Validation")

            train_data_frame = self.read_data(
                self.data_ingestion_artifact.trained_file_path)

            test_data_frame = self.read_data(
                self.data_ingestion_artifact.test_file_path)

            status_validate_columns_train = self.validate_columns(
                train_data_frame)

            logging.info("Started Validating the Dataframes")

            if not status_validate_columns_train:
                raise Exception("Validating Columns in Training Data failed")

            status_validate_columns_test = self.validate_columns(
                test_data_frame)
            if not status_validate_columns_test:
                raise Exception("Validating Columns in Test Data failed")

            status_validate_numcol_train = self.validate_columns(
                train_data_frame)
            if not status_validate_numcol_train:
                raise Exception(
                    "Validating Numerical Columns in Train Data failed")

            status_validate_numcol_test = self.validate_columns(
                test_data_frame)
            if not status_validate_numcol_test:
                raise Exception(
                    "Validating Numerical Columns in Test Data failed")

            status = self.detect_data_drift(
                train_data_frame, test_data_frame, self.data_validation_config.drift_report_file_path)

            data_validation_artifact = DataValidationArtifact(
                status,
                self.data_ingestion_artifact.trained_file_path,
                self.data_ingestion_artifact.test_file_path,
                None,
                None,
                self.data_validation_config.drift_report_file_path)

            return data_validation_artifact

        except Exception as e:
            exception(e, sys)
