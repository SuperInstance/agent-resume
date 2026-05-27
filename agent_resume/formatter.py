"""ResumeFormatter — render resumes in plain text, markdown, or JSON."""

from __future__ import annotations

import json
from typing import Any

from agent_resume.resume import AgentResume


class ResumeFormatter:
    """Format an AgentResume into various output formats.

    Example::

        fmt = ResumeFormatter()
        print(fmt.to_markdown(resume))
        print(fmt.to_json(resume, indent=2))
    """

    # -- JSON --------------------------------------------------------------

    def to_json(self, resume: AgentResume, indent: int = 2) -> str:
        """Serialize resume to a JSON string."""
        return json.dumps(resume.to_dict(), indent=indent, ensure_ascii=False)

    def to_dict(self, resume: AgentResume) -> dict[str, Any]:
        """Return the raw dict (useful for further processing)."""
        return resume.to_dict()

    # -- Plain text --------------------------------------------------------

    def to_text(self, resume: AgentResume) -> str:
        """Render resume as a clean plain-text document."""
        lines: list[str] = []
        lines.append(f"{'=' * 60}")
        lines.append(f"  AGENT RESUME: {resume.name}")
        lines.append(f"  ID: {resume.id}")
        lines.append(f"{'=' * 60}")
        lines.append("")

        if resume.summary:
            lines.append("SUMMARY")
            lines.append("-" * 40)
            lines.append(resume.summary)
            lines.append("")

        # Skills
        if resume.skills:
            lines.append("SKILLS")
            lines.append("-" * 40)
            for s in resume.skills:
                cat = f" [{s.category}]" if s.category else ""
                lines.append(f"  • {s.name}{cat} — {s.proficiency.value}")
                for ev in s.evidence[:3]:
                    lines.append(f"      - {ev}")
            lines.append("")

        # Experience
        if resume.experience:
            lines.append("EXPERIENCE")
            lines.append("-" * 40)
            for exp in resume.experience:
                dur = f" ({exp.duration_days}d)" if exp.duration_days is not None else ""
                lines.append(f"  {exp.title}{dur}")
                if exp.role:
                    lines.append(f"    Role: {exp.role}")
                if exp.description:
                    lines.append(f"    {exp.description}")
                if exp.outcome:
                    lines.append(f"    Outcome: {exp.outcome}")
            lines.append("")

        # Metrics
        m = resume.metrics
        if m.tasks_completed > 0:
            lines.append("PERFORMANCE METRICS")
            lines.append("-" * 40)
            lines.append(f"  Uptime:          {m.uptime_pct}%")
            lines.append(f"  Tasks completed: {m.tasks_completed}")
            lines.append(f"  Accuracy:        {m.accuracy_pct}%")
            lines.append(f"  Avg response:    {m.avg_response_time_ms}ms")
            lines.append("")

        # Certifications
        if resume.certifications:
            lines.append("CERTIFICATIONS")
            lines.append("-" * 40)
            for c in resume.certifications:
                lines.append(f"  • {c.name}" + (f" ({c.issuer})" if c.issuer else ""))
            lines.append("")

        # Portfolio
        if resume.portfolio:
            lines.append("PORTFOLIO")
            lines.append("-" * 40)
            for p in resume.portfolio:
                lines.append(f"  {p.title}")
                if p.description:
                    lines.append(f"    {p.description}")
                if p.outcome:
                    lines.append(f"    Outcome: {p.outcome}")
            lines.append("")

        # Badges
        if resume.badges:
            lines.append("BADGES")
            lines.append("-" * 40)
            for b in resume.badges:
                lines.append(f"  🏅 {b.name}")
            lines.append("")

        return "\n".join(lines)

    # -- Markdown ----------------------------------------------------------

    def to_markdown(self, resume: AgentResume) -> str:
        """Render resume as a Markdown document."""
        lines: list[str] = []
        lines.append(f"# {resume.name}")
        lines.append(f"> Agent ID: `{resume.id}`")
        lines.append("")

        if resume.summary:
            lines.append(resume.summary)
            lines.append("")

        # Skills
        if resume.skills:
            lines.append("## Skills")
            lines.append("")
            lines.append("| Skill | Category | Proficiency | Endorsements |")
            lines.append("|-------|----------|-------------|--------------|")
            for s in resume.skills:
                cat = s.category or "—"
                endorse_count = len(s.endorsements)
                lines.append(f"| {s.name} | {cat} | {s.proficiency.value} | {endorse_count} |")
            lines.append("")

        # Experience
        if resume.experience:
            lines.append("## Experience")
            lines.append("")
            for exp in resume.experience:
                lines.append(f"### {exp.title}")
                if exp.role:
                    lines.append(f"**Role:** {exp.role}  ")
                dur = f"{exp.duration_days} days" if exp.duration_days is not None else "ongoing"
                lines.append(f"**Duration:** {dur}  ")
                lines.append("")
                if exp.description:
                    lines.append(exp.description)
                    lines.append("")
                if exp.outcome:
                    lines.append(f"*Outcome:* {exp.outcome}")
                    lines.append("")

        # Metrics
        m = resume.metrics
        if m.tasks_completed > 0:
            lines.append("## Performance Metrics")
            lines.append("")
            lines.append(f"| Metric | Value |")
            lines.append(f"|--------|-------|")
            lines.append(f"| Uptime | {m.uptime_pct}% |")
            lines.append(f"| Tasks completed | {m.tasks_completed:,} |")
            lines.append(f"| Accuracy | {m.accuracy_pct}% |")
            lines.append(f"| Avg response time | {m.avg_response_time_ms}ms |")
            lines.append("")

        # Certifications
        if resume.certifications:
            lines.append("## Certifications")
            lines.append("")
            for c in resume.certifications:
                lines.append(f"- **{c.name}**" + (f" — {c.issuer}" if c.issuer else ""))
            lines.append("")

        # Portfolio
        if resume.portfolio:
            lines.append("## Portfolio")
            lines.append("")
            for p in resume.portfolio:
                lines.append(f"### {p.title}")
                if p.description:
                    lines.append(p.description)
                if p.outcome:
                    lines.append(f"\n**Outcome:** {p.outcome}")
                lines.append("")

        # Badges
        if resume.badges:
            lines.append("## Badges")
            lines.append("")
            for b in resume.badges:
                lines.append(f"- 🏅 **{b.name}** (`{b.id}`)")
            lines.append("")

        return "\n".join(lines)
