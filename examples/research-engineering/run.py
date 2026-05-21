"""End-to-end: research-engineering report → Open Outcome verdict.

Loads ``report.json`` (a frozen GeneratedReport from the sibling
``opensubagents/research-engineering`` plugin), maps the brief to an
``OutcomeDeclaration``, grades the report through both ``research-
engineering``'s own ``HeuristicGrader`` and Open Outcome's
``HeuristicVerifier``, asserts the per-dimension scores agree, and prints
the OTel span attribute dict the verdict would emit.

This script is the worked example from the spec's
``specification/appendix-d-worked-example.md``, in executable form.
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

from open_outcome import (
    Citation,
    Claim,
    Confidence,
    HeuristicVerifier,
    OutcomeDeclaration,
    Report,
    SourceKind,
    Verdict,
    verdict_to_span_attributes,
)
from open_outcome.conformance import validate_outcome_dict, validate_verdict_dict

# `research_engineering` is the sibling plugin's python package — name uses
# an underscore even though the repo name uses a dash.
from research_engineering.archetypes import GeneratedReport as REReport
from research_engineering.harness.grader import default_grader as re_default_grader

HERE = Path(__file__).resolve().parent
REPORT_PATH = HERE / "report.json"
OUTCOME_PATH = HERE / "outcome.json"
VERDICT_PATH = HERE / "verdict.json"

# Mapping from the research-engineering brief archetypes to the
# archetype-specific field names this example knows to lift into
# ``OutcomeDeclaration.archetype_fields``.
ARCHETYPE_FIELDS_BY_ARCHETYPE: dict[str, tuple[str, ...]] = {
    "vendor_comparison": ("candidates", "dimensions"),
    "deep_dive": ("target", "angles"),
    "capability_audit": ("target", "capabilities"),
}


def brief_to_outcome(brief: dict[str, Any]) -> OutcomeDeclaration:
    """Map a research-engineering ``Brief`` to an Open Outcome ``OutcomeDeclaration``."""
    archetype = brief["archetype"]
    keys = ARCHETYPE_FIELDS_BY_ARCHETYPE.get(archetype, ())
    archetype_fields = {k: brief[k] for k in keys if k in brief}
    return OutcomeDeclaration(
        title=brief["title"],
        as_of=date.fromisoformat(brief["as_of"]),
        question=brief["question"],
        success_criteria=tuple(brief.get("success_criteria", []) or []),
        archetype=archetype,
        archetype_fields=archetype_fields or None,
        requester=brief.get("requester"),
    )


def report_to_open_outcome(report: dict[str, Any]) -> Report:
    """Map a research-engineering ``GeneratedReport`` dict to an Open Outcome ``Report``."""

    def _cite(c: dict[str, Any]) -> Citation:
        return Citation(
            url=c["url"],
            title=c["title"],
            accessed=date.fromisoformat(c["accessed"]),
            kind=SourceKind(c["kind"]),
            quote=c.get("quote"),
        )

    def _claim(c: dict[str, Any]) -> Claim:
        return Claim(
            statement=c["statement"],
            confidence=Confidence(c["confidence"]),
            citations=tuple(_cite(x) for x in c.get("citations", [])),
            caveats=c.get("caveats"),
        )

    return Report(
        summary=report["summary"],
        claims=tuple(_claim(c) for c in report["claims"]),
        open_questions=tuple(report.get("open_questions", []) or []),
        methodology_notes=report.get("methodology_notes"),
    )


def main() -> int:
    raw = json.loads(REPORT_PATH.read_text())

    # 1. Map.
    outcome = brief_to_outcome(raw["brief"])
    report = report_to_open_outcome(raw)

    # 2. Validate against the JSON Schemas.
    outcome_jsonable = outcome.model_dump(mode="json", exclude_none=True)
    validate_outcome_dict(outcome_jsonable)

    # 3. Grade through both implementations.
    open_outcome_verdict: Verdict = HeuristicVerifier().verify(outcome, report)
    re_grade = re_default_grader().grade(REReport.model_validate(raw))

    # 4. Persist the Open Outcome fixtures alongside the report.
    OUTCOME_PATH.write_text(json.dumps(outcome_jsonable, indent=2, sort_keys=True))
    VERDICT_PATH.write_text(
        json.dumps(open_outcome_verdict.to_jsonable(), indent=2, sort_keys=True)
    )
    validate_verdict_dict(open_outcome_verdict.to_jsonable())

    # 5. Assert parity. The Open Outcome rubric is the research-engineering
    #    rubric, so the dimension scores MUST match exactly.
    re_by_name = {s.dimension.value: s.score for s in re_grade.scores}
    oo_by_name = {d.name: d.score for d in open_outcome_verdict.dimensions}
    print("Parity check (research-engineering vs open-outcome):")
    print(f"  {'dimension':<24} {'r-e':>5}  {'o-o':>5}")
    all_match = True
    for name in oo_by_name:
        re_score = re_by_name.get(name)
        oo_score = oo_by_name[name]
        match = re_score == oo_score
        all_match = all_match and match
        marker = "✓" if match else "✗"
        print(f"  {name:<24} {re_score!s:>5}  {oo_score!s:>5}  {marker}")
    if not all_match:
        print("\nparity: FAIL", file=sys.stderr)
        return 1
    print("\nparity: OK")
    print(f"open-outcome overall: {open_outcome_verdict.overall}")
    print(f"research-engineering overall: {re_grade.overall()}")

    # 6. Print the OTel projection.
    print("\nOTel span attributes (span name = verify_outcome):")
    for k, v in verdict_to_span_attributes(open_outcome_verdict).items():
        print(f"  {k} = {v!r}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
