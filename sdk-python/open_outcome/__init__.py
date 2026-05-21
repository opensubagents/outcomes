"""open-outcome: reference Python SDK for the Open Outcome specification.

This package provides typed models for the three shapes the spec defines —
``OutcomeDeclaration``, ``Report``, and ``Verdict`` — plus a deterministic
``HeuristicVerifier`` and an OpenTelemetry projection.

The package is the conformance reference for the spec at
``../specification/README.md``: bugs that disagree with the prose spec are
treated as SDK bugs, not as spec bugs.
"""
from __future__ import annotations

from .evidence import Citation, Claim, Confidence, SourceKind
from .otel import verdict_to_span_attributes
from .outcome import OutcomeDeclaration
from .report import Report
from .verdict import DimensionScore, Verdict
from .verifier import HeuristicVerifier, Verifier
from .conformance import (
    SPEC_VERSION,
    validate_outcome_dict,
    validate_verdict_dict,
)

__all__ = [
    "Citation",
    "Claim",
    "Confidence",
    "DimensionScore",
    "HeuristicVerifier",
    "OutcomeDeclaration",
    "Report",
    "SPEC_VERSION",
    "SourceKind",
    "Verdict",
    "Verifier",
    "validate_outcome_dict",
    "validate_verdict_dict",
    "verdict_to_span_attributes",
]
