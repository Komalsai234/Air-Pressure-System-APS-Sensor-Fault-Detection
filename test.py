from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation


if __name__ == '__main__':

    data_ingestion = DataIngestion()
    data_ingestion_start = data_ingestion.initiate_data_ingestion()

    data_validation = DataValidation()
    data_validation_start = data_validation.initiate_data_validation()
    print(data_validation)
