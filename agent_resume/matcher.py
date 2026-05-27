"""ResumeMatcher — score a resume against job/task requirements."""

from __future__ import annotations

from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import Any

from agent_resume.resume import AgentResume
from agent_resume.skill import ProficiencyLevel


@dataclass
class Requirement:
    """A single requirement for a job or task.

    Attributes:
        name: Skill or capability name.
        min_proficiency: Minimum acceptable proficiency level.
        weight: Importance weight (default 1.0).
        category: Optional category for grouping.
    """

    name: str
    min_proficiency: ProficiencyLevel = ProficiencyLevel.INTERMEDIATE
    weight: float = 1.0
    category: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "min_proficiency": self.min_proficiency.value,
            "weight": self.weight,
            "category": self.category,
        }


@dataclass
class MatchResult:
    """Result of matching a resume against requirements.

    Attributes:
        overall_score: 0.0–1.0 overall fitness score.
        matched: Requirements that were met.
        missing: Requirements that were not met.
        partial: Requirements partially met (skill found but below proficiency).
        details: Per-requirement breakdown.
    """

    overall_score: float
    matched: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    partial: list[str] = field(default_factory=list)
    details: list[dict[str, Any]] = field(default_factory=list)

    @property
    def is_qualified(self) -> bool:
        return len(self.missing) == 0 and self.overall_score >= 0.6

    def to_dict(self) -> dict[str, Any]:
        return {
            "overall_score": round(self.overall_score, 4),
            "is_qualified": self.is_qualified,
            "matched": self.matched,
            "missing": self.missing,
            "partial": self.partial,
            "details": self.details,
        }


def _fuzzy_match(a: str, b: str) -> float:
    """Return similarity ratio between two strings (0.0–1.0)."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


class ResumeMatcher:
    """Score agent resumes against a set of requirements.

    Example::

        matcher = ResumeMatcher()
        matcher.add_requirement("Python", ProficiencyLevel.ADVANCED)
        matcher.add_requirement("API Design", ProficiencyLevel.INTERMEDIATE)
        result = matcher.match(resume)
        print(result.overall_score, result.is_qualified)
    """

    def __init__(self, fuzzy_threshold: float = 0.6) -> None:
        self.requirements: list[Requirement] = []
        self.fuzzy_threshold = fuzzy_threshold

    def add_requirement(
        self,
        name: str,
        min_proficiency: ProficiencyLevel = ProficiencyLevel.INTERMEDIATE,
        weight: float = 1.0,
        category: str = "",
    ) -> ResumeMatcher:
        self.requirements.append(Requirement(name, min_proficiency, weight, category))
        return self

    def clear(self) -> ResumeMatcher:
        self.requirements.clear()
        return self

    def _find_skill_match(self, req_name: str, resume: AgentResume) -> tuple[float, Any | None]:
        """Find the best matching skill for a requirement. Returns (score, skill)."""
        best_score = 0.0
        best_skill = None
        for skill in resume.skills:
            # Exact match
            if skill.name.lower() == req_name.lower():
                return (1.0, skill)
            # Tag match
            for tag in skill.tags:
                if tag.lower() == req_name.lower():
                    return (0.95, skill)
            # Fuzzy match on name
            ratio = _fuzzy_match(skill.name, req_name)
            if ratio > best_score:
                best_score = ratio
                best_skill = skill
        if best_score >= self.fuzzy_threshold:
            return (best_score, best_skill)
        return (0.0, None)

    def match(self, resume: AgentResume) -> MatchResult:
        """Match a resume against all requirements."""
        if not self.requirements:
            return MatchResult(overall_score=1.0)

        total_weight = sum(r.weight for r in self.requirements)
        if total_weight == 0:
            return MatchResult(overall_score=0.0)

        weighted_score = 0.0
        matched: list[str] = []
        missing: list[str] = []
        partial: list[str] = []
        details: list[dict[str, Any]] = []

        for req in self.requirements:
            name_score, skill = self._find_skill_match(req.name, resume)

            if skill is None:
                missing.append(req.name)
                details.append({
                    "requirement": req.name,
                    "status": "missing",
                    "name_match_score": name_score,
                    "proficiency_score": 0.0,
                    "contribution": 0.0,
                })
                continue

            prof_score = min(skill.proficiency.numeric / req.min_proficiency.numeric, 1.0)
            contribution = name_score * prof_score * req.weight

            if prof_score >= 1.0:
                matched.append(req.name)
                status = "matched"
            else:
                partial.append(req.name)
                status = "partial"

            weighted_score += contribution
            details.append({
                "requirement": req.name,
                "status": status,
                "matched_skill": skill.name,
                "name_match_score": round(name_score, 3),
                "proficiency_score": round(prof_score, 3),
                "contribution": round(contribution, 4),
            })

        overall = weighted_score / total_weight if total_weight else 0.0
        return MatchResult(
            overall_score=overall,
            matched=matched,
            missing=missing,
            partial=partial,
            details=details,
        )

    def rank(self, resumes: list[AgentResume]) -> list[tuple[AgentResume, MatchResult]]:
        """Rank multiple resumes by match score. Best first."""
        results = [(r, self.match(r)) for r in resumes]
        results.sort(key=lambda x: x[1].overall_score, reverse=True)
        return results
