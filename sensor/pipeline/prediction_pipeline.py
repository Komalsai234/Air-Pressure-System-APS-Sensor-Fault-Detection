import os
import sys
import pandas as pd
from sensor.entity.prediction_config_entity import PredictionPipelineConfig
from sensor.entity.artifact_entity import DataTranformationArtifact, ModelTrainerArtifact
from sensor.untils.main_unitls import read_yaml_file, load_obj_file
from sensor.constant.prediction_pipeline import *
from sensor.ml.model.estimator import Target_Value_Encoder


class PredictionPipeline():
    def __init__(self, prediction_config: PredictionPipelineConfig, transformation_artifact=DataTranformationArtifact, trainer_artifacrt=ModelTrainerArtifact) -> None:
        self.prediction_config = prediction_config
        self.data_transformation_artifact = transformation_artifact
        self.model_trainer_artifact = trainer_artifacrt

    def get_prediction(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        df = dataframe

        schema = read_yaml_file(file_path=SCHEMA_FILE_PATH)

        df.drop(schema[SCHEMA_DROP_COLS], inplace=True)

        model_preprocessor_file_path = self.data_transformation_artifact.transformed_preprocessed_obj_file_path

        model_preprocessor = load_obj_file(
            file_path=model_preprocessor_file_path)

        df_preprocessed = model_preprocessor.transform(df)

        trained_model_file_path = self.model_trainer_artifact.trained_model_obj_path

        trained_model = load_obj_file(trained_model_file_path)

        prediction = pd.DataFrame(trained_model.predict(df_preprocessed))

        os.makedirs(os.path.dirname(
            self.prediction_config.prediction_file_path), exist_ok=True)

        prediction.to_csv(self.prediction_config.prediction_file_path)

        return prediction
