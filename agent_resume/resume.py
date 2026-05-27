"""AgentResume — the central data model for an agent's resume."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any

from agent_resume.experience import Experience
from agent_resume.skill import Skill


@dataclass
class PerformanceMetrics:
    """Quantitative performance snapshot."""

    uptime_pct: float = 0.0
    tasks_completed: int = 0
    accuracy_pct: float = 0.0
    avg_response_time_ms: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "uptime_pct": self.uptime_pct,
            "tasks_completed": self.tasks_completed,
            "accuracy_pct": self.accuracy_pct,
            "avg_response_time_ms": self.avg_response_time_ms,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PerformanceMetrics:
        return cls(
            uptime_pct=data.get("uptime_pct", 0.0),
            tasks_completed=data.get("tasks_completed", 0),
            accuracy_pct=data.get("accuracy_pct", 0.0),
            avg_response_time_ms=data.get("avg_response_time_ms", 0.0),
        )


@dataclass
class Certification:
    """A certification or qualification."""

    name: str
    issuer: str = ""
    date_earned: date | None = None
    expires: date | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "issuer": self.issuer,
            "date_earned": self.date_earned.isoformat() if self.date_earned else None,
            "expires": self.expires.isoformat() if self.expires else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Certification:
        return cls(
            name=data["name"],
            issuer=data.get("issuer", ""),
            date_earned=date.fromisoformat(d) if (d := data.get("date_earned")) else None,
            expires=date.fromisoformat(d) if (d := data.get("expires")) else None,
        )


@dataclass
class Badge:
    """An achievement badge."""

    id: str
    name: str
    earned: date | None = None

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name, "earned": self.earned.isoformat() if self.earned else None}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Badge:
        return cls(
            id=data["id"],
            name=data["name"],
            earned=date.fromisoformat(d) if (d := data.get("earned")) else None,
        )


@dataclass
class PortfolioItem:
    """A portfolio entry showcasing work."""

    title: str
    description: str = ""
    outcome: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"title": self.title, "description": self.description, "outcome": self.outcome}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PortfolioItem:
        return cls(title=data["title"], description=data.get("description", ""), outcome=data.get("outcome", ""))


@dataclass
class AgentResume:
    """Complete resume for an AI agent.

    Attributes:
        id: Unique agent identifier.
        name: Human-readable name.
        summary: Short bio / executive summary.
        skills: List of skills with proficiency.
        experience: List of experience entries.
        metrics: Performance metrics snapshot.
        certifications: Qualifications held.
        portfolio: Notable work items.
        badges: Achievement badges.
        tags: Free-form tags for search.
        created_date: When the resume was first created.
        updated_date: When the resume was last updated.
    """

    id: str
    name: str
    summary: str = ""
    skills: list[Skill] = field(default_factory=list)
    experience: list[Experience] = field(default_factory=list)
    metrics: PerformanceMetrics = field(default_factory=PerformanceMetrics)
    certifications: list[Certification] = field(default_factory=list)
    portfolio: list[PortfolioItem] = field(default_factory=list)
    badges: list[Badge] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    created_date: date | None = None
    updated_date: date | None = None

    # -- helpers -----------------------------------------------------------

    def skill_names(self) -> list[str]:
        return [s.name for s in self.skills]

    def add_skill(self, skill: Skill) -> AgentResume:
        self.skills.append(skill)
        return self

    def add_experience(self, exp: Experience) -> AgentResume:
        self.experience.append(exp)
        return self

    def add_certification(self, cert: Certification) -> AgentResume:
        self.certifications.append(cert)
        return self

    def add_portfolio_item(self, item: PortfolioItem) -> AgentResume:
        self.portfolio.append(item)
        return self

    def add_badge(self, badge: Badge) -> AgentResume:
        self.badges.append(badge)
        return self

    def touch(self) -> None:
        """Update the ``updated_date`` to today."""
        self.updated_date = date.today()

    # -- serialization -----------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "summary": self.summary,
            "skills": [s.to_dict() for s in self.skills],
            "experience": [e.to_dict() for e in self.experience],
            "metrics": self.metrics.to_dict(),
            "certifications": [c.to_dict() for c in self.certifications],
            "portfolio": [p.to_dict() for p in self.portfolio],
            "badges": [b.to_dict() for b in self.badges],
            "tags": list(self.tags),
            "created_date": self.created_date.isoformat() if self.created_date else None,
            "updated_date": self.updated_date.isoformat() if self.updated_date else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AgentResume:
        return cls(
            id=data["id"],
            name=data["name"],
            summary=data.get("summary", ""),
            skills=[Skill.from_dict(s) for s in data.get("skills", [])],
            experience=[Experience.from_dict(e) for e in data.get("experience", [])],
            metrics=PerformanceMetrics.from_dict(data["metrics"]) if "metrics" in data else PerformanceMetrics(),
            certifications=[Certification.from_dict(c) for c in data.get("certifications", [])],
            portfolio=[PortfolioItem.from_dict(p) for p in data.get("portfolio", [])],
            badges=[Badge.from_dict(b) for b in data.get("badges", [])],
            tags=list(data.get("tags", [])),
            created_date=date.fromisoformat(d) if (d := data.get("created_date")) else None,
            updated_date=date.fromisoformat(d) if (d := data.get("updated_date")) else None,
        )
