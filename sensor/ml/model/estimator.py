import pandas as pd


class Target_Value_Encoder:
    def __init__(self):
        self.pos = 1
        self.neg = 0

    def target_column_encoding(self, target_column):
        df_target_encoded = target_column.replace(
            {"pos": self.pos, "neg": self.neg})
        return df_target_encoded


class SensorModelTrainer:
    def __init__(self, trained_model, preprocessing_obj):
        self.trained_model = trained_model
        self.preprocessing_obj = preprocessing_obj

    def predict(self, y_test):
        y_test_preprocessing = self.preprocessing_obj.transform(y_test)
        y_test_prediction = self.trained_model.predict(y_test_preprocessing)

        return y_test_prediction
