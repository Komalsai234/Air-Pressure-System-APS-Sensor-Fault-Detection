from sensor.exception import exception

from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
from sensor.entity.artifact_entity import ModelEvalutionMetrics

import os
import sys


def get_classification_metrics(y_true, y_pred) -> ModelEvalutionMetrics:
    try:

        f1_score_metrics = f1_score(y_true, y_pred)
        recall_score_metrics = recall_score(y_true, y_pred)
        precision_score_metrics = precision_score(y_true, y_pred)

        model_evalution_metrics = ModelEvalutionMetrics(model_f1_score=f1_score_metrics,
                                                        model_precision_score=precision_score_metrics,
                                                        model_recall_score=recall_score_metrics)

        return model_evalution_metrics

    except Exception as e:
        raise exception(e, sys)


def get_classification_score(y_true, y_pred):
    classification_score = accuracy_score(y_true, y_pred)

    return classification_score
