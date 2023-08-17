from sensor.constant.training_pipeline import *
from sensor.entity.config_entity import ModelTrainerConfig
from sensor.entity.artifact_entity import DataIngestionArtifact, ModelTrainerArtifact, ModelEvalutionMetrics, DataTranformationArtifact

from sensor.logger import logging
from sensor.exception import exception

from sensor.untils.main_unitls import load_numpy_file, load_obj_file, save_obj_as_file
from sensor.ml.metrics.classification_metrics import get_classification_metrics
from sensor.ml.model.estimator import SensorModelTrainer
from xgboost import XGBClassifier

import os
import sys


class ModelTrainer:

    def __init__(self, data_transformation_artifact: DataTranformationArtifact, model_trainer_config: ModelTrainerConfig):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config

        except Exception as e:
            raise exception(e, sys)

    def train_model(self, X_train, y_train):
        model_xgboost = XGBClassifier()

        model_xgboost.fit(X_train, y_train)

        return model_xgboost

    def intiaite_model_trainer(self) -> ModelTrainerArtifact:

        logging.info("Initiating the model training")

        train_file_path = self.data_transformation_artifact.transformed_train_file_path

        logging.info("Loading the training data for model training")
        train_df = load_numpy_file(train_file_path)

        test_file_path = self.data_transformation_artifact.transformed_test_file_path

        logging.info("Loading the test data for model training")
        test_df = load_numpy_file(test_file_path)

        X_train = train_df[:, :-1]
        y_train = train_df[:, -1].astype(int)
        X_test = test_df[:, :-1]
        y_test = test_df[:, -1].astype(int)

        logging.info(y_train)
        logging.info(y_train.dtype)
        logging.info(len(y_train))

        logging.info("Fitting the training data to the model")

        train_model = self.train_model(X_train, y_train)

        y_pred_train = train_model.predict(X_train)

        classification_metrics_train = get_classification_metrics(
            y_train, y_pred_train)

        if classification_metrics_train.model_f1_score < MODEL_TRAINER_EXCEPTED_SCORE:
            raise ("The Model is not performing good, try different experiments")

        y_pred_test = train_model.predict(X_test)

        classification_metrics_test = get_classification_metrics(
            y_test, y_pred_test)

        if (abs(classification_metrics_test.model_f1_score - classification_metrics_train.model_f1_score) > MODEL_TRAINER_UNDER_AND_OVERFIT_THRESHOLD):
            raise ("The Model not performing well as it is Underfitting/Overfitting")

        logging.info("Loading the preprocessing object")
        logging.info(
            self.model_trainer_config.model_trainer_trained_model_obj_path)

        preprocessed_obj = load_obj_file(
            self.data_transformation_artifact.transformed_preprocessed_obj_file_path)

        model = SensorModelTrainer(train_model, preprocessed_obj)

        os.makedirs(
            os.path.dirname(self.model_trainer_config.model_trainer_trained_model_obj_path), exist_ok=True)

        logging.info("Saving the training model")

        save_obj_as_file(
            self.model_trainer_config.model_trainer_trained_model_obj_path, model)

        model_training_artifact = ModelTrainerArtifact(trained_model_obj_path=self.model_trainer_config.model_trainer_trained_model_obj_path,
                                                       model_metrics=classification_metrics_test
                                                       )

        return model_training_artifact
