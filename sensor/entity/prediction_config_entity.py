import os
from dataclasses import dataclass
from datetime import datetime

from sensor.constant.prediction_pipeline import *

from datetime import datetime

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")


@dataclass
class PredictionPipelineConfig:
    pipeline_name: str = PIPELINE_NAME

    prediction_dir: str = os.path.join(PREDICTION_DIR, TIMESTAMP)

    timestamp: str = TIMESTAMP

    prediction_file_path = os.path.join(prediction_dir, PREDICTION_FILE_NAME)

    saved_models_s3 = os.path.join(SAVED_MODELS_S3_BUCKET)
