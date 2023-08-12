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


def write_yaml_file(file_path: str, content: dict, replace: bool):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as file:
            yaml.dump(file, content)

    except Exception as e:
        exception(e, sys)
