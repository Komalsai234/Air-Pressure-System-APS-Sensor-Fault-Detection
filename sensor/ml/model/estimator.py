import pandas as pd
import os
import sys

from sensor.exception import exception
from sensor.constant.training_pipeline import SAVED_MODEL_DIR


class Target_Value_Encoder:
    def __init__(self):
        self.pos = 1
        self.neg = 0

    def target_column_encoding(self, target_column):
        df_target_encoded = target_column.replace(
            {"pos": self.pos, "neg": self.neg})
        return df_target_encoded

    def target_column_decoding(self, encoded_target_column):
        df_decoded = encoded_target_column.replace({1: "pos", 0: "neg"})

        return df_decoded


class SensorModelTrainer:
    def __init__(self, trained_model, preprocessing_obj):
        self.trained_model = trained_model
        self.preprocessing_obj = preprocessing_obj

    def predict(self, y_test):
        y_test_preprocessing = self.preprocessing_obj.transform(y_test)
        y_test_prediction = self.trained_model.predict(y_test_preprocessing)

        return y_test_prediction


class TrainedModelResolver:

    def __init__(self, saved_model_dir: SAVED_MODEL_DIR):
        self.saved_model_dir = saved_model_dir

    def get_best_model_file_path(self):
        try:
            time_stamps_list = os.listdir(self.saved_model_dir)
            latest_time_stamp = list(map(int, time_stamps_list))

            latest_model_timestamp = max(latest_time_stamp)

            latest_model_file_path = os.path.join(
                SAVED_MODEL_DIR, f"{latest_model_timestamp}")

            return latest_model_file_path

        except Exception as e:
            raise exception(e, sys)

    def is_dir_exsist(self) -> bool:

        try:
            if not os.path.exists(self.saved_model_dir):
                return False

            if len(os.listdir(self.saved_model_dir) == 0):
                return False

            latest_model_path = self.get_best_model_file_path

            if not os.path.exists(latest_model_path):
                return False

            return True

        except Exception as e:
            raise exception(e, sys)
