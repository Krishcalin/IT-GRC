"""Integrity checks for the ISO 27001 seed data (no DB required)."""

from app.seed.iso27001 import (
    ANNEX_A_CONTROLS, ISO27019_CONTROLS, NIST_CSF_CONTROLS, SOC2_CONTROLS, IEC62443_CONTROLS,
    CONTROL_MAPPINGS, ISMS_CLAUSES, MANDATORY_DOCUMENTS,
    SAMPLE_METRICS, SAMPLE_TRAINING, SAMPLE_TASKS, SAMPLE_ASSESSMENTS, DEFAULT_ROLES,
)

THEMES = {"Organizational", "People", "Physical", "Technological"}
ALL_CONTROLS = ANNEX_A_CONTROLS + ISO27019_CONTROLS + NIST_CSF_CONTROLS + SOC2_CONTROLS + IEC62443_CONTROLS


def test_expected_counts():
    assert len(ANNEX_A_CONTROLS) == 93
    assert len(ISO27019_CONTROLS) == 12
    assert len(NIST_CSF_CONTROLS) == 22
    assert len(SOC2_CONTROLS) == 13
    assert len(IEC62443_CONTROLS) == 8
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
    clauses = [c["clause"] for c in ALL_CONTROLS]
    assert len(clauses) == len(set(clauses))


def test_additional_frameworks_well_formed():
    for c in NIST_CSF_CONTROLS:
        assert {"clause", "title", "theme", "description", "framework"} <= c.keys()
        assert c["framework"] == "NIST CSF 2.0"
    for c in SOC2_CONTROLS:
        assert {"clause", "title", "theme", "description", "framework"} <= c.keys()
        assert c["framework"] == "SOC 2"
    for c in IEC62443_CONTROLS:
        assert {"clause", "title", "theme", "description", "framework"} <= c.keys()
        assert c["framework"] == "IEC 62443-2-1:2024"


def test_iec62443_maps_to_iso_controls():
    """The ISO 27001 → IEC 62443 crosswalk should reach every 62443 SPE and be
    sourced from real ISO 27001 / 27019 controls."""
    iec_clauses = {c["clause"] for c in IEC62443_CONTROLS}
    iso_clauses = {c["clause"] for c in ANNEX_A_CONTROLS} | {c["clause"] for c in ISO27019_CONTROLS}
    targeted = set()
    for src, tgt, _rel in CONTROL_MAPPINGS:
        if tgt in iec_clauses:
            assert src in iso_clauses, f"62443 mapping from non-ISO source {src}"
            targeted.add(tgt)
    assert targeted == iec_clauses, f"SPEs with no ISO mapping: {iec_clauses - targeted}"


def test_sample_assessments_well_formed():
    types = {"Control Self-Assessment", "Maturity Assessment", "Vendor Questionnaire"}
    results = {"Compliant", "Partial", "Non-Compliant", "N/A", "Yes", "No"}
    clause_set = {c["clause"] for c in ALL_CONTROLS}
    for a in SAMPLE_ASSESSMENTS:
        assert a["title"] and a["assessment_type"] in types
        assert isinstance(a["items"], list) and a["items"]
        for it in a["items"]:
            if it.get("maturity") is not None:
                assert 0 <= it["maturity"] <= 5
            if it.get("result") is not None:
                assert it["result"] in results
            if it.get("clause") is not None:
                assert it["clause"] in clause_set


def test_control_mappings_reference_known_clauses():
    clause_set = {c["clause"] for c in ALL_CONTROLS}
    rels = {"equivalent", "related", "broader", "narrower"}
    pairs = set()
    for src, tgt, rel in CONTROL_MAPPINGS:
        assert src in clause_set, f"unknown source clause {src}"
        assert tgt in clause_set, f"unknown target clause {tgt}"
        assert src != tgt
        assert rel in rels
        pairs.add((src, tgt))
    assert len(pairs) == len(CONTROL_MAPPINGS), "duplicate mapping pair"


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
