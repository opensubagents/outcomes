# open-outcome (Python)

Reference Python SDK for the [Open Outcome](../specification/README.md)
specification — declare outcomes, verify reports, grade results.

[![status: experimental](https://img.shields.io/static/v1?label=Status&message=experimental&color=orange)](../MATURITY.md)
[![spec: v0.1.0](https://img.shields.io/static/v1?label=Spec&message=v0.1.0&color=blue)](../specification/README.md)

## Install

```sh
# From a checkout
pip install -e '.[dev]'
```

The package is not yet on PyPI; the v0.1 release is meant to be installed
from source.

## Quickstart

```python
from datetime import date
from open_outcome import (
    OutcomeDeclaration,
    Claim,
    Citation,
    Confidence,
    HeuristicVerifier,
    Report,
    SourceKind,
)

outcome = OutcomeDeclaration(
    title="Will the deploy be reproducible?",
    as_of=date(2026, 5, 21),
    question="Does the build produce byte-identical artifacts from the same source?",
    success_criteria=["A hash comparison is performed", "Any drift is explained"],
)

report = Report(
    summary="The build is reproducible. The CI hash matches the local hash.",
    claims=[
        Claim(
            statement="The CI artifact hash equals the local artifact hash.",
            confidence=Confidence.HIGH,
            citations=[
                Citation(
                    url="https://example.com/ci/run/1234",
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
            ],
        ),
    ],
)

verdict = HeuristicVerifier().verify(outcome, report)
print(verdict.overall)
print(verdict.to_otel_attributes())
```

## API surface

| Symbol | Purpose |
|---|---|
| `OutcomeDeclaration` | The outcome (section 1 of the spec). |
| `Report`, `Claim`, `Citation`, `Confidence`, `SourceKind` | Inputs to the verifier (section 4). |
| `Verdict`, `DimensionScore` | The graded result (section 3). |
| `Verifier` (Protocol), `HeuristicVerifier` | Verifier interface and reference impl (section 2). |
| `verdict_to_span_attributes(verdict)` | OTel projection (section 6 / appendix B). |
| `validate_outcome_dict(data)`, `validate_verdict_dict(data)` | Conformance helpers backed by the JSON schemas. |

## Layout

```
sdk-python/
├── pyproject.toml
├── open_outcome/
│   ├── __init__.py             # public surface
│   ├── outcome.py              # OutcomeDeclaration
│   ├── evidence.py             # Citation, Claim, Confidence, SourceKind
│   ├── report.py               # Report (input to the verifier)
│   ├── verdict.py              # Verdict, DimensionScore
│   ├── verifier.py             # Verifier Protocol + HeuristicVerifier
│   ├── otel.py                 # verdict_to_span_attributes
│   ├── conformance.py          # JSON Schema validators
│   └── schemas/                # bundled spec schemas (read-only at runtime)
│       ├── outcome.schema.json
│       ├── verdict.schema.json
│       └── evidence.schema.json
└── tests/
    ├── test_outcome_schema.py
    ├── test_verifier.py
    ├── test_otel.py
    └── test_conformance.py
```

The bundled schemas under `open_outcome/schemas/` are copies of the
canonical schemas in [`../schema/`](../schema/) (the SDK packages them so
applications don't need to fetch them at runtime). They are kept in sync
by a CI check.

## Conformance

This SDK targets Open Outcome **v0.1.0**. Conformance terms are described
in [appendix C](../specification/appendix-c-conformance.md).
