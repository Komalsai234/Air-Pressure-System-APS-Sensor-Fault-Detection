from sensor.entity.artifact_entity import ModelTrainerArtifact, DataValidationArtifact, ModelEvalutionArtifact
from sensor.entity.config_entity import ModelEvalutionConfig
from sensor.constant.training_pipeline import *
from sensor.ml.model.estimator import TrainedModelResolver, Target_Value_Encoder
from sensor.logger import logging
from sensor.exception import exception
from sensor.untils.main_unitls import load_obj_file, write_yaml_file
from sensor.ml.metrics.classification_metrics import get_classification_metrics

import os
import sys
import pandas as pd


class ModelEvalution:
    def __init__(self, model_trainer_artifact: ModelTrainerArtifact, model_evalution_config: ModelEvalutionConfig, data_validation_artifact: DataValidationArtifact):
        try:
            self.model_trainer_artifact = model_trainer_artifact
            self.model_evalution_config = model_evalution_config
            self.data_validation_artifact = data_validation_artifact
            logging.info(self.data_validation_artifact)

        except Exception as e:
            raise exception(e, sys)

    def initiate_model_evalution(self) -> ModelEvalutionArtifact:
        try:
            logging.info("Initiating model evalution")

            valid_train_path = self.data_validation_artifact.valid_train_path
            valid_test_path = self.data_validation_artifact.valid_test_path

            train_df = pd.read_csv(valid_train_path)
            test_df = pd.read_csv(valid_test_path)

            logging.info(
                "Merging the train and test dataframes for further model evalution")

            train_test_df = pd.concat([train_df, test_df], axis=0)

            logging.info("Dropping the target column from the dataframe")
            data_frame_features = train_test_df.drop(TARGET_COLUMN, axis=1)
            data_frame_target = train_test_df[TARGET_COLUMN]

            target_value_encoding = Target_Value_Encoder()

            df_target = target_value_encoding.target_column_encoding(
                data_frame_target)

            model_resolver = TrainedModelResolver(
                saved_model_dir=SAVED_MODEL_DIR)

            logging.info("Checking if the saved_model directory exsist or not")

            is_dir_exsist = model_resolver.is_dir_exsist()
            is_model_accepted = True

            if not is_dir_exsist:
                logging.info("The saved_model dir does not exsist")
                model_evalution_artifact = ModelEvalutionArtifact(
                    is_model_accepted=is_model_accepted,
                    model_improved_accuracy=None,
                    trained_model_file_path=self.model_trainer_artifact.trained_model_obj_path,
                    best_model_file_path=None,
                    best_model_evalution_metrics=None,
                    trained_model_evalution_metrics=self.model_trainer_artifact.model_metrics
                )

                logging.info(
                    f"Model Evalution Metrics: {model_evalution_artifact}")

                write_yaml_file(
                    self.model_evalution_config.model_evalution_report_file_path, model_evalution_artifact, False)

                return model_evalution_artifact

            best_model_file_path = model_resolver.get_best_model_file_path()

            logging.info("Loading the train model and latest model")

            logging.info(self.model_trainer_artifact.trained_model_obj_path)

            trained_model = load_obj_file(
                self.model_trainer_artifact.trained_model_obj_path)

            logging.info(best_model_file_path)

            latest_model = load_obj_file(best_model_file_path)

            logging.info(
                "Prediction on the data using trained and latest model")

            trained_model_pred = trained_model.predict(data_frame_features)
            latest_model_pred = latest_model.predict(data_frame_features)

            logging.info(
                "Getting the classification metrics of trained and latest model")

            trained_model_metrics = get_classification_metrics(
                trained_model_pred, df_target)
            latest_model_metrics = get_classification_metrics(
                latest_model_pred, df_target)

            logging.info(
                "Checking if the trained is having any impoved accuracy score compared to trained model")

            imporved_accuracy = trained_model_metrics.model_f1_score - \
                trained_model_metrics.model_f1_score

            if self.model_evalution_config.model_evaltion_best_model_threshold < imporved_accuracy:
                is_model_accepted = True

            else:
                is_model_accepted = False

            model_evalution_artifact = ModelEvalutionArtifact(
                is_model_accepted=is_model_accepted,
                model_improved_accuracy=imporved_accuracy,
                best_model_file_path=best_model_file_path,
                trained_model_file_path=self.model_trainer_artifact.trained_model_obj_path,
                best_model_evalution_metrics=latest_model_metrics,
                trained_model_evalution_metrics=trained_model_metrics
            )

            logging.info("Creating a yaml file for model evalution")

            write_yaml_file(
                self.model_evalution_config.model_evalution_report_file_path, model_evalution_artifact, replace=False)

            return model_evalution_artifact

        except Exception as e:
            raise exception(e, sys)
