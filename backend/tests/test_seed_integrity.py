"""Integrity checks for the ISO 27001 seed data (no DB required)."""

from app.seed.iso27001 import (
    ANNEX_A_CONTROLS, ISMS_CLAUSES, MANDATORY_DOCUMENTS,
    SAMPLE_METRICS, SAMPLE_TRAINING, DEFAULT_ROLES,
)


def test_expected_counts():
    assert len(ANNEX_A_CONTROLS) == 93
    assert len(ISMS_CLAUSES) == 30
    assert len(MANDATORY_DOCUMENTS) == 17
    assert len(DEFAULT_ROLES) == 6


def test_controls_have_required_keys_and_valid_theme():
    themes = {"Organizational", "People", "Physical", "Technological"}
    for c in ANNEX_A_CONTROLS:
        assert {"clause", "title", "theme", "description"} <= c.keys()
        assert c["theme"] in themes


def test_clauses_keys_and_numbering():
    for c in ISMS_CLAUSES:
        assert {"clause", "clause_number", "section", "title", "requirement"} <= c.keys()
        assert 4 <= c["clause_number"] <= 10


def test_mandatory_documents_have_clause_ref():
    for d in MANDATORY_DOCUMENTS:
        assert d.get("clause_ref")
        assert d.get("title")


def test_metric_directions_and_types_valid():
    for m in SAMPLE_METRICS:
        assert m["direction"] in {"higher_is_better", "lower_is_better"}
        assert m["metric_type"] in {"KPI", "KRI", "KCI"}


def test_training_campaigns_have_records_list():
    assert all(isinstance(t.get("records", []), list) for t in SAMPLE_TRAINING)
