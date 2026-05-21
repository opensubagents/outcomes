"""Verifier interface and the reference HeuristicVerifier.

Implements Section 2 (Verifier) of the Open Outcome spec.

``HeuristicVerifier`` ports the algorithm of
``research_engineering.harness.grader.HeuristicGrader`` one-to-one so the
``examples/research-engineering/`` end-to-end can assert byte-level parity
between the two implementations.
"""
from __future__ import annotations

from collections import Counter
from typing import Protocol

from .conformance import SPEC_VERSION
from .evidence import Confidence, SourceKind
from .outcome import OutcomeDeclaration
from .report import Report
from .verdict import DimensionScore, Verdict


REFERENCE_VERIFIER_ID = "open-outcome.python.heuristic"


class Verifier(Protocol):
    """A verifier consumes an outcome plus a report and returns a verdict.

    Implementations MUST be pure with respect to their inputs (Requirement
    2.1.2) and MUST NOT mutate the outcome (Requirement 2.1.3).
    """

    def verify(self, outcome: OutcomeDeclaration, report: Report) -> Verdict:
        ...


class HeuristicVerifier:
    """Deterministic verifier with no network and no LLM. Section 2.2.

    Ports the per-dimension scoring methods from research-engineering's
    ``HeuristicGrader`` verbatim so the verdicts agree byte-for-byte on
    the same input.
    """

    def verify(self, outcome: OutcomeDeclaration, report: Report) -> Verdict:
        dimensions: tuple[DimensionScore, ...] = (
            self._score_confidence_calibration(report),
            self._score_citation_quality(report),
            self._score_coverage(outcome, report),
            self._score_decision_usefulness(report),
            self._score_clarity(report),
        )
        overall = round(sum(d.score for d in dimensions) / len(dimensions), 1)
        return Verdict(
            spec_version=SPEC_VERSION,
            dimensions=dimensions,
            overall=overall,
            evidence=report.all_citations(),
            notes="HeuristicVerifier (no LLM)",
            verifier_id=REFERENCE_VERIFIER_ID,
        )

    @staticmethod
    def _score_confidence_calibration(report: Report) -> DimensionScore:
        violations: list[str] = []
        for claim in report.claims:
            primary = sum(1 for c in claim.citations if c.kind == SourceKind.PRIMARY)
            reputable = sum(
                1
                for c in claim.citations
                if c.kind in (SourceKind.PRIMARY, SourceKind.SECONDARY)
            )
            if claim.confidence == Confidence.HIGH and primary < 2:
                violations.append(
                    f"high-confidence claim has {primary} primary source(s): "
                    f"{claim.statement[:60]}..."
                )
            elif (
                claim.confidence == Confidence.MEDIUM
                and primary < 1
                and reputable < 2
            ):
                violations.append(
                    f"medium-confidence claim has weak sourcing: "
                    f"{claim.statement[:60]}..."
                )
            elif claim.confidence == Confidence.LOW and primary >= 2:
                violations.append(
                    f"low-confidence claim is well-sourced (under-calibrated): "
                    f"{claim.statement[:60]}..."
                )
        n = len(report.claims)
        ratio = (n - len(violations)) / n if n else 0.0
        score = 1 + round(ratio * 4)
        justification = (
            "all claims calibrated"
            if not violations
            else f"{len(violations)}/{n} miscalibrated: " + "; ".join(violations[:2])
        )
        return DimensionScore(
            name="confidence_calibration",
            score=score,
            justification=justification,
        )

    @staticmethod
    def _score_citation_quality(report: Report) -> DimensionScore:
        cits = report.all_citations()
        if not cits:
            return DimensionScore(
                name="citation_quality",
                score=1,
                justification="report has no citations",
            )
        kinds = Counter(c.kind for c in cits)
        primary_share = kinds[SourceKind.PRIMARY] / len(cits)
        if primary_share >= 0.5:
            score, just = 5, f"{kinds[SourceKind.PRIMARY]}/{len(cits)} primary"
        elif primary_share >= 0.25:
            score, just = 4, f"{kinds[SourceKind.PRIMARY]}/{len(cits)} primary"
        elif kinds[SourceKind.PRIMARY] >= 1:
            score, just = 3, "at least one primary, mostly secondary"
        elif kinds[SourceKind.SECONDARY] >= 1:
            score, just = 2, "secondary only"
        else:
            score, just = 1, "community-only sourcing"
        return DimensionScore(
            name="citation_quality",
            score=score,
            justification=just,
        )

    @staticmethod
    def _score_coverage(
        outcome: OutcomeDeclaration, report: Report
    ) -> DimensionScore:
        required: list[str] = list(outcome.success_criteria)
        af = outcome.archetype_fields or {}
        if outcome.archetype == "vendor_comparison":
            required += list(af.get("dimensions", []))
        elif outcome.archetype == "deep_dive":
            required += list(af.get("angles", []))
        elif outcome.archetype == "capability_audit":
            required += list(af.get("capabilities", []))
        if not required:
            return DimensionScore(
                name="coverage",
                score=3,
                justification="outcome specifies no explicit coverage requirements",
            )
        haystack = " ".join(c.statement.lower() for c in report.claims)
        hits = sum(
            1
            for r in required
            if any(tok in haystack for tok in str(r).lower().split())
        )
        ratio = hits / len(required)
        score = 1 + round(ratio * 4)
        return DimensionScore(
            name="coverage",
            score=score,
            justification=f"{hits}/{len(required)} required axes mentioned",
        )

    @staticmethod
    def _score_decision_usefulness(report: Report) -> DimensionScore:
        signals = 0
        if report.open_questions:
            signals += 1
        if any(c.caveats for c in report.claims):
            signals += 1
        if report.methodology_notes:
            signals += 1
        if any(
            word in report.summary.lower()
            for word in ("recommend", "choose", "prefer", "avoid", "tradeoff")
        ):
            signals += 1
        score = max(1, min(5, 1 + signals))
        return DimensionScore(
            name="decision_usefulness",
            score=score,
            justification=f"{signals}/4 decision signals present",
        )

    @staticmethod
    def _score_clarity(report: Report) -> DimensionScore:
        sentences = [s for s in report.summary.replace("!", ".").split(".") if s.strip()]
        n = len(sentences)
        if 2 <= n <= 4:
            score, just = 5, f"summary is {n} sentences"
        elif n == 1 or n == 5:
            score, just = 3, f"summary is {n} sentence(s) — outside 2-4 ideal"
        else:
            score, just = 2, f"summary is {n} sentences"
        return DimensionScore(
            name="clarity",
            score=score,
            justification=just,
        )
