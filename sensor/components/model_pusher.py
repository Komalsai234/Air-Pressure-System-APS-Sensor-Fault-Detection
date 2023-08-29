from sensor.exception import exception
from sensor.logger import logging

from sensor.entity.config_entity import ModelEvalutionConfig, ModelTrainerConfig, ModelPusherConfig
from sensor.entity.artifact_entity import ModelEvalutionArtifact, ModelTrainerArtifact, ModelPusherArtifact

from datetime import datetime

from sensor.logger import logging
from sensor.exception import exception

import os
import sys
import shutil


class ModelPusher:

    def __init__(self, model_evalution_artifact: ModelEvalutionArtifact, model_pusher_config: ModelPusherConfig):

        try:
            self.model_evalution_artifact = model_evalution_artifact
            self.model_pusher_config = ModelPusherConfig

        except Exception as e:
            exception(e, sys)

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        logging.info("Initiating Model Pusher")

        trained_model_path = self.model_evalution_artifact.trained_model_file_path

        logging.info("Creating the dir model_pusher to save the trained model")

        os.makedirs(os.path.dirname(
            self.model_pusher_config.pusher_saved_model_file_path), exist_ok=True)
        shutil.copy(trained_model_path,
                    self.model_pusher_config.pusher_saved_model_file_path)

        logging.info(
            "Create a common folder saved_model to save all the model with timestamp")

        saved_model_file_path = self.model_pusher_config.saved_model_dir_file_path
        os.makedirs(os.path.dirname(
            saved_model_file_path))
        shutil.copy(trained_model_path,
                    saved_model_file_path)

        model_pusher_artifact = ModelPusherArtifact(
            saved_model_path=saved_model_file_path, model_path=trained_model_path)

        return model_pusher_artifact
