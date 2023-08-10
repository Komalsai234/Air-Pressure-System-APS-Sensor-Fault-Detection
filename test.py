from sensor.entity.config_entity import DataIngestionConfig
import os

if __name__ == '__main__':

    d = DataIngestionConfig()
    traning_file_path = os.path.dirname(
        d.training_file_path)

    print(traning_file_path)
    print(DataIngestionConfig.training_file_path)

    data = {
        "calories": [420, 380, 390],
        "duration": [50, 40, 45]
    }

    df = data.to_csv()
