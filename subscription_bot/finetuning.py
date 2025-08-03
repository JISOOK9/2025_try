"""Utilities for fine-tuning Transformer models.

This module implements a minimal example of intent classification fine-tuning
using Hugging Face Transformers. It uses a tiny random model so that tests can
run quickly without heavy downloads.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import torch
from torch.utils.data import Dataset
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)


@dataclass
class IntentExample:
    """Simple text/label pair."""

    text: str
    label: str


class IntentDataset(Dataset):
    """PyTorch dataset for intent classification."""

    def __init__(self, examples: List[IntentExample], tokenizer, label2id: Dict[str, int]):
        self.examples = examples
        self.tokenizer = tokenizer
        self.label2id = label2id

    def __len__(self) -> int:  # pragma: no cover - trivial
        return len(self.examples)

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        ex = self.examples[idx]
        enc = self.tokenizer(
            ex.text,
            padding="max_length",
            truncation=True,
            max_length=32,
        )
        enc = {k: torch.tensor(v) for k, v in enc.items()}
        enc["labels"] = torch.tensor(self.label2id[ex.label])
        return enc


def fine_tune_intent_model(
    examples: List[IntentExample],
    model_name: str = "hf-internal-testing/tiny-random-bert",
    output_dir: str = "./intent_model",
) -> Tuple[AutoModelForSequenceClassification, AutoTokenizer]:
    """Fine-tune ``model_name`` on ``examples`` for intent classification.

    Parameters
    ----------
    examples:
        Training data.
    model_name:
        Pretrained model identifier on Hugging Face Hub.
    output_dir:
        Directory used by the Trainer for checkpoints.

    Returns
    -------
    model, tokenizer
        The fine-tuned model and associated tokenizer.
    """

    label_names = sorted({ex.label for ex in examples})
    label2id = {label: i for i, label in enumerate(label_names)}
    id2label = {i: label for label, i in label2id.items()}

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    dataset = IntentDataset(examples, tokenizer, label2id)

    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=len(label_names),
        id2label=id2label,
        label2id=label2id,
    )

    args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=1,
        per_device_train_batch_size=2,
        logging_steps=1,
        no_cuda=True,
    )
    trainer = Trainer(model=model, args=args, train_dataset=dataset)
    trainer.train()

    return model, tokenizer
