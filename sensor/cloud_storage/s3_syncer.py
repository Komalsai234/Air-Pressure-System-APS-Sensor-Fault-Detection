import os


def sync_folder_to_s3(folder: str, bucket_url: str):
    command = "aws s3 sync {folder} {bucket_url}"
    os.system(command=command)


def sync_folder_from_s3(folder: str, bucket_url: str):
    command = "aws s3 sync {bucket_url} {folder}"
    os.system(command=command)
