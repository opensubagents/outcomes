"""Citations, claims, and the confidence / source-kind enums.

Implements Section 4 (Evidence) and Section 5 (Confidence Calibration) of
the Open Outcome spec.
"""
from __future__ import annotations

from datetime import date
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator


class Confidence(str, Enum):
    """Calibrated confidence labels.

    Calibration thresholds are normative in
    ``specification/sections/05-confidence.md``:

    * ``HIGH`` — at least 2 independent primary citations OR 1
      vendor-authoritative primary citation.
    * ``MEDIUM`` — at least 1 primary citation OR at least 2 citations of
      kind in {primary, secondary}.
    * ``LOW`` — any single citation, or no citations when the claim is an
      explicit inference.
    """

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class SourceKind(str, Enum):
    """Coarse classification of a citation source.

    * ``PRIMARY`` — vendor docs, source code, RFCs, authoritative artifacts.
    * ``SECONDARY`` — reputable third-party explanations (engineering blogs).
    * ``COMMUNITY`` — forums, social media, crowd-sourced content.
    """

    PRIMARY = "primary"
    SECONDARY = "secondary"
    COMMUNITY = "community"


class Citation(BaseModel):
    """A reference to a source supporting a claim. Section 4.1."""

    model_config = ConfigDict(frozen=True)

    url: HttpUrl
    title: str = Field(min_length=1)
    accessed: date
    kind: SourceKind
    quote: str | None = Field(default=None)


class Claim(BaseModel):
    """A single assertion produced by an agent run. Section 4.2."""

    model_config = ConfigDict(frozen=True)

    statement: str = Field(min_length=1)
    confidence: Confidence
    citations: tuple[Citation, ...] = Field(default_factory=tuple)
    caveats: str | None = None

    @model_validator(mode="after")
    def _require_citations_unless_low(self) -> "Claim":
        if self.confidence != Confidence.LOW and not self.citations:
            raise ValueError(
                "non-low confidence claim must cite at least one source: "
                f"{self.statement!r}"
            )
        return self
