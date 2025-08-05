from __future__ import annotations

from typing import Sequence, Tuple
import csv

from sklearn.metrics import confusion_matrix

FALLBACK_MESSAGE = "죄송해요. 아직 잘 모르겠어요."


def build_confusion_matrix(y_true: Sequence[str], y_pred: Sequence[str]) -> Tuple[list[str], list[list[int]]]:
    """Return labels and confusion matrix for the given predictions."""
    labels = sorted(set(y_true) | set(y_pred))
    matrix = confusion_matrix(y_true, y_pred, labels=labels)
    return list(labels), matrix


def save_confusion_matrix(labels: Sequence[str], matrix, path) -> None:
    """Save confusion matrix as CSV file."""
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([""] + list(labels))
        for label, row in zip(labels, matrix):
            writer.writerow([label] + list(row))


def calculate_fallback_rate(responses: Sequence[str], fallback_message: str = FALLBACK_MESSAGE) -> float:
    """Calculate the ratio of fallback responses."""
    if not responses:
        return 0.0
    count = sum(1 for r in responses if fallback_message in r)
    return count / len(responses)
