"""Experience entries — tasks, outcomes, and duration."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any


@dataclass
class Experience:
    """A single experience entry on an agent's resume.

    Attributes:
        title: Short title (e.g. "Customer Support Automation").
        role: Role the agent played (e.g. "Primary Handler").
        description: What was done.
        outcome: Measurable result or impact.
        project: Project or system name.
        start_date: When the experience began.
        end_date: When it ended (None = ongoing).
        tags: Free-form tags.
    """

    title: str
    role: str = ""
    description: str = ""
    outcome: str = ""
    project: str = ""
    start_date: date | None = None
    end_date: date | None = None
    tags: list[str] = field(default_factory=list)

    @property
    def duration(self) -> timedelta | None:
        """Elapsed time, or None if dates are missing."""
        if self.start_date is None:
            return None
        end = self.end_date or date.today()
        return end - self.start_date

    @property
    def duration_days(self) -> int | None:
        d = self.duration
        return d.days if d is not None else None

    @property
    def is_ongoing(self) -> bool:
        return self.end_date is None and self.start_date is not None

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "role": self.role,
            "description": self.description,
            "outcome": self.outcome,
            "project": self.project,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "duration_days": self.duration_days,
            "is_ongoing": self.is_ongoing,
            "tags": list(self.tags),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Experience:
        return cls(
            title=data["title"],
            role=data.get("role", ""),
            description=data.get("description", ""),
            outcome=data.get("outcome", ""),
            project=data.get("project", ""),
            start_date=date.fromisoformat(d) if (d := data.get("start_date")) else None,
            end_date=date.fromisoformat(d) if (d := data.get("end_date")) else None,
            tags=list(data.get("tags", [])),
        )
