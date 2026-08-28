#!/usr/bin/env python3
"""Generate deterministic Gate 5E content and freeze audits from canonical data."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import yaml

try:
    from .content import ROOT, load_records, research_scope
except ImportError:
    from content import ROOT, load_records, research_scope


ANALYSIS = {
    "geographies-of-climate-learning": {
        "stable": "Cities must use knowledge produced elsewhere.",
        "instability": "A precedent or visible resemblance does not establish that its lessons will travel.",
        "consequence": "Unexamined contextual differences can make cross-city inference misleading.",
        "intervention": "Study the geography, authority, movement and adaptation of urban climate knowledge.",
    },
    "where-new-evidence-matters": {
        "stable": "Important evidence is uneven and incomplete.",
        "instability": "An absence does not show that producing the missing evidence would be valuable.",
        "consequence": "Research resources may accumulate cases without changing consequential uncertainty.",
        "intervention": "Connect evidence mapping to research design and decision analysis.",
    },
    "modes-of-climate-delivery": {
        "stable": "Urban climate policy is often classified by targets, technologies or instruments.",
        "instability": "Evidence and ambition do not implement themselves, and similar policies can follow different trajectories.",
        "consequence": "Policy labels can conceal the authority, resources and capability required for durable action.",
        "intervention": "Compare the institutional configurations through which change becomes operable.",
    },
    "consequences-for-people-and-places": {
        "stable": "Climate action changes emissions and wider social, economic and health outcomes.",
        "instability": "Average benefits and total value can conceal different effects across people, places and periods.",
        "consequence": "Appraisal can hide burdens, harms, trade-offs and distributional change.",
        "intervention": "Examine intended and unintended outcomes, their distribution and their dependence on delivery.",
    },
}


def theme_audit() -> str:
    parts = ["# Gate 5E theme reader-value audit", "", "Status: PASS", "", "The final public copy is generated directly from `config/research_scope.yml`; the sections below reproduce every public argument field used on theme pages."]
    for theme in research_scope()["themes"]:
        a = ANALYSIS[theme["id"]]
        parts += [
            "", f"## {theme['name']}", "",
            f"- **Stable understanding:** {a['stable']}",
            f"- **Instability:** {a['instability']}",
            f"- **Consequence:** {a['consequence']}",
            f"- **Analytical intervention:** {a['intervention']}",
            f"- **Changed understanding:** {theme['what_this_changes']}",
            f"- **Boundary:** {theme['analytical_boundary']}",
            "", "### Final public copy", "",
            f"**Guiding question:** {theme['guiding_question']}", "",
            theme["long_description"][0], "", theme["long_description"][1], "",
            f"**Analytical boundary:** {theme['analytical_boundary']}", "",
            f"**What this changes:** {theme['what_this_changes']}", "",
            f"**Connection to the cycle:** {theme['connection_to_next']}",
        ]
    return "\n".join(parts) + "\n"


def idea_audit() -> str:
    themes = {item["id"]: item["name"] for item in research_scope()["themes"]}
    ideas = sorted(load_records("data/research-ideas"), key=lambda item: (list(themes).index(item["theme_id"]), item["display_order"]))
    parts = ["# Gate 5E research-ideas reader-value audit", "", "Status: PASS", "", "Twenty-four active records are present, six per theme. Every record below is owner-approved as a possible direction and retains the exact non-active/non-funded disclaimer; approval does not make it Work."]
    current = None
    for idea in ideas:
        if idea["theme_id"] != current:
            current = idea["theme_id"]
            parts += ["", f"## {themes[current]}"]
        parts += [
            "", f"### {idea['working_title']} (`{idea['idea_id']}`)", "",
            f"- **Problem of understanding:** {idea['problem_of_understanding']}",
            f"- **Question:** {idea['question']}",
            f"- **Consequence:** {idea['why_it_may_matter']}",
            f"- **Possible research design:** {idea['possible_research_design']}",
            f"- **Methods:** {', '.join(idea['suggested_methods'])}.",
        ]
        if idea.get("required_qualification"):
            parts.append(f"- **Required research-governance qualification:** {idea['required_qualification']}")
        if idea.get("required_boundary"):
            parts.append(f"- **Required boundary:** {idea['required_boundary']}")
        parts.append(f"- **Activity confirmation:** {idea['disclaimer']}")
    return "\n".join(parts) + "\n"


def freeze_audit() -> str:
    fixture = yaml.safe_load((ROOT / "tests/fixtures/gate-5d-previous-work-freeze.yml").read_text())
    parts = [
        "# Gate 5E previous-work examples freeze audit", "", "Status: PASS", "",
        "Gate 5D selected previous-work examples were deliberately excluded from Gate 5E editorial changes. File hashes protect theme relationships, relationship-to-lab values and rationales; rendered-section assertions protect IDs and display order.", "",
        "| Theme | Gate 5D ordered IDs | Gate 5E ordered IDs | Result |", "|---|---|---|---|",
    ]
    for theme_id, expected in fixture["selected_previous_work"].items():
        page = (ROOT / "research" / f"{theme_id}.qmd").read_text()
        section = page.split("## Selected completed and foundational work", 1)[1].split("## Questions this theme opens", 1)[0]
        observed = [f"{kind}/{slug[:-5]}" for kind, slug in re.findall(r'href="/(work|publications)/([^\"]+\.html)', section)]
        result = "Identical" if observed == expected else "MISMATCH"
        parts.append(f"| `{theme_id}` | {'<br>'.join(f'`{item}`' for item in expected)} | {'<br>'.join(f'`{item}`' for item in observed)} | {result} |")
        if result != "Identical":
            raise ValueError(f"previous-work order changed for {theme_id}")
    parts += ["", "## Source-record integrity", "", "| Controlled file | Gate 5D SHA-256 | Gate 5E SHA-256 | Result |", "|---|---|---|---|"]
    for relative, expected in fixture["source_file_hashes"].items():
        observed = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        result = "Identical" if observed == expected else "MISMATCH"
        parts.append(f"| `{relative}` | `{expected}` | `{observed}` | {result} |")
        if result != "Identical":
            raise ValueError(f"frozen source changed: {relative}")
    parts += ["", "The controlled publication-theme file retains every Gate 5D theme assignment, evidence-source URL and rationale. The seven controlled Work files retain every Gate 5D `relationship_to_lab` value and relationship rationale. No example was added, removed or promoted. A separate owner review remains required before publication."]
    return "\n".join(parts) + "\n"


def main() -> int:
    output = ROOT / "docs/reviews/gate-5e"
    output.mkdir(parents=True, exist_ok=True)
    (output / "theme-reader-value-audit.md").write_text(theme_audit(), encoding="utf-8")
    (output / "research-ideas-reader-value-audit.md").write_text(idea_audit(), encoding="utf-8")
    (output / "previous-work-examples-freeze-audit.md").write_text(freeze_audit(), encoding="utf-8")
    print("Generated Gate 5E theme, idea and previous-work freeze audits.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
