"""Integrity checks for the ISO 27001 seed data (no DB required)."""

from app.seed.iso27001 import (
    ANNEX_A_CONTROLS, ISO27019_CONTROLS, ISMS_CLAUSES, MANDATORY_DOCUMENTS,
    SAMPLE_METRICS, SAMPLE_TRAINING, SAMPLE_TASKS, DEFAULT_ROLES,
)

THEMES = {"Organizational", "People", "Physical", "Technological"}


def test_expected_counts():
    assert len(ANNEX_A_CONTROLS) == 93
    assert len(ISO27019_CONTROLS) == 12
    assert len(ISMS_CLAUSES) == 30
    assert len(MANDATORY_DOCUMENTS) == 17
    assert len(DEFAULT_ROLES) == 6


def test_controls_have_required_keys_and_valid_theme():
    for c in ANNEX_A_CONTROLS:
        assert {"clause", "title", "theme", "description"} <= c.keys()
        assert c["theme"] in THEMES


def test_iso27019_controls_well_formed():
    annex_clauses = {c["clause"] for c in ANNEX_A_CONTROLS}
    for c in ISO27019_CONTROLS:
        assert {"clause", "title", "theme", "description", "framework"} <= c.keys()
        assert c["theme"] in THEMES
        assert c["framework"] == "ISO 27019:2024"
        assert c["clause"].startswith("ENR.")
        assert c["clause"] not in annex_clauses  # no collision with Annex A


def test_all_control_clauses_unique():
    clauses = [c["clause"] for c in ANNEX_A_CONTROLS + ISO27019_CONTROLS]
    assert len(clauses) == len(set(clauses))


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


def test_sample_tasks_well_formed():
    types = {"Action", "Approval", "Review", "Remediation"}
    priorities = {"Low", "Medium", "High", "Critical"}
    statuses = {"Open", "In Progress", "Blocked", "Done", "Cancelled"}
    assert len(SAMPLE_TASKS) >= 1
    for t in SAMPLE_TASKS:
        assert t["title"]
        assert t["task_type"] in types
        assert t["priority"] in priorities
        assert t["status"] in statuses
        assert isinstance(t["due_offset_days"], int)
