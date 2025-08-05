from pathlib import Path

import torch
from subscription_bot.finetuning import IntentExample, fine_tune_intent_model


def test_fine_tune_intent_model_runs():
    examples = [
        IntentExample("내 구독 목록 알려줘", "조회"),
        IntentExample("넷플릭스랑 디즈니플러스 뭐가 달라?", "비교"),
    ]
    model, tokenizer = fine_tune_intent_model(examples)
    inputs = tokenizer("내 구독 목록 알려줘", return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
    assert logits.shape[-1] == 2


def test_fine_tune_exports_onnx(tmp_path, monkeypatch):
    examples = [
        IntentExample("내 구독 목록 알려줘", "조회"),
        IntentExample("넷플릭스랑 디즈니플러스 뭐가 달라?", "비교"),
    ]

    def fake_export(model, args, f, **kwargs):
        Path(f).write_text("onnx")

    monkeypatch.setattr(
        "subscription_bot.finetuning.torch.onnx.export", fake_export
    )

    output_dir = tmp_path / "onnx_out"
    fine_tune_intent_model(
        examples, output_dir=str(output_dir), export_onnx=True
    )
    assert (output_dir / "model.onnx").exists()
