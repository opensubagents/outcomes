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


def test_citation_staleness_downgrades_quality():
    """D5: majority-stale citations drop citation_quality by one."""
    outcome = _make_outcome()
    stale_claim = Claim(
        statement="The CI artifact hash equals the local hash.",
        confidence=Confidence.HIGH,
        citations=(
            Citation(
                url="https://example.com/ci-run-1234",
                title="CI run #1234",
                accessed=date(2024, 1, 1),  # >180 days old at test time
                kind=SourceKind.PRIMARY,
            ),
            Citation(
                url="https://example.com/local-build-log",
                title="Local build log",
                accessed=date(2024, 1, 1),  # >180 days old at test time
                kind=SourceKind.PRIMARY,
            ),
        ),
    )
    report = Report(summary="hash compared.", claims=(stale_claim,))
    v = HeuristicVerifier().verify(outcome, report)
    cq = next(d for d in v.dimensions if d.name == "citation_quality")
    # 2/2 primary would normally score 5; majority-stale downgrades by 1.
    assert cq.score == 4
    assert "stale" in cq.justification


def test_citation_staleness_floor_at_one():
    """D5: staleness cannot drop a score below the floor of 1."""
    outcome = _make_outcome()
    stale_community = Claim(
        statement="Stale community evidence only.",
        confidence=Confidence.LOW,
        citations=(
            Citation(
                url="https://reddit.com/r/x/1",
                title="r1",
                accessed=date(2024, 1, 1),
                kind=SourceKind.COMMUNITY,
            ),
        ),
    )
    report = Report(summary="x.", claims=(stale_community,))
    v = HeuristicVerifier().verify(outcome, report)
    cq = next(d for d in v.dimensions if d.name == "citation_quality")
    # Base score 1 (community-only); staleness must not drop it below 1.
    assert cq.score == 1


def test_citation_staleness_fresh_no_downgrade():
    """D5: fresh citations do not trigger the downgrade."""
    outcome = _make_outcome()
    fresh_claim = _make_high_confidence_claim()  # accessed 2026-05-21, fresh
    report = Report(summary="hash compared.", claims=(fresh_claim,))
    v = HeuristicVerifier().verify(outcome, report)
    cq = next(d for d in v.dimensions if d.name == "citation_quality")
    assert cq.score == 5
    assert "stale" not in cq.justification
