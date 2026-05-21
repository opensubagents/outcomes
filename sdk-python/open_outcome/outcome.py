"""OutcomeDeclaration — what should be true after an agent runs.

Implements Section 1 of the Open Outcome spec. The model is frozen so that
``Verifier.verify(...)`` cannot mutate the outcome it receives
(Requirement 1.3.1, Requirement 2.1.3).
"""
from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class OutcomeDeclaration(BaseModel):
    """A typed description of what should be true after an agent run."""

    model_config = ConfigDict(frozen=True)

    title: str = Field(min_length=1, description="Requirement 1.1.1")
    as_of: date = Field(description="Requirement 1.1.2")
    question: str = Field(min_length=1, description="Requirement 1.1.3")
    success_criteria: tuple[str, ...] = Field(
        min_length=1, description="Requirement 1.1.4"
    )
    archetype: str | None = Field(default=None, description="Requirement 1.2.1")
    archetype_fields: dict[str, object] | None = Field(
        default=None, description="Requirement 1.2.2"
    )
    requester: str | None = None
