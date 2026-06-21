"""Unit tests for the metric RAG derivation (no DB required)."""

from app.models.metric import compute_rag


def test_no_data_when_target_or_current_missing():
    assert compute_rag(None, 5, "higher_is_better") == "No Data"
    assert compute_rag(5, None, "lower_is_better") == "No Data"
    assert compute_rag(None, None, "higher_is_better") == "No Data"


def test_higher_is_better():
    assert compute_rag(95, 96, "higher_is_better") == "On Target"
    assert compute_rag(95, 95, "higher_is_better") == "On Target"
    assert compute_rag(95, 90, "higher_is_better") == "Near Target"   # >= 90% of target
    assert compute_rag(95, 80, "higher_is_better") == "Off Target"


def test_lower_is_better():
    assert compute_rag(5, 4, "lower_is_better") == "On Target"
    assert compute_rag(5, 5, "lower_is_better") == "On Target"
    assert compute_rag(5, 5.4, "lower_is_better") == "Near Target"    # within 10% over
    assert compute_rag(5, 9, "lower_is_better") == "Off Target"


def test_zero_target_lower_is_better():
    assert compute_rag(0, 0, "lower_is_better") == "On Target"
    assert compute_rag(0, 3, "lower_is_better") == "Off Target"
