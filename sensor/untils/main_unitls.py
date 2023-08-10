import os
import sys
import yaml
from sensor.logger import logging
from sensor.exception import exception


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "r") as schemafile:
            schema = yaml.safe_load(schemafile)

        return schema

    except Exception as e:
        exception(e, sys)
