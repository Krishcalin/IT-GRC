"""Unit tests for workflow-task overdue logic (no DB required)."""

from datetime import date

from app.models.task import task_is_overdue, TASK_OPEN_STATUSES


TODAY = date(2026, 6, 21)


def test_overdue_when_open_and_past_due():
    assert task_is_overdue(date(2026, 6, 1), "Open", TODAY) is True
    assert task_is_overdue(date(2026, 6, 1), "In Progress", TODAY) is True
    assert task_is_overdue(date(2026, 6, 1), "Blocked", TODAY) is True


def test_not_overdue_when_closed():
    assert task_is_overdue(date(2026, 6, 1), "Done", TODAY) is False
    assert task_is_overdue(date(2026, 6, 1), "Cancelled", TODAY) is False


def test_not_overdue_without_due_date_or_future_due():
    assert task_is_overdue(None, "Open", TODAY) is False
    assert task_is_overdue(date(2026, 12, 1), "Open", TODAY) is False
    assert task_is_overdue(TODAY, "Open", TODAY) is False  # due today is not overdue


def test_open_statuses_set():
    assert TASK_OPEN_STATUSES == {"Open", "In Progress", "Blocked"}
