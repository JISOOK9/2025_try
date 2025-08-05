"""FastAPI application for SubscriptionBot."""

from __future__ import annotations

from typing import Optional, Dict, Any

from fastapi import FastAPI
from pydantic import BaseModel

from . import chatbot


app = FastAPI()


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""

    question: str
    context: Optional[Dict[str, Any]] = None


@app.post("/chat")
def chat(request: ChatRequest) -> Dict[str, str]:
    """Return chatbot answer for the given question."""

    response = chatbot.answer(request.question, request.context)
    return {"answer": response}


@app.get("/health")
def health() -> Dict[str, str]:
    """Simple health-check endpoint."""

    return {"status": "ok"}

