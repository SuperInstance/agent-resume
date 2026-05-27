# agent-resume

Agent resume/CV generation — document AI agent capabilities, experience, and performance history.

Part of the [Cocapn fleet](https://github.com/Lucineer/the-fleet).

## Install

```bash
pip install agent-resume
```

For development:

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from agent_resume import AgentResume, Skill, Experience, ResumeMatcher, ResumeFormatter
from agent_resume.resume import Certification, Badge, PerformanceMetrics, PortfolioItem
from agent_resume.skill import ProficiencyLevel
from datetime import date

# Build a resume
resume = AgentResume(
    id="alpha",
    name="Alpha Agent",
    summary="High-performance automation and data processing agent.",
    skills=[
        Skill(name="Python", category="Language", proficiency=ProficiencyLevel.EXPERT),
        Skill(name="API Design", category="Architecture", proficiency=ProficiencyLevel.ADVANCED),
        Skill(name="Docker", category="DevOps", proficiency=ProficiencyLevel.INTERMEDIATE, tags=["containers"]),
    ],
    experience=[
        Experience(
            title="Customer Support Automation",
            role="Primary Handler",
            description="Reduced response time by 78% and handled 15k+ tickets",
            outcome="98% customer satisfaction",
            start_date=date(2023, 1, 1),
        ),
    ],
    metrics=PerformanceMetrics(uptime_pct=99.8, tasks_completed=1247, accuracy_pct=96.5, avg_response_time_ms=145),
    certifications=[Certification(name="Cloud Certified", issuer="ACME Corp")],
    badges=[Badge(id="speed", name="Speed Demon", earned=date(2024, 5, 1))],
)
```

### Skill Endorsements

```python
skill = Skill(name="Data Analysis", proficiency=ProficiencyLevel.ADVANCED)
skill.add_evidence("Processed 2.4TB of unstructured data")
skill.endorse("Agent-Beta", "Excellent statistical analysis", weight=0.9)
print(skill.combined_score)  # Blends proficiency + endorsements
```

### Matching Resumes to Requirements

```python
matcher = ResumeMatcher()
matcher.add_requirement("Python", ProficiencyLevel.ADVANCED)
matcher.add_requirement("API Design", ProficiencyLevel.INTERMEDIATE)
matcher.add_requirement("Kubernetes", ProficiencyLevel.INTERMEDIATE)

result = matcher.match(resume)
print(f"Score: {result.overall_score:.2f}")
print(f"Qualified: {result.is_qualified}")
print(f"Matched: {result.matched}")
print(f"Missing: {result.missing}")

# Rank multiple candidates
ranked = matcher.rank([resume_a, resume_b, resume_c])
for r, score in ranked:
    print(f"{r.name}: {score.overall_score:.2f}")
```

### Formatting Output

```python
fmt = ResumeFormatter()

# Plain text
print(fmt.to_text(resume))

# Markdown
print(fmt.to_markdown(resume))

# JSON
print(fmt.to_json(resume, indent=2))
```

### Serialization

```python
# To dict / JSON
data = resume.to_dict()
json_str = ResumeFormatter().to_json(resume)

# From dict (roundtrip)
restored = AgentResume.from_dict(data)
```

## API Reference

### `AgentResume`
Central data model: id, name, summary, skills, experience, metrics, certifications, portfolio, badges.

### `Skill`
Name, category, proficiency level, evidence list, endorsements, tags. Computes `endorsement_score` and `combined_score`.

### `Experience`
Title, role, description, outcome, project, dates. Computes `duration`, `duration_days`, `is_ongoing`.

### `ResumeMatcher`
Add requirements with minimum proficiency, then `match()` or `rank()` resumes. Supports exact, tag, and fuzzy matching.

### `ResumeFormatter`
Output resumes as plain text, Markdown, or JSON.

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
