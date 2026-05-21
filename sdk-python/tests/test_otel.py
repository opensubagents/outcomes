"""OTel attribute projection (Section 6, appendix B)."""
from __future__ import annotations

from datetime import date

from open_outcome import (
    Citation,
    Claim,
    Confidence,
    HeuristicVerifier,
    OutcomeDeclaration,
    Report,
    SourceKind,
    verdict_to_span_attributes,
)
from open_outcome.otel import SPAN_NAME


def _verdict_for_tests():
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
    report = Report(summary="one. two. three.", claims=(claim,))
    return HeuristicVerifier().verify(outcome, report)


def test_required_attributes_present():
    """Requirement 6.1.1."""
    v = _verdict_for_tests()
    a = verdict_to_span_attributes(v)
    assert a["gen_ai.outcome.spec_version"] == "0.1.0"
    assert isinstance(a["gen_ai.outcome.overall"], float)
    assert a["gen_ai.outcome.dimension_count"] == 5
    assert a["gen_ai.outcome.evidence_count"] == 2
    assert a["gen_ai.outcome.verifier_id"] == "open-outcome.python.heuristic"


def test_per_dimension_attributes():
    """Requirement 6.1.2."""
    v = _verdict_for_tests()
    a = verdict_to_span_attributes(v)
    for d in v.dimensions:
        key = f"gen_ai.outcome.dimension.{d.name}.score"
        assert key in a
        assert a[key] == d.score


def test_span_name_constant():
    """Requirement 6.2.1."""
    assert SPAN_NAME == "verify_outcome"


def test_evidence_array_not_inlined():
    """Requirement 6.1.3: evidence is not put on the span as a single attribute."""
    v = _verdict_for_tests()
    a = verdict_to_span_attributes(v)
    assert "gen_ai.outcome.evidence" not in a
