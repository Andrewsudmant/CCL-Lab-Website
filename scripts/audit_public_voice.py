#!/usr/bin/env python3
"""Deterministic public-voice diagnostics; reports text patterns without editing."""

from __future__ import annotations

import argparse
import html
import re
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORD = re.compile(r"[A-Za-z0-9]+(?:[’'-][A-Za-z0-9]+)*")
SENTENCE = re.compile(r"(?<=[.!?])\s+")
STOCK = (
    "at the intersection of", "in an increasingly complex landscape", "critical role", "robust framework",
    "holistic", "multifaceted", "transformative", "leverage", "leveraging", "foster", "fostering",
    "meaningful impact", "unlock", "navigate", "cutting-edge", "innovative solutions", "evidence to action",
    "scaling what works", "this theme examines", "this work seeks to", "it is important to note",
    "has important implications",
)
ABSTRACT = {
    "authority", "finance", "capability", "coordination", "participation", "sequencing", "maintenance",
    "relevance", "uncertainty", "delivery", "consequences", "implementation", "appraisal", "distribution",
    "governance", "infrastructure", "knowledge", "evidence", "responsibility", "capacity", "interpretation",
}


class PublicText(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hidden = 0
        self.in_main = 0
        self.parts: list[str] = []
        self.headings: list[str] = []
        self.heading_tag: str | None = None
        self.heading_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if tag == "main": self.in_main += 1
        if tag in {"script", "style", "noscript"} or attr.get("aria-hidden") == "true": self.hidden += 1
        if tag in {"h1", "h2", "h3", "h4"} and self.in_main and not self.hidden:
            self.heading_tag, self.heading_parts = tag, []

    def handle_endtag(self, tag: str) -> None:
        if tag == self.heading_tag:
            self.headings.append(" ".join(self.heading_parts).strip())
            self.heading_tag = None
        if tag in {"script", "style", "noscript"} and self.hidden: self.hidden -= 1
        if tag == "main" and self.in_main: self.in_main -= 1

    def handle_data(self, data: str) -> None:
        if self.in_main and not self.hidden:
            value = " ".join(html.unescape(data).split())
            if value:
                self.parts.append(value)
                if self.heading_tag: self.heading_parts.append(value)


def parse_page(path: Path) -> tuple[str, list[str]]:
    parser = PublicText(); parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
    text = " ".join(parser.parts)
    shared_banner = "Draft website The Cities and Climate Learning Lab is being established at Simon Fraser University. Some descriptions of developing research and possible future work will continue to be refined."
    return text.replace(shared_banner, ""), parser.headings


def page_key(site_dir: Path, path: Path) -> str:
    return path.relative_to(site_dir).as_posix()


def repeated_phrases(texts: dict[str, str]) -> list[tuple[str, int]]:
    counts: Counter[str] = Counter()
    for text in texts.values():
        words = [w.casefold() for w in WORD.findall(text)]
        seen = {" ".join(words[i:i+n]) for n in (4, 5, 6) for i in range(len(words)-n+1)}
        counts.update(seen)
    return sorted(((p, c) for p, c in counts.items() if c >= 3), key=lambda x: (-x[1], x[0]))[:40]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-dir", default="_site")
    parser.add_argument("--output", default="reports/editorial/gate-5h-public-voice-diagnostic.md")
    args = parser.parse_args()
    site_dir = ROOT / args.site_dir
    pages = sorted(site_dir.rglob("*.html"))
    parsed = {page_key(site_dir, p): parse_page(p) for p in pages}
    texts = {k: v[0] for k, v in parsed.items()}
    all_text = "\n".join(texts.values())
    sentences = [(page, s.strip()) for page, text in texts.items() for s in SENTENCE.split(text) if s.strip()]
    openings = Counter(" ".join(WORD.findall(s.casefold())[:4]) for _, s in sentences if len(WORD.findall(s)) >= 4)
    long_sentences = [(p, s, len(WORD.findall(s))) for p, s in sentences if len(WORD.findall(s)) > 30]
    headings = Counter(tuple(h.casefold() for h in hs[i:i+3]) for _, hs in parsed.values() for i in range(max(0, len(hs)-2)))
    abstract_series = []
    for page, text in texts.items():
        for match in re.finditer(r"\b(?:[A-Za-z-]+,\s*){3,}[A-Za-z-]+(?:\s+and\s+[A-Za-z-]+)?", text):
            nouns = [w.casefold() for w in WORD.findall(match.group())]
            if sum(w in ABSTRACT for w in nouns) >= 4: abstract_series.append((page, match.group()))
    terms = yaml.safe_load((ROOT / "config/plain_language_terms.yml").read_text())["terms"]
    allowlist_path = ROOT / "config/public_voice_allowlist.yml"
    allowlist = {item["phrase"]: item for item in yaml.safe_load(allowlist_path.read_text())["entries"]}
    term_order = []
    for item in terms:
        for page in item["pages"]:
            text = texts.get(page, "").replace("’", "'").casefold()
            term_at = text.find(item["technical_term"].replace("’", "'").casefold())
            plain_at = text.find(item["plain_first_use"].replace("’", "'").casefold())
            if term_at >= 0 and (plain_at < 0 or term_at < plain_at): term_order.append((page, item["technical_term"]))
    freq_phrases = ["does not by itself", "not simply", "not merely", "not only", "this theme examines", "this work asks"]
    output = ["# Gate 5H public-voice diagnostic", "", f"Rendered pages inspected: **{len(pages)}**. This deterministic report supports human editorial judgement; it is not a readability score or an automatic release gate, and it never rewrites copy.", "", "## Phrase frequencies", ""]
    output += [f"- `{p}`: {all_text.casefold().count(p)}" for p in freq_phrases]
    output += [f"- `may`: {len(re.findall(r'\bmay\b', all_text, re.I))}", f"- `could`: {len(re.findall(r'\bcould\b', all_text, re.I))}", f"- `can`: {len(re.findall(r'\bcan\b', all_text, re.I))}"]
    output += ["", "## Stock phrases", ""]
    for phrase in STOCK:
        count = len(re.findall(rf'\b{re.escape(phrase)}\b', all_text, re.I))
        note = ""
        if phrase in allowlist:
            item = allowlist[phrase]
            note = f" — allow-listed up to {item['maximum_occurrences']} occurrence(s) on {', '.join(item['pages'])}: {item['reason']}"
        output.append(f"- `{phrase}`: {count}{note}")
    output += ["", "## Repeated four-word-or-longer phrases across pages", ""] + ([f"- {c} pages: `{p}`" for p, c in repeated_phrases(texts)] or ["- None at the three-page reporting threshold."])
    output += ["", "## Repeated sentence openings", ""] + ([f"- {c} times: `{p}`" for p, c in openings.most_common() if c >= 3][:30] or ["- None at the three-sentence reporting threshold."])
    output += ["", "## Sentences over 30 words", ""] + ([f"- `{p}` ({n} words): {s}" for p, s, n in long_sentences] or ["- None."])
    output += ["", "## Abstract-noun series", ""] + ([f"- `{p}`: {s}" for p, s in abstract_series] or ["- None detected."])
    output += ["", "## Repeated visible heading sequences", ""] + ([f"- {c} pages: {' / '.join(h)}" for h, c in headings.items() if c >= 2] or ["- None."])
    output += ["", "## Technical terms used before mapped plain first use", ""] + ([f"- `{p}`: {t}" for p, t in term_order] or ["- None on mapped pages."])
    target = ROOT / args.output; target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(output) + "\n", encoding="utf-8")
    print(f"Public-voice diagnostic written to {target.relative_to(ROOT)} for {len(pages)} pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
