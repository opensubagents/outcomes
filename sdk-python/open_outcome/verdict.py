"""Verdict and DimensionScore.

Implements Section 3 (Verdict) of the Open Outcome spec.
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .evidence import Citation


class DimensionScore(BaseModel):
    """One dimension of a verdict. Section 3.1.1 / 3.3.2."""

    model_config = ConfigDict(frozen=True)

    name: str = Field(min_length=1)
    score: int = Field(ge=1, le=5)
    justification: str = Field(min_length=1)


class Verdict(BaseModel):
    """The graded result a verifier returns. Section 3."""

    model_config = ConfigDict(frozen=True)

    spec_version: str = Field(
        pattern=r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$",
        description="Requirement 3.1.3",
    )
    dimensions: tuple[DimensionScore, ...] = Field(
        min_length=1, description="Requirement 3.1.1"
    )
    overall: float = Field(ge=1.0, le=5.0, description="Requirement 3.1.2")
    evidence: tuple[Citation, ...] = Field(
        default_factory=tuple, description="Requirement 3.1.4"
    )
    notes: str | None = Field(default=None, description="Requirement 3.2.1")
    verifier_id: str | None = Field(default=None, description="Requirement 3.2.2")

    @model_validator(mode="after")
    def _check_dimension_names_unique(self) -> "Verdict":
        names = [d.name for d in self.dimensions]
        if len(set(names)) != len(names):
            raise ValueError(
                f"verdict dimensions must have unique names (Requirement 3.3.1): {names!r}"
            )
        return self

    @model_validator(mode="after")
    def _check_overall_is_mean(self) -> "Verdict":
        expected = round(sum(d.score for d in self.dimensions) / len(self.dimensions), 1)
        if abs(self.overall - expected) > 1e-9:
            raise ValueError(
                f"overall {self.overall} is not the mean of dimension scores "
                f"({expected}); see Requirement 3.1.2"
            )
        return self

    @model_validator(mode="after")
    def _check_evidence_dedup(self) -> "Verdict":
        urls = [str(c.url) for c in self.evidence]
        if len(set(urls)) != len(urls):
            raise ValueError(
                "verdict evidence must be deduplicated by URI (Requirement 4.3.1)"
            )
        return self

    def equals(self, other: "Verdict") -> bool:
        """Verdict equality per Requirement 3.4.1."""
        if self.spec_version != other.spec_version:
            return False
        if abs(self.overall - other.overall) > 1e-9:
            return False
        a = {(d.name, d.score, d.justification) for d in self.dimensions}
        b = {(d.name, d.score, d.justification) for d in other.dimensions}
        if a != b:
            return False
        au = {str(c.url) for c in self.evidence}
        bu = {str(c.url) for c in other.evidence}
        return au == bu

    def to_jsonable(self) -> dict:
        """Wire-format dict that validates against ``verdict.schema.json``.

        Absent optional fields are omitted (not serialized as ``null``) and
        URL objects are coerced to strings. This is the form to send across
        process boundaries or to persist alongside a report.
        """
        return self.model_dump(mode="json", exclude_none=True)
