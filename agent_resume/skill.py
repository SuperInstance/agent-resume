"""Skill representation with proficiency levels, evidence, and endorsements."""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import date
from typing import Any


class ProficiencyLevel(enum.Enum):
    """Standardized proficiency levels for agent skills."""

    NOVICE = "novice"
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"
    MASTER = "master"

    @property
    def numeric(self) -> int:
        """Return a numeric value (1-6) for scoring."""
        return {
            ProficiencyLevel.NOVICE: 1,
            ProficiencyLevel.BEGINNER: 2,
            ProficiencyLevel.INTERMEDIATE: 3,
            ProficiencyLevel.ADVANCED: 4,
            ProficiencyLevel.EXPERT: 5,
            ProficiencyLevel.MASTER: 6,
        }[self]


@dataclass(frozen=True)
class Endorsement:
    """An endorsement from another agent or system."""

    endorser: str
    comment: str
    date: date
    weight: float = 1.0  # 0.0–1.0 confidence of the endorser

    def __post_init__(self) -> None:
        if not 0.0 <= self.weight <= 1.0:
            raise ValueError(f"weight must be between 0.0 and 1.0, got {self.weight}")


@dataclass
class Skill:
    """An agent skill with proficiency, evidence, and endorsements.

    Attributes:
        name: Human-readable skill name (e.g. "Natural Language Processing").
        category: Optional grouping category (e.g. "Language", "DevOps").
        proficiency: Current proficiency level.
        evidence: List of descriptive evidence strings supporting this skill.
        endorsements: Endorsements from other agents or systems.
        acquired_date: When the skill was first recorded.
        tags: Free-form tags for search/filter.
    """

    name: str
    category: str = ""
    proficiency: ProficiencyLevel = ProficiencyLevel.INTERMEDIATE
    evidence: list[str] = field(default_factory=list)
    endorsements: list[Endorsement] = field(default_factory=list)
    acquired_date: date | None = None
    tags: list[str] = field(default_factory=list)

    # -- derived helpers --------------------------------------------------

    @property
    def endorsement_score(self) -> float:
        """Weighted average endorsement score (0.0–1.0). Returns 0.0 if no endorsements."""
        if not self.endorsements:
            return 0.0
        total_weight = sum(e.weight for e in self.endorsements)
        if total_weight == 0:
            return 0.0
        return total_weight / len(self.endorsements)

    @property
    def combined_score(self) -> float:
        """Blend proficiency numeric (normalised to 0–1) with endorsement score."""
        prof_norm = (self.proficiency.numeric - 1) / 5.0  # 0.0–1.0
        if not self.endorsements:
            return prof_norm
        return 0.6 * prof_norm + 0.4 * self.endorsement_score

    def add_evidence(self, text: str) -> Skill:
        """Append an evidence string. Returns *self* for chaining."""
        self.evidence.append(text)
        return self

    def endorse(self, endorser: str, comment: str, date_: date | None = None, weight: float = 1.0) -> Skill:
        """Add an endorsement. Returns *self* for chaining."""
        self.endorsements.append(Endorsement(endorser, comment, date_ or date.today(), weight))
        return self

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dict."""
        return {
            "name": self.name,
            "category": self.category,
            "proficiency": self.proficiency.value,
            "evidence": list(self.evidence),
            "endorsements": [
                {"endorser": e.endorser, "comment": e.comment, "date": e.date.isoformat(), "weight": e.weight}
                for e in self.endorsements
            ],
            "acquired_date": self.acquired_date.isoformat() if self.acquired_date else None,
            "tags": list(self.tags),
            "endorsement_score": self.endorsement_score,
            "combined_score": self.combined_score,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Skill:
        """Deserialize from a dict produced by ``to_dict``."""
        endorsements = [
            Endorsement(
                endorser=e["endorser"],
                comment=e["comment"],
                date=date.fromisoformat(e["date"]),
                weight=e.get("weight", 1.0),
            )
            for e in data.get("endorsements", [])
        ]
        return cls(
            name=data["name"],
            category=data.get("category", ""),
            proficiency=ProficiencyLevel(data.get("proficiency", "intermediate")),
            evidence=list(data.get("evidence", [])),
            endorsements=endorsements,
            acquired_date=date.fromisoformat(d) if (d := data.get("acquired_date")) else None,
            tags=list(data.get("tags", [])),
        )
