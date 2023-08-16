import pandas as pd


class Target_Value_Encoder:
    def __init__(self):
        self.pos = 1
        self.neg = 0

    def target_column_encoding(self, target_column):
        df_target_encoded = target_column.replace(
            {"pos": self.pos, "neg": self.neg})
        return df_target_encoded
