"""Conformance: outcome.json and verdict.json fixtures validate against the schemas."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

from open_outcome import (
    Citation,
    Claim,
    Confidence,
    HeuristicVerifier,
    OutcomeDeclaration,
    Report,
    SourceKind,
    validate_outcome_dict,
    validate_verdict_dict,
)
from open_outcome.conformance import (
    evidence_schema,
    outcome_schema,
    verdict_schema,
)


def test_bundled_schemas_match_canonical_copies():
    """The SDK-bundled schemas MUST equal the schemas in /schema."""
    repo_root = Path(__file__).resolve().parents[2]
    for name, fn in (
        ("outcome.schema.json", outcome_schema),
        ("verdict.schema.json", verdict_schema),
        ("evidence.schema.json", evidence_schema),
    ):
        canonical = json.loads((repo_root / "schema" / name).read_text())
        assert fn() == canonical, f"bundled {name} drifted from canonical"


def test_minimum_outcome_validates():
    data = {
        "title": "t",
        "as_of": "2026-05-21",
        "question": "q",
        "success_criteria": ["c"],
    }
    validate_outcome_dict(data)


def test_outcome_missing_field_fails():
    data = {
        "title": "t",
        "as_of": "2026-05-21",
        "question": "q",
        # missing success_criteria
    }
    with pytest.raises(Exception):
        validate_outcome_dict(data)


def test_verifier_output_validates():
    outcome = OutcomeDeclaration(
        title="t",
        as_of=date(2026, 5, 21),
        question="q",
        success_criteria=("c",),
    )
    claim = Claim(
        statement="x",
        confidence=Confidence.HIGH,
        citations=(
            Citation(
                url="https://example.com/a",
                title="a",
                accessed=date(2026, 5, 21),
                kind=SourceKind.PRIMARY,
            ),
            Citation(
                url="https://example.com/b",
                title="b",
                accessed=date(2026, 5, 21),
                kind=SourceKind.PRIMARY,
            ),
        ),
    )
    report = Report(summary="one. two.", claims=(claim,))
    verdict = HeuristicVerifier().verify(outcome, report)
    validate_verdict_dict(verdict.to_jsonable())
