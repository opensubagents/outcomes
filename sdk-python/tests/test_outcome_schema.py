"""Outcome model round-trip and Requirement 1.x coverage."""
from __future__ import annotations

from datetime import date

import pytest
from pydantic import ValidationError

from open_outcome import OutcomeDeclaration


def test_minimum_required_fields():
    """Requirement 1.1.1 – 1.1.4."""
    o = OutcomeDeclaration(
        title="Will the deploy be reproducible?",
        as_of=date(2026, 5, 21),
        question="Does it match?",
        success_criteria=("Hash compared",),
    )
    assert o.archetype is None
    assert o.archetype_fields is None


def test_blank_title_rejected():
    """Requirement 1.1.1."""
    with pytest.raises(ValidationError):
        OutcomeDeclaration(
            title="",
            as_of=date(2026, 5, 21),
            question="ok",
            success_criteria=("ok",),
        )


def test_empty_success_criteria_rejected():
    """Requirement 1.1.4."""
    with pytest.raises(ValidationError):
        OutcomeDeclaration(
            title="t",
            as_of=date(2026, 5, 21),
            question="q",
            success_criteria=(),
        )


def test_immutability():
    """Requirement 1.3.1."""
    o = OutcomeDeclaration(
        title="t",
        as_of=date(2026, 5, 21),
        question="q",
        success_criteria=("c",),
    )
    with pytest.raises(ValidationError):
        o.title = "mutated"  # type: ignore[misc]


def test_archetype_and_fields_optional():
    """Requirement 1.2.1, 1.2.2."""
    o = OutcomeDeclaration(
        title="t",
        as_of=date(2026, 5, 21),
        question="q",
        success_criteria=("c",),
        archetype="vendor_comparison",
        archetype_fields={"candidates": ["A", "B"], "dimensions": ["d"]},
    )
    assert o.archetype == "vendor_comparison"
    assert (o.archetype_fields or {})["candidates"] == ["A", "B"]
