import os
import sys
import pandas as pd
from sensor.cloud_storage.s3_syncer import sync_folder_from_s3, set_aws_env_variable
from sensor.entity.prediction_config_entity import PredictionPipelineConfig
from sensor.untils.main_unitls import read_yaml_file, load_obj_file
from sensor.constant.prediction_pipeline import *
from sensor.ml.model.estimator import TrainedModelResolver
from sensor.ml.model.estimator import Target_Value_Encoder


class PredictionPipeline():
    def __init__(self, prediction_config: PredictionPipelineConfig) -> None:
        self.prediction_config = prediction_config

    def get_saved_model_dir(self):
        s3_bucket_url = f"s3://{S3_BUCKET_NAME}/{S3_BUCKET_SAVED_MODELS_DIR_NAME}"
        sync_folder_from_s3(
            s3_bucket_url, self.prediction_config.saved_models_s3)

    def run_prediction(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        df = dataframe

        # schema = read_yaml_file(file_path=SCHEMA_FILE_PATH)

        # df.drop(schema[SCHEMA_DROP_COLS], inplace=True)

        os.makedirs(self.prediction_config.saved_models_s3, exist_ok=True)

        set_aws_env_variable()
        self.get_saved_model_dir()

        model_resolver = TrainedModelResolver(
            saved_model_dir=self.prediction_config.saved_models_s3)

        best_model_file_path = model_resolver.get_best_model_file_path()

        model = load_obj_file(best_model_file_path)

        preprocess_data = model.preprocessing_obj.transform(df)

        prediction = model.trained_model.predict(preprocess_data)

        target_value_decoder = Target_Value_Encoder()

        prediction = target_value_decoder.target_column_decoding(
            pd.DataFrame(prediction))

        os.makedirs(os.path.dirname(
            self.prediction_config.prediction_file_path), exist_ok=True)

        prediction.to_csv(self.prediction_config.prediction_file_path)

        return prediction
