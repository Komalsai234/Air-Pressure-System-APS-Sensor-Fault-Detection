from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str


@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_path: str
    valid_test_path: str
    invalid_train_path: str
    invalid_test_path: str
    drift_report_file_path: str


@dataclass
class DataTranformationArtifact:
    transformed_preprocessed_obj_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str


@dataclass
class ModelEvalutionMetrics:
    model_f1_score: int
    model_precision_score: int
    model_recall_score: int


@dataclass
class ModelTrainerArtifact:
    trained_model_obj_path: str
    model_metrics: ModelEvalutionMetrics
