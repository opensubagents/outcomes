"""OpenTelemetry span attribute projection for a Verdict.

Implements Section 6 (Observability) and the proposed attribute table in
appendix B of the Open Outcome spec. The output is a plain ``dict[str,
str | int | float]`` so it can be set on a span via any OTel SDK without
this package depending on the OTel SDK itself.
"""
from __future__ import annotations

import re

from .verdict import Verdict

_SNAKE_CASE = re.compile(r"[^a-z0-9]+")


def _normalize(name: str) -> str:
    return _SNAKE_CASE.sub("_", name.lower()).strip("_")


def verdict_to_span_attributes(verdict: Verdict) -> dict[str, str | int | float]:
    """Project a Verdict onto the OTel attribute table in appendix B."""
    attrs: dict[str, str | int | float] = {
        "gen_ai.outcome.spec_version": verdict.spec_version,
        "gen_ai.outcome.overall": verdict.overall,
        "gen_ai.outcome.dimension_count": len(verdict.dimensions),
        "gen_ai.outcome.evidence_count": len(verdict.evidence),
    }
    if verdict.verifier_id:
        attrs["gen_ai.outcome.verifier_id"] = verdict.verifier_id
    for d in verdict.dimensions:
        attrs[f"gen_ai.outcome.dimension.{_normalize(d.name)}.score"] = d.score
    return attrs


SPAN_NAME = "verify_outcome"
"""The span name a verifier SHOULD use per Requirement 6.2.1."""
