"""HeuristicVerifier behavior and determinism (Section 2)."""
from __future__ import annotations

from datetime import date

import pytest
from pydantic import ValidationError

from open_outcome import (
    Citation,
    Claim,
    Confidence,
    HeuristicVerifier,
    OutcomeDeclaration,
    Report,
    SourceKind,
)


def _make_outcome() -> OutcomeDeclaration:
    return OutcomeDeclaration(
        title="t",
        as_of=date(2026, 5, 21),
        question="q",
        success_criteria=("hash compared",),
        archetype="deep_dive",
        archetype_fields={"angles": ["reproducibility"]},
    )


def _make_high_confidence_claim() -> Claim:
    return Claim(
        statement="The CI artifact hash equals the local hash.",
        confidence=Confidence.HIGH,
        citations=(
            Citation(
                url="https://example.com/ci-run-1234",
                title="CI run #1234",
                accessed=date(2026, 5, 21),
                kind=SourceKind.PRIMARY,
            ),
            Citation(
                url="https://example.com/local-build-log",
                title="Local build log",
                accessed=date(2026, 5, 21),
                kind=SourceKind.PRIMARY,
            ),
        ),
    )


def test_high_confidence_requires_two_primaries():
    """Requirement 5.1.1: enforced at the model level."""
    with pytest.raises(ValidationError):
        Claim(
            statement="x",
            confidence=Confidence.HIGH,
            citations=(),  # zero citations, not allowed for non-low
        )


def test_verdict_carries_spec_version():
    """Requirement 3.1.3."""
    outcome = _make_outcome()
    report = Report(
        summary="hash compared. reproducibility confirmed.",
        claims=(_make_high_confidence_claim(),),
        methodology_notes="diff -q on both artifacts",
    )
    v = HeuristicVerifier().verify(outcome, report)
    assert v.spec_version == "0.1.0"


def test_dimension_names_unique():
    """Requirement 3.3.1 is enforced by Verdict's model validator."""
    outcome = _make_outcome()
    report = Report(
        summary="hash compared. reproducibility confirmed.",
        claims=(_make_high_confidence_claim(),),
    )
    v = HeuristicVerifier().verify(outcome, report)
    names = [d.name for d in v.dimensions]
    assert len(set(names)) == len(names)


def test_determinism():
    """Requirement 2.2.2: bit-identical on repeated runs."""
    outcome = _make_outcome()
    report = Report(
        summary="hash compared. reproducibility confirmed.",
        claims=(_make_high_confidence_claim(),),
    )
    v1 = HeuristicVerifier().verify(outcome, report)
    v2 = HeuristicVerifier().verify(outcome, report)
    assert v1.equals(v2)
    assert v1.model_dump_json() == v2.model_dump_json()


def test_overall_is_mean():
    """Requirement 3.1.2."""
    outcome = _make_outcome()
    report = Report(
        summary="hash compared. reproducibility confirmed.",
        claims=(_make_high_confidence_claim(),),
    )
    v = HeuristicVerifier().verify(outcome, report)
    expected = round(sum(d.score for d in v.dimensions) / len(v.dimensions), 1)
    assert v.overall == expected


def test_evidence_dedup():
    """Requirement 4.3.1."""
    outcome = _make_outcome()
    report = Report(
        summary="hash compared. reproducibility confirmed.",
        claims=(_make_high_confidence_claim(), _make_high_confidence_claim()),
    )
    v = HeuristicVerifier().verify(outcome, report)
    urls = [str(c.url) for c in v.evidence]
    assert len(urls) == len(set(urls))


def test_overconfident_claim_caught():
    """Section 5.2.1: high label with weak sourcing."""
    outcome = _make_outcome()
    weak = Claim(
        statement="Reproducibility holds in general.",
        confidence=Confidence.HIGH,
        citations=(
            Citation(
                url="https://example.com/blog-post",
                title="A blog post",
                accessed=date(2026, 5, 21),
                kind=SourceKind.SECONDARY,
            ),
        ),
    )
    report = Report(summary="hash compared.", claims=(weak,))
    v = HeuristicVerifier().verify(outcome, report)
    calib = next(d for d in v.dimensions if d.name == "confidence_calibration")
    assert calib.score < 5
