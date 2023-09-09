import os
from sensor.constant.env_variable import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def set_aws_env_variable():
    os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
    os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY


def sync_folder_to_s3(folder: str, bucket_url: str):
    command = f"aws s3 sync {folder} {bucket_url}"
    os.system(command=command)


def sync_folder_from_s3(bucket_url: str, folder: str):
    command = f"aws s3 sync {bucket_url} {folder}"
    os.system(command=command)
