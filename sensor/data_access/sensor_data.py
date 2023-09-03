import sys

import numpy as np
import pandas as pd

from sensor.config.mango_db_connection import MongoDBClient
from sensor.constant.database import DATABASE_NAME

from sensor.logger import logging
from sensor.exception import exception


class SensorData:

    def __init__(self):

        try:
            self.sensors_database = MongoDBClient(database_name=DATABASE_NAME)

        except Exception as e:
            exception(e, sys)

    def export_collection_as_dataframe(self, collection_name) -> pd.DataFrame:

        try:
            sensors_collection = self.sensors_database.database[collection_name]

            sensors_data_list = list(sensors_collection.find())

            df = pd.DataFrame(sensors_data_list)

            if ('_id' in df.columns):
                df.drop('_id', axis=1, inplace=True)

            df.replace({"na": np.nan}, inplace=True)

            return df

        except Exception as e:
            exception(e, sys)
