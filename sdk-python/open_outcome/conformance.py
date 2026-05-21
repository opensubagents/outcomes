"""JSON Schema validation helpers backed by the bundled spec schemas.

The schemas under ``open_outcome/schemas/`` are copies of the canonical
schemas in ``../../schema/``. They are validated against the canonical
copies in tests so a CI mismatch will fail the build.
"""
from __future__ import annotations

import json
from functools import lru_cache
from importlib import resources

import jsonschema
from referencing import Registry, Resource

SPEC_VERSION = "0.1.0"


@lru_cache(maxsize=None)
def _load_schema(name: str) -> dict:
    text = (resources.files("open_outcome") / "schemas" / name).read_text(
        encoding="utf-8"
    )
    return json.loads(text)


def outcome_schema() -> dict:
    return _load_schema("outcome.schema.json")


def verdict_schema() -> dict:
    return _load_schema("verdict.schema.json")


def evidence_schema() -> dict:
    return _load_schema("evidence.schema.json")


@lru_cache(maxsize=None)
def _registry() -> Registry:
    """Registry containing all three schemas, keyed by their $id."""
    resources_ = []
    for fn in (outcome_schema, verdict_schema, evidence_schema):
        s = fn()
        resources_.append((s["$id"], Resource.from_contents(s)))
    return Registry().with_resources(resources_)


def _validator_for(schema: dict) -> jsonschema.Validator:
    cls = jsonschema.validators.validator_for(schema)
    cls.check_schema(schema)
    return cls(
        schema,
        format_checker=jsonschema.FormatChecker(),
        registry=_registry(),
    )


def validate_outcome_dict(data: dict) -> None:
    """Raise ``jsonschema.ValidationError`` if ``data`` is not a valid outcome.

    See Requirement 2.3.1: verifiers MUST raise rather than degrade.
    """
    _validator_for(outcome_schema()).validate(data)


def validate_verdict_dict(data: dict) -> None:
    """Raise ``jsonschema.ValidationError`` if ``data`` is not a valid verdict."""
    _validator_for(verdict_schema()).validate(data)
