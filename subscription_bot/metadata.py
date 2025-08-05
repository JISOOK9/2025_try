"""Utilities to extract subscription metadata using spaCy."""
from __future__ import annotations

import re
from typing import Dict, List, Union

import spacy
from spacy.pipeline import EntityRuler

_nlp = spacy.load("ko_core_news_sm")
_ruler = _nlp.add_pipe("entity_ruler", before="ner")
_ruler.add_patterns([
    {"label": "PRICE", "pattern": [{"TEXT": {"REGEX": r"^\d+[\d,]*원.*$"}}]},
    {"label": "PRICE", "pattern": [{"TEXT": {"REGEX": r"^\d+[\d,]*달러.*$"}}]},
    {"label": "PRICE", "pattern": [{"TEXT": {"REGEX": r"^\d+[\d,]*$"}}, {"TEXT": {"REGEX": "원|달러"}}]},
    {"label": "BENEFIT", "pattern": [{"LOWER": "무료"}, {"POS": "NOUN"}]},
    {"label": "BENEFIT", "pattern": [{"LOWER": "무제한"}, {"POS": "NOUN"}]},
    {"label": "BENEFIT", "pattern": [{"LOWER": "할인"}, {"POS": "NOUN"}]},
])


def _clean_price(text: str) -> str:
    """Return currency expression without Korean particles."""
    match = re.search(r"\d[\d,]*\s*(?:원|달러)", text)
    return match.group(0) if match else text


def tag_metadata(text: str) -> Dict[str, Union[str, List[str], None]]:
    """Extract 상품명, 가격, 혜택 information from ``text``."""
    doc = _nlp(text)
    match = re.search(r"(.*?)\s*(?:은|는)", text)
    product = match.group(1).strip() if match else None
    prices = [_clean_price(ent.text) for ent in doc.ents if ent.label_ == "PRICE"]
    benefits = [ent.text for ent in doc.ents if ent.label_ == "BENEFIT"]
    return {"상품명": product, "가격": prices, "혜택": benefits}
