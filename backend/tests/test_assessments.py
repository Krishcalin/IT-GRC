"""Unit tests for assessment scoring (no DB required)."""

from app.models.assessment import aggregate_score


def test_maturity_weighted_when_maturities_present():
    # avg(3,2,4,2,3) = 2.8 -> 2.8/5*100 = 56.0
    assert aggregate_score([3, 2, 4, 2, 3], [None] * 5) == 56.0
    assert aggregate_score([5, 5], [None, None]) == 100.0
    assert aggregate_score([0, 0], [None, None]) == 0.0


def test_result_based_when_no_maturity():
    # Yes,Yes,No,Yes,Partial -> good=3, partial=0.5 -> 3.5/5*100 = 70.0
    assert aggregate_score([None] * 5, ["Yes", "Yes", "No", "Yes", "Partial"]) == 70.0
    assert aggregate_score([None, None], ["Compliant", "Compliant"]) == 100.0
    assert aggregate_score([None, None], ["Non-Compliant", "Non-Compliant"]) == 0.0


def test_na_and_blank_results_ignored():
    # Only the two rated results count; N/A and None are ignored.
    assert aggregate_score([None] * 4, ["Compliant", "N/A", None, "Non-Compliant"]) == 50.0


def test_empty_is_zero():
    assert aggregate_score([], []) == 0.0
    assert aggregate_score([None], [None]) == 0.0
