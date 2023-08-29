import os
import sys
import yaml
from sensor.logger import logging
from sensor.exception import exception
import numpy as np
import joblib


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "r") as schemafile:
            schema = yaml.safe_load(schemafile)

        return schema

    except Exception as e:
        exception(e, sys)


def write_yaml_file(file_path: str, content, replace: bool):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as file:
            yaml.dump(content, file)

    except Exception as e:
        exception(e, sys)


def save_numpy_as_file(file_path: str, array: np.array):

    try:

        file_path_dir = os.path.dirname(file_path)
        os.makedirs(file_path_dir, exist_ok=True)

        with open(file_path, "wb") as file:
            np.save(file, array)

    except Exception as e:
        exception(e, sys)


def load_numpy_file(file_path: str) -> np.array:

    try:
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                array = np.load(file)

            return array

    except Exception as e:
        raise exception(e, sys)


def save_obj_as_file(file_path: str, object):

    try:
        if not os.path.exists(os.path.dirname(file_path)):
            file_path_dir = os.path.dirname(file_path)
            os.makedirs(file_path_dir)

        joblib.dump(object, file_path)

    except Exception as e:
        raise exception(e, sys)


def load_obj_file(file_path: str):
    try:
        if os.path.exists(file_path):
            obj = joblib.load(file_path)
            return obj

    except Exception as e:
        exception(e, sys)
