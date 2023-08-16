from sensor.constant.training_pipeline import *
from sensor.entity.config_entity import ModelTrainerConfig
from sensor.entity.artifact_entity import DataIngestionArtifact, ModelTrainerArtifact, ModelEvalutionMetrics

from sensor.logger import logging
from sensor.exception import exception

from sensor.untils.main_unitls import load_numpy_file

import os
import sys


class ModelTrainer:

    def __init__(self, data_transformation_artifact: DataIngestionArtifact, model_trainer_config: ModelTrainerConfig):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config

        except Exception as e:
            raise exception(e, sys)

    def intiaite_model_trainer(self):

        train_file_path = self.data_transformation_artifact.trained_file_path
