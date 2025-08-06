"""Data access layer for subscription_bot.

This subpackage provides simple mock modules representing internal
and external data sources. The :func:`build_user_context` function in
:mod:`subscription_bot.data.service` aggregates these sources into a
single context dictionary for use by the chatbot.
"""
from .service import build_user_context

__all__ = ["build_user_context"]
