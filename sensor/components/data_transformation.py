import os
import sys
from sensor.logger import logging
from sensor.exception import exception

from sensor.constant.training_pipeline import *
from sensor.entity.artifact_entity import DataValidationArtifact
from sensor.entity.config_entity import DataTransformationConfig
from sensor.untils.main_unitls import load_numpy_file, save_numpy_as_file
from sensor.ml.model.estimator import Target_Value_Encoder

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np

from imblearn.combine import SMOTETomek


class DataTransformation:

    def __init__(self, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig):

        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config

        except Exception as e:
            raise exception(e, sys)

    def read_csv_file(self, file_path: str) -> pd.DataFrame:
        try:
            df = pd.DataFrame(file_path)
            return df

        except Exception as e:
            raise exception(e, sys)

    @staticmethod
    def get_data_transformation_object(self):

        logging.info(
            "Getting the transformation object from get_data_transformation function")

        simple_imputer = SimpleImputer(strategy="mean")

        scaler = RobustScaler()

        logging.info("Initiated Pipeline for Simple Imputer and Robust Scaler")

        transformation_pipeline = Pipeline(
            steps=[("imputer", simple_imputer), ("robust_scaler", scaler)])

        return transformation_pipeline

    def initiate_data_transformation(self):

        logging.info("Starting Data Tranformation")

        try:

            train_df = self.read_csv_file(
                self.data_validation_artifact.valid_train_path)
            test_df = self.read_csv_file(
                self.data_validation_artifact.valid_test_path)

            logging.info("Dropping the target column for transformation")

            train_df_features = train_df.drop(TARGET_COLUMN, axis=-1)
            train_df_target = train_df[TARGET_COLUMN]

            test_df_features = test_df.drop(TARGET_COLUMN, axis=-1)
            test_df_target = test_df[TARGET_COLUMN]

            tranformation_obj = self.get_data_transformation_object()

            logging.info(
                "Transforming the labels(neg,pos) of target varaibles into 1 and 0")

            train_df_target = Target_Value_Encoder.Target_column_encoding(
                train_df_target)
            test_df_target = Target_Value_Encoder.Target_column_encoding(
                test_df_target)

            transformation_obj = self.get_data_transformation_object()

            logging.info(
                "Appyling the Preprocessing model to the train and test dataframe")

            train_df_features_arr = transformation_obj.fit_transform(
                train_df_features)
            test_df_features_arr = transformation_obj.fit_transform(
                test_df_features)

            logging.info("Applying the SMOTE+TOMEK for training dataset")

            smt = SMOTETomek(sampling_strategy="minority")

            train_df_features_arr_final, train_df_target_arr_final = smt.fit_resample(
                train_df_features_arr, train_df_target)

            logging.info("Applying the SMOTE+TOMEK for testing dataset")

            test_df_features_arr_final, test_df_target_arr_final = smt.fit_resample(
                test_df_features_arr, test_df_target)

            logging.info("Saving the training arr to the file")

            train_arr = np.c_[train_df_features_arr_final,
                              train_df_target_arr_final]
            save_numpy_as_file(
                self.data_transformation_config.data_transformation_training_file_path, train_arr)

            logging.info("Saving the testing arr to the file")

            test_arr = np.c_[test_df_features_arr_final,
                             test_df_target_arr_final]
            save_numpy_as_file(
                self.data_transformation_config.data_transformation_testing_file_path, test_arr)

            logging.info("Saving the Pre-processing object")
            sa

        except Exception as e:
            raise exception(e, sys)
