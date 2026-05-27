"""Tests for agent_resume package."""

from datetime import date, timedelta

import pytest

from agent_resume import (
    AgentResume,
    Experience,
    ProficiencyLevel,
    ResumeFormatter,
    ResumeMatcher,
    Skill,
)
from agent_resume.resume import Badge, Certification, PerformanceMetrics, PortfolioItem
from agent_resume.skill import Endorsement


# -- Helpers ------------------------------------------------------------------

def _sample_skill(name: str = "Python", prof: ProficiencyLevel = ProficiencyLevel.EXPERT) -> Skill:
    return Skill(name=name, category="Language", proficiency=prof)


def _sample_experience(title: str = "Data Pipeline") -> Experience:
    return Experience(
        title=title,
        role="Lead Engineer",
        description="Built a real-time data pipeline",
        outcome="Processed 2TB/day with 99.9% uptime",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 6, 30),
    )


def _sample_resume() -> AgentResume:
    return AgentResume(
        id="test-agent",
        name="Test Agent",
        summary="A test agent for unit testing.",
        skills=[
            _sample_skill("Python", ProficiencyLevel.EXPERT),
            _sample_skill("API Design", ProficiencyLevel.ADVANCED),
            Skill(name="Docker", category="DevOps", proficiency=ProficiencyLevel.INTERMEDIATE, tags=["containers"]),
        ],
        experience=[_sample_experience()],
        metrics=PerformanceMetrics(uptime_pct=99.8, tasks_completed=1247, accuracy_pct=96.5, avg_response_time_ms=145),
        certifications=[Certification(name="Cloud Certified", issuer="ACME Corp", date_earned=date(2024, 3, 15))],
        portfolio=[PortfolioItem(title="Cool Project", description="Did something cool", outcome="It worked")],
        badges=[Badge(id="speed", name="Speed Demon", earned=date(2024, 5, 1))],
        tags=["backend", "data"],
        created_date=date(2024, 1, 1),
    )


# -- Skill tests --------------------------------------------------------------

class TestSkill:
    def test_creation_defaults(self):
        s = Skill(name="Testing")
        assert s.name == "Testing"
        assert s.proficiency == ProficiencyLevel.INTERMEDIATE
        assert s.evidence == []
        assert s.endorsements == []

    def test_proficiency_numeric(self):
        assert ProficiencyLevel.NOVICE.numeric == 1
        assert ProficiencyLevel.MASTER.numeric == 6

    def test_combined_score_no_endorsements(self):
        s = _sample_skill()
        # Expert (5) → (5-1)/5 = 0.8
        assert s.combined_score == pytest.approx(0.8)

    def test_endorse_score(self):
        s = _sample_skill()
        s.endorse("Agent-B", "Great work", weight=0.9)
        s.endorse("Agent-C", "Solid", weight=0.7)
        assert 0.0 < s.endorsement_score <= 1.0

    def test_endorsement_weight_validation(self):
        with pytest.raises(ValueError):
            Endorsement(endorser="X", comment="y", date=date.today(), weight=2.0)

    def test_chaining(self):
        s = Skill(name="X").add_evidence("did thing").endorse("A", "nice")
        assert len(s.evidence) == 1
        assert len(s.endorsements) == 1

    def test_serialization_roundtrip(self):
        s = _sample_skill()
        s.add_evidence("Built 3 microservices")
        s.endorse("Reviewer", "Excellent", date_=date(2024, 1, 1))
        s.tags = ["backend"]
        s.acquired_date = date(2023, 6, 1)
        d = s.to_dict()
        s2 = Skill.from_dict(d)
        assert s2.name == s.name
        assert s2.proficiency == s.proficiency
        assert s2.evidence == s.evidence
        assert len(s2.endorsements) == 1
        assert s2.tags == ["backend"]
        assert s2.acquired_date == date(2023, 6, 1)


# -- Experience tests ---------------------------------------------------------

class TestExperience:
    def test_duration(self):
        e = _sample_experience()
        assert e.duration_days == 181  # Jan 1 to Jun 30 in 2024

    def test_ongoing(self):
        e = Experience(title="Current", start_date=date(2024, 1, 1))
        assert e.is_ongoing
        assert e.duration_days is not None

    def test_no_dates(self):
        e = Experience(title="Something")
        assert e.duration is None
        assert e.duration_days is None
        assert not e.is_ongoing

    def test_serialization_roundtrip(self):
        e = _sample_experience()
        e2 = Experience.from_dict(e.to_dict())
        assert e2.title == e.title
        assert e2.role == e.role
        assert e2.start_date == e.start_date
        assert e2.end_date == e.end_date


# -- Resume tests -------------------------------------------------------------

