"""Shared pytest fixtures for TaskFlow tests."""

import pytest
from datetime import datetime


@pytest.fixture
def sample_datetime() -> datetime:
    """Return a fixed datetime for reproducible tests."""
    return datetime(2025, 12, 27, 10, 30, 0)
