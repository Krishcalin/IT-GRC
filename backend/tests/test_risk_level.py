"""Unit tests for the 5x5 risk-level scoring (no DB required)."""

from app.models.risk import _risk_level


def test_critical():
    assert _risk_level(5, 5) == "Critical"   # 25
    assert _risk_level(4, 5) == "Critical"   # 20


def test_high():
    assert _risk_level(3, 5) == "High"       # 15
    assert _risk_level(3, 4) == "High"       # 12


def test_medium():
    assert _risk_level(2, 3) == "Medium"     # 6
    assert _risk_level(3, 2) == "Medium"     # 6


def test_low():
    assert _risk_level(2, 2) == "Low"        # 4
    assert _risk_level(1, 1) == "Low"        # 1
