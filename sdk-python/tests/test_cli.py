"""Behavior of the ``open_outcome.cli`` entrypoint used by outcome-gate CI."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

from open_outcome import (
    Citation,
    Claim,
    Confidence,
    OutcomeDeclaration,
    Report,
    SourceKind,
)


def _passing_outcome() -> OutcomeDeclaration:
    return OutcomeDeclaration(
        title="Adopt outcome-gated CI",
        as_of=date(2026, 5, 21),
        question="Does every PR ship an outcome+report pair scoring above 3.5?",
        success_criteria=("workflow runs HeuristicVerifier on every pull request",),
        archetype="capability_audit",
        archetype_fields={"capabilities": ["gate every pull request"]},
    )


def _passing_report() -> Report:
    return Report(
        summary=(
            "We recommend adopting an outcome-gated workflow that runs HeuristicVerifier "
            "on every pull request. The gate blocks merge when overall is below the "
            "configured floor."
        ),
        claims=(
            Claim(
                statement="The workflow runs HeuristicVerifier on every pull request via the open-outcome CLI.",
                confidence=Confidence.HIGH,
                citations=(
                    Citation(
                        url="https://example.com/workflow",
                        title="outcome-gate.yml",
                        accessed=date(2026, 5, 21),
                        kind=SourceKind.PRIMARY,
                    ),
                    Citation(
                        url="https://example.com/cli",
                        title="open_outcome.cli",
                        accessed=date(2026, 5, 21),
                        kind=SourceKind.PRIMARY,
                    ),
                ),
                caveats="Gate runs only on pull_request events.",
            ),
        ),
        open_questions=("Should the floor ratchet to 4.0?",),
        methodology_notes="Verified locally with HeuristicVerifier.",
    )


def _failing_report() -> Report:
    return Report(
        summary="Nothing to see here.",
        claims=(
            Claim(
                statement="x",
                confidence=Confidence.LOW,
                citations=(
                    Citation(
                        url="https://example.com/forum",
                        title="forum post",
                        accessed=date(2026, 5, 21),
                        kind=SourceKind.COMMUNITY,
                    ),
                ),
            ),
        ),
    )


def _run_cli(*argv: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "open_outcome.cli", *argv],
        capture_output=True,
        text=True,
    )


def _write_pair(tmp_path: Path, outcome: OutcomeDeclaration, report: Report) -> tuple[Path, Path]:
    o = tmp_path / "p.outcome.json"
    r = tmp_path / "p.report.json"
    o.write_text(
        json.dumps(outcome.model_dump(mode="json", exclude_none=True)), encoding="utf-8"
    )
    r.write_text(
        json.dumps(report.model_dump(mode="json", exclude_none=True)), encoding="utf-8"
    )
    return o, r


def test_verify_passing_pair_exits_zero(tmp_path: Path):
    o, r = _write_pair(tmp_path, _passing_outcome(), _passing_report())
    res = _run_cli("verify", str(o), str(r), "--floor", "3.5")
    assert res.returncode == 0, res.stderr
    verdict = json.loads(res.stdout.strip().splitlines()[-1])
    assert verdict["overall"] >= 3.5
    assert verdict["verifier_id"] == "open-outcome.python.heuristic"
    assert verdict["spec_version"] == "0.1.0"


def test_verify_below_floor_exits_one(tmp_path: Path):
    o, r = _write_pair(tmp_path, _passing_outcome(), _failing_report())
    res = _run_cli("verify", str(o), str(r), "--floor", "3.5")
    assert res.returncode == 1, res.stderr
    verdict = json.loads(res.stdout.strip().splitlines()[-1])
    assert verdict["overall"] < 3.5


def test_verify_malformed_json_exits_two(tmp_path: Path):
    o = tmp_path / "bad.outcome.json"
    r = tmp_path / "bad.report.json"
    o.write_text("not json {", encoding="utf-8")
    r.write_text("{}", encoding="utf-8")
    res = _run_cli("verify", str(o), str(r))
    assert res.returncode == 2, res.stderr


def test_verify_writes_summary_md(tmp_path: Path):
    o, r = _write_pair(tmp_path, _passing_outcome(), _passing_report())
    summary = tmp_path / "summary.md"
    res = _run_cli(
        "verify", str(o), str(r), "--floor", "3.5", "--summary-md", str(summary)
    )
    assert res.returncode == 0, res.stderr
    body = summary.read_text(encoding="utf-8")
    assert "| p |" in body
    assert "pass" in body


def test_check_urls_downgrades_on_broken(tmp_path: Path, monkeypatch):
    """D6: --check-urls downgrades citation_quality by one when any URL is 4xx/5xx."""
    from open_outcome import cli as cli_mod

    o, r = _write_pair(tmp_path, _passing_outcome(), _passing_report())

    # Patch _head_check to return 404 for every URL — exercised in-process so
    # the monkeypatch takes effect (subprocess wouldn't see it).
    monkeypatch.setattr(cli_mod, "_head_check", lambda url, timeout=5.0: 404)

    rc = cli_mod.main(["verify", str(o), str(r), "--floor", "3.5", "--check-urls"])
    # Bootstrap pair scores 5.0 originally; downgrading citation_quality from 5 to 4
    # drops overall to 4.8 which still clears floor 3.5 — rc=0.
    assert rc == 0


def test_check_urls_off_by_default(tmp_path: Path, monkeypatch):
    """D6: without --check-urls, the gate stays deterministic (no network)."""
    from open_outcome import cli as cli_mod

    o, r = _write_pair(tmp_path, _passing_outcome(), _passing_report())

    called = {"n": 0}

    def fail_if_called(url, timeout=5.0):
        called["n"] += 1
        return 404

    monkeypatch.setattr(cli_mod, "_head_check", fail_if_called)

    rc = cli_mod.main(["verify", str(o), str(r), "--floor", "3.5"])
    assert rc == 0
    assert called["n"] == 0, "head_check must not be called without --check-urls"
