"""Intent classifier using TF-IDF and Logistic Regression.

For demonstration, a small dataset is embedded directly in this module.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Sample training data based on PRD examples
SAMPLE_DATA = [
    ("내 구독 목록 알려줘", "조회"),
    ("넷플릭스랑 디즈니플러스 뭐가 달라?", "비교"),
    ("가성비 좋은 OTT 뭐 있어?", "추천"),
    ("유튜브 프리미엄 해지하고 싶어요", "해지"),
    ("계속 써야 할지 고민이에요", "고민"),
]


@dataclass
class IntentClassifier:
    """Simple wrapper around scikit-learn classifier."""

    vectorizer: TfidfVectorizer
    model: LogisticRegression

    def train(self, texts: List[str], labels: List[str]) -> None:
        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)

    def predict(self, text: str) -> str:
        X = self.vectorizer.transform([text])
        return self.model.predict(X)[0]


# Create and train the classifier on import for ease of use
_classifier = IntentClassifier(TfidfVectorizer(), LogisticRegression())
_classifier.train([q for q, _ in SAMPLE_DATA], [l for _, l in SAMPLE_DATA])


def predict_intent(text: str) -> str:
    """Predict intent for ``text`` using the pre-trained classifier."""
    return _classifier.predict(text)
