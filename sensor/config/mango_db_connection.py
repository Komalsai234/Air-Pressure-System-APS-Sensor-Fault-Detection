import os
import sys

import certifi
import pymongo

from sensor.constant.database import DATABASE_NAME
from sensor.constant.env_variable import MONGODB_URL_KEY
from sensor.constant.env_variable import *
from sensor.exception import exception

ca = certifi.where()


class MongoDBClient:
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = MONGODB_URL_KEY

                if mongo_db_url is None:
                    # raise exception(
                    #    f"Environment key: {MONGODB_URL_KEY} is not set.")
                    print("error")

                MongoDBClient.client = pymongo.MongoClient(
                    mongo_db_url)

            self.client = MongoDBClient.client

            self.database = self.client[database_name]

            self.database_name = database_name

        except Exception as e:
            raise exception(e, sys)
