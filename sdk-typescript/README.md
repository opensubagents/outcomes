# @opensubagents/open-outcome (TypeScript)

Reference TypeScript SDK for the [Open Outcome](../specification/README.md)
specification — declare outcomes, verify reports, grade results.

[![status: experimental](https://img.shields.io/static/v1?label=Status&message=experimental&color=orange)](../MATURITY.md)
[![spec: v0.1.0](https://img.shields.io/static/v1?label=Spec&message=v0.1.0&color=blue)](../specification/README.md)

## Install

The package is not yet on npm; the v0.1 release is meant to be consumed
from source.

```sh
cd sdk-typescript
pnpm install
pnpm test
```

## Quickstart

```ts
import {
  OutcomeDeclaration,
  HeuristicVerifier,
  Confidence,
  SourceKind,
  verdictToSpanAttributes,
} from "@opensubagents/open-outcome";

const outcome: OutcomeDeclaration = {
  title: "Will the deploy be reproducible?",
  as_of: "2026-05-21",
  question: "Does the build produce byte-identical artifacts from the same source?",
  success_criteria: ["A hash comparison is performed", "Any drift is explained"],
};

const report = {
  summary: "The build is reproducible. The CI hash matches the local hash.",
  claims: [
    {
      statement: "The CI artifact hash equals the local artifact hash.",
      confidence: Confidence.HIGH,
      citations: [
        { url: "https://example.com/ci/run/1234", title: "CI run #1234", accessed: "2026-05-21", kind: SourceKind.PRIMARY },
        { url: "https://example.com/local-build-log", title: "Local build log", accessed: "2026-05-21", kind: SourceKind.PRIMARY },
      ],
    },
  ],
};

const verdict = new HeuristicVerifier().verify(outcome, report);
console.log(verdict.overall);
console.log(verdictToSpanAttributes(verdict));
```

## Parity with the Python SDK

This SDK implements the **same `HeuristicVerifier` algorithm** as the Python
SDK. Each SDK's test suite includes shared fixtures so both implementations
produce equal verdicts on the same input.

## Layout

```
sdk-typescript/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts
│   ├── outcome.ts
│   ├── evidence.ts
│   ├── report.ts
│   ├── verdict.ts
│   ├── verifier.ts
│   ├── otel.ts
│   └── conformance.ts
├── schemas/                # bundled spec schemas
└── test/
    ├── outcome.test.ts
    ├── verifier.test.ts
    ├── otel.test.ts
    └── conformance.test.ts
```
