# agent-resume — Agent Capability Documentation

**Generate resumes/CVs for AI agents — document capabilities, experience, performance history, and proficiency levels.**

## What This Gives You

- **Structured resumes** — document agent skills, experience, and performance in a standard format
- **Proficiency levels** — rate skills as BEGINNER, INTERMEDIATE, ADVANCED, EXPERT, MASTER
- **Experience tracking** — record projects, tasks completed, success rates, and durations
- **Resume matching** — find the best agent for a task by matching requirements to resume capabilities
- **Multi-format output** — generate resumes as markdown, JSON, or structured text

## Quick Start

```bash
pip install agent-resume
```

```python
from agent_resume import AgentResume, Skill, ProficiencyLevel, Experience, ResumeMatcher

# Build a resume
resume = AgentResume(agent_id="agent-3", name="Fleet Builder")
resume.add_skill(Skill(name="Rust", level=ProficiencyLevel.ADVANCED, years=2))
resume.add_skill(Skill(name="Python", level=ProficiencyLevel.EXPERT, years=4))
resume.add_experience(Experience(
    project="cocapn-health-rs",
    role="Lead Developer",
    tasks_completed=47,
    success_rate=0.94,
))

# Find the best agent for a task
matcher = ResumeMatcher()
matcher.add_resume(resume)
best = matcher.match(requirements=["Rust", "benchmarking"])
print(f"Best fit: {best.agent_id} (score: {best.score:.2f})")

# Format output
from agent_resume import ResumeFormatter
formatter = ResumeFormatter()
print(formatter.to_markdown(resume))
```

## API Reference

### `AgentResume(agent_id, name)` — `add_skill()`, `add_experience()`, `summary()`
### `Skill(name, level, years, evidence)` · `ProficiencyLevel` — BEGINNER → MASTER
### `Experience(project, role, tasks_completed, success_rate, duration)`
### `ResumeMatcher` — `add_resume()`, `match(requirements) → MatchResult`
### `ResumeFormatter` — `to_markdown()`, `to_json()`, `to_text()`

## How It Fits

The credentialing layer for the [SuperInstance fleet](https://github.com/SuperInstance). Works with [agent-tattoo](https://github.com/SuperInstance/agent-tattoo) — tattoos are the raw experience, resumes are the polished document.

- **[agent-tattoo](https://github.com/SuperInstance/agent-tattoo)** — Behavioral markers (feed into resumes)
- **[agent-generations](https://github.com/SuperInstance/agent-generations)** — Version tracking
- **[captain](https://github.com/SuperInstance/captain)** — Uses matcher for task assignment

## Testing

```bash
pytest tests/
```

## Installation

```bash
pip install agent-resume
```

Python 3.10+. MIT license.
