"""End-to-end CI check: research-engineering report parity with Open Outcome.

The test runs ``run.py`` as a subprocess and asserts:
1. ``run.py`` exits 0 (parity holds; verdict validates against the schema).
2. ``outcome.json`` and ``verdict.json`` were written to disk.
3. The written verdict satisfies ``schema/verdict.schema.json`` (the
   conformance check is what makes this directory the spec's acceptance
   test).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from open_outcome.conformance import (
    validate_outcome_dict,
    validate_verdict_dict,
)

HERE = Path(__file__).resolve().parent
EXAMPLE_DIR = HERE.parent
RUN_PY = EXAMPLE_DIR / "run.py"


def test_run_py_exits_zero():
    result = subprocess.run(
        [sys.executable, str(RUN_PY)],
        cwd=EXAMPLE_DIR,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert "parity: OK" in result.stdout


def test_outcome_and_verdict_written_and_valid():
    outcome_path = EXAMPLE_DIR / "outcome.json"
    verdict_path = EXAMPLE_DIR / "verdict.json"
    assert outcome_path.exists(), "run.py should have written outcome.json"
    assert verdict_path.exists(), "run.py should have written verdict.json"
    validate_outcome_dict(json.loads(outcome_path.read_text()))
    validate_verdict_dict(json.loads(verdict_path.read_text()))
