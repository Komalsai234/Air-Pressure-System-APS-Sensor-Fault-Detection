import pandas as pd
from sensor.constant.training_pipeline import *


class Target_Value_Encoder:

    def __init__(self, data_frame=pd.DataFrame):

        self.data_frame = data_frame

        self.dict = {"pos": 1, "neg": 0}

    def Target_column_encoding(self):
        df_target_column = self.data_frame[TARGET_COLUMN]

        df_target_encoded = df_target_column.replace(
            {"pos": self.dict.get("pos"), "neg": self.dict.get("neg")})

        return df_target_encoded

    def Target_column_decoding(self):
        df_target_column = self.data_frame[TARGET_COLUMN]

        df_target_decoded = df_target_column.replace(
            {"1": "pos", "0": "neg"})

        return df_target_decoded