class TestAgentResume:
    def test_creation(self):
        r = _sample_resume()
        assert r.id == "test-agent"
        assert len(r.skills) == 3

    def test_skill_names(self):
        r = _sample_resume()
        assert "Python" in r.skill_names()

    def test_add_methods_chain(self):
        r = AgentResume(id="x", name="X")
        r.add_skill(Skill(name="A")).add_experience(Experience(title="B")).add_badge(Badge(id="c", name="C"))
        assert len(r.skills) == 1
        assert len(r.experience) == 1
        assert len(r.badges) == 1

    def test_touch(self):
        r = _sample_resume()
        r.touch()
        assert r.updated_date == date.today()

    def test_serialization_roundtrip(self):
        r = _sample_resume()
        d = r.to_dict()
        r2 = AgentResume.from_dict(d)
        assert r2.id == r.id
        assert r2.name == r.name
        assert len(r2.skills) == len(r.skills)
        assert len(r2.experience) == len(r.experience)
        assert r2.metrics.uptime_pct == r.metrics.uptime_pct
        assert len(r2.certifications) == len(r.certifications)
        assert len(r2.portfolio) == len(r.portfolio)
        assert len(r2.badges) == len(r.badges)

    def test_from_dict_missing_optional_fields(self):
        r = AgentResume.from_dict({"id": "a", "name": "B"})
        assert r.id == "a"
        assert r.skills == []
        assert r.metrics.uptime_pct == 0.0


# -- Matcher tests ------------------------------------------------------------

class TestResumeMatcher:
    def test_exact_match(self):
        m = ResumeMatcher()
        m.add_requirement("Python", ProficiencyLevel.ADVANCED)
        r = _sample_resume()
        result = m.match(r)
        assert "Python" in result.matched
        assert result.overall_score > 0.5

    def test_missing_skill(self):
        m = ResumeMatcher()
        m.add_requirement("Rust", ProficiencyLevel.EXPERT)
        result = m.match(_sample_resume())
        assert "Rust" in result.missing
        assert result.overall_score < 0.5

    def test_partial_proficiency(self):
        m = ResumeMatcher()
        m.add_requirement("Docker", ProficiencyLevel.EXPERT)
        r = _sample_resume()  # Docker is INTERMEDIATE
        result = m.match(r)
        assert "Docker" in result.partial
        assert result.overall_score > 0

    def test_tag_match(self):
        m = ResumeMatcher()
        m.add_requirement("containers", ProficiencyLevel.INTERMEDIATE)
        r = _sample_resume()  # Docker has tag "containers"
        result = m.match(r)
        assert "containers" in result.matched

    def test_fuzzy_match(self):
        m = ResumeMatcher(fuzzy_threshold=0.5)
        m.add_requirement("api designing", ProficiencyLevel.INTERMEDIATE)
        r = _sample_resume()  # Has "API Design"
        result = m.match(r)
        assert "api designing" in result.matched or "api designing" in result.partial

    def test_no_requirements(self):
        m = ResumeMatcher()
        result = m.match(_sample_resume())
        assert result.overall_score == 1.0

    def test_is_qualified(self):
        m = ResumeMatcher()
        m.add_requirement("Python", ProficiencyLevel.INTERMEDIATE)
        result = m.match(_sample_resume())
        assert result.is_qualified

    def test_not_qualified(self):
        m = ResumeMatcher()
        m.add_requirement("Rust", ProficiencyLevel.EXPERT)
        result = m.match(_sample_resume())
        assert not result.is_qualified

    def test_rank(self):
        r1 = AgentResume(id="a", name="A", skills=[Skill(name="Python", proficiency=ProficiencyLevel.EXPERT)])
        r2 = AgentResume(id="b", name="B", skills=[Skill(name="Python", proficiency=ProficiencyLevel.NOVICE)])
        m = ResumeMatcher()
        m.add_requirement("Python", ProficiencyLevel.INTERMEDIATE)
        ranked = m.rank([r2, r1])
        assert ranked[0][0].id == "a"

    def test_match_result_serialization(self):
        m = ResumeMatcher()
        m.add_requirement("Python", ProficiencyLevel.ADVANCED)
        result = m.match(_sample_resume())
        d = result.to_dict()
        assert "overall_score" in d
        assert isinstance(d["matched"], list)


# -- Formatter tests ----------------------------------------------------------

class TestResumeFormatter:
    def test_to_json(self):
        fmt = ResumeFormatter()
        r = _sample_resume()
        j = fmt.to_json(r)
        assert '"test-agent"' in j
        assert '"Python"' in j

    def test_to_text(self):
        fmt = ResumeFormatter()
        text = fmt.to_text(_sample_resume())
        assert "Test Agent" in text
        assert "Python" in text
        assert "expert" in text.lower()
        assert "EXPERIENCE" in text

    def test_to_markdown(self):
        fmt = ResumeFormatter()
        md = fmt.to_markdown(_sample_resume())
        assert "# Test Agent" in md
        assert "## Skills" in md
        assert "| Python" in md
        assert "## Experience" in md

    def test_to_dict(self):
        fmt = ResumeFormatter()
        d = fmt.to_dict(_sample_resume())
        assert isinstance(d, dict)
        assert d["id"] == "test-agent"

    def test_empty_resume_text(self):
        fmt = ResumeFormatter()
        r = AgentResume(id="empty", name="Empty")
        text = fmt.to_text(r)
        assert "Empty" in text

    def test_empty_resume_markdown(self):
        fmt = ResumeFormatter()
        r = AgentResume(id="empty", name="Empty")
        md = fmt.to_markdown(r)
        assert "# Empty" in md

    def test_json_roundtrip(self):
        import json
        fmt = ResumeFormatter()
        r = _sample_resume()
        j = fmt.to_json(r)
        d = json.loads(j)
        r2 = AgentResume.from_dict(d)
        assert r2.id == r.id
        assert len(r2.skills) == len(r.skills)
