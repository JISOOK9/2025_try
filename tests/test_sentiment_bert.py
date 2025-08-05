"""Tests for BERT based sentiment analysis with mocked model."""

from __future__ import annotations

from unittest.mock import Mock

import torch

import subscription_bot.sentiment as sentiment


def _setup_mock(logits: list[float]) -> None:
    """Configure mocked tokenizer and model returning ``logits``."""

    sentiment._tokenizer = Mock(return_value={"input_ids": torch.tensor([[1]])})

    output = Mock()
    output.logits = torch.tensor([logits])
    sentiment._model = Mock(return_value=output)


def test_label_mapping_positive_negative_neutral():
    _setup_mock([0.1, 0.2, 0.7])
    assert sentiment.analyze_sentiment("foo") == "긍정"

    _setup_mock([0.7, 0.2, 0.1])
    assert sentiment.analyze_sentiment("bar") == "부정"

    _setup_mock([0.2, 0.6, 0.2])
    assert sentiment.analyze_sentiment("baz") == "중립"

