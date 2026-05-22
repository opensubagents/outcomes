"""Command-line entrypoint for the reference HeuristicVerifier.

Used by the ``outcome-gate`` CI workflow to score an outcome+report pair
attached to a pull request. Deterministic, no network, no LLM.

Exit codes:
    0 — verdict.overall >= floor
    1 — verdict.overall <  floor
    2 — input could not be parsed or did not conform to the schema
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema
from pydantic import ValidationError

from .conformance import validate_outcome_dict
from .outcome import OutcomeDeclaration
from .report import Report
from .verifier import REFERENCE_VERIFIER_ID, HeuristicVerifier


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"outcome-gate: failed to read {path}: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


def _verify(outcome_path: Path, report_path: Path, floor: float, summary_md: Path | None) -> int:
    outcome_data = _load_json(outcome_path)
    report_data = _load_json(report_path)

    try:
        validate_outcome_dict(outcome_data)
        outcome = OutcomeDeclaration(**outcome_data)
        report = Report.model_validate(report_data)
    except (jsonschema.ValidationError, ValidationError, TypeError, ValueError) as exc:
        print(f"outcome-gate: schema error: {exc}", file=sys.stderr)
        return 2

    verdict = HeuristicVerifier().verify(outcome, report)

    if verdict.verifier_id != REFERENCE_VERIFIER_ID:
        print(
            f"outcome-gate: refusing non-reference verifier_id {verdict.verifier_id!r}; "
            f"the gate is the deterministic heuristic only",
            file=sys.stderr,
        )
        return 2

    print(json.dumps(verdict.to_jsonable(), separators=(",", ":")))

    if summary_md is not None:
        slug = outcome_path.stem.removesuffix(".outcome")
        row = "| {slug} | {overall} | {floor} | {status} | {dims} |\n".format(
            slug=slug,
            overall=verdict.overall,
            floor=floor,
            status="pass" if verdict.overall >= floor else "**FAIL**",
            dims=" / ".join(f"{d.name[:3]}={d.score}" for d in verdict.dimensions),
        )
        with summary_md.open("a", encoding="utf-8") as fh:
            fh.write(row)

    if verdict.overall < floor:
        print(
            f"outcome-gate: overall {verdict.overall} < floor {floor} for "
            f"{outcome_path.name}",
            file=sys.stderr,
        )
        return 1

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="open-outcome", description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    verify = sub.add_parser("verify", help="score an outcome+report pair")
    verify.add_argument("outcome", type=Path, help="path to outcome JSON")
    verify.add_argument("report", type=Path, help="path to report JSON")
    verify.add_argument(
        "--floor",
        type=float,
        default=3.5,
        help="minimum verdict.overall required to pass (default 3.5)",
    )
    verify.add_argument(
        "--summary-md",
        type=Path,
        default=None,
        help="append a one-row markdown table for $GITHUB_STEP_SUMMARY",
    )

    args = parser.parse_args(argv)

    if args.cmd == "verify":
        return _verify(args.outcome, args.report, args.floor, args.summary_md)

    parser.error(f"unknown command {args.cmd!r}")
    return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
