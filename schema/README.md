# Schemas

This directory contains the JSON Schemas that are the machine-checkable form
of the [Open Outcome specification](../specification/README.md). The schemas
are normative: any conflict between the prose spec and the schemas is a bug
that needs an issue and a fix.

## Files

| File | What it validates |
|---|---|
| [`outcome.schema.json`](./outcome.schema.json) | An [outcome declaration](../specification/sections/01-outcome-declaration.md). |
| [`verdict.schema.json`](../schema/verdict.schema.json) | A [verdict](../specification/sections/03-verdict.md) returned by a verifier. |
| [`evidence.schema.json`](./evidence.schema.json) | A [citation](../specification/sections/04-evidence.md) or [claim](../specification/glossary.md#claim); referenced by `outcome` and `verdict`. |

## Using the schemas

### Python

```python
import json, jsonschema
from importlib import resources

outcome_schema = json.loads(
    (resources.files("open_outcome") / "schemas" / "outcome.schema.json").read_text()
)
jsonschema.validate(instance=my_outcome_dict, schema=outcome_schema)
```

The reference Python SDK provides higher-level helpers in
[`open_outcome.conformance`](../sdk-python/open_outcome/conformance.py).

### TypeScript

```ts
import { validateOutcome } from "@opensubagents/open-outcome";
const result = validateOutcome(myOutcomeJson);
if (!result.valid) throw new Error(result.errors.join("\n"));
```

### Command line

The CI workflow at `.github/workflows/spec-lint.yml` runs
[ajv-cli](https://github.com/ajv-validator/ajv-cli) against every schema.
You can run the same locally:

```sh
ajv compile -s schema/outcome.schema.json -c ajv-formats
ajv validate -s schema/outcome.schema.json -d 'examples/**/outcome.json' -c ajv-formats
```

## JSON Schema dialect

All schemas use [JSON Schema 2020-12](https://json-schema.org/specification-links.html#2020-12).
Schema `$id` URIs point at `https://schemas.opensubagents.org/outcome/`
namespaced paths; the URIs are stable references, not necessarily
fetchable. Implementations SHOULD bundle the schemas with the SDK rather
than fetching them at runtime.
