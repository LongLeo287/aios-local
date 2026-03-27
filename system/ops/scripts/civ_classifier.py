#!/usr/bin/env python3
"""
ops/scripts/civ_classifier.py — C4: Auto-Classifier (URL/text → type + route)
Input: any string CEO pastes (URL, "Ý tưởng:" text, file path, etc.)
Output: {type, confidence, route, suggested_agent}

Usage:
  python ops/scripts/civ_classifier.py "https://github.com/org/repo"
  python ops/scripts/civ_classifier.py "Ý tưởng: voice input"
  python ops/scripts/civ_classifier.py --stdin   # read from stdin
"""
import re
import sys
import json
from typing import NamedTuple

class Classification(NamedTuple):
    type: str           # REPO | WEB | DOC | TOOL | IDEA | PAPER | VIDEO | PLUGIN
    confidence: str     # HIGH | MEDIUM | LOW
    route: str          # which dept/kho to route to
    agent: str          # which agent handles it
    label: str          # human-readable label

RULES = [
    # GitHub repos
    (r"github\.com/[\w\-]+/[\w\-]+",  "REPO",   "HIGH",   "skills/ or plugins/",     "repo-fetcher",       "GitHub Repository"),
    # arXiv / papers
    (r"arxiv\.org|papers\.ssrn",       "PAPER",  "HIGH",   "brain/knowledge/notes/",  "content-analyst-agent", "Research Paper"),
    # YouTube / video
    (r"youtu\.be|youtube\.com/watch",  "VIDEO",  "HIGH",   "brain/knowledge/notes/",  "web-crawler",        "Video (transcript)"),
    # PDF documents
    (r"\.pdf($|\?)",                   "DOC",    "HIGH",   "brain/knowledge/notes/",  "doc-parser",         "PDF Document"),
    # NPM / PyPI / package
    (r"npmjs\.com|pypi\.org|pkg\.go",  "TOOL",   "HIGH",   "kho/plugins/ or kho/llm/","strix-agent",        "Package/Library"),
    # General URL (web article / blog)
    (r"https?://",                     "WEB",    "MEDIUM", "brain/knowledge/notes/",  "web-crawler",        "Web Article/Blog"),
    # Idea / feature request
    (r"^(Ý tưởng|idea|feature|tính năng|đề xuất)[:：]", "IDEA", "HIGH", "rd/experiments/", "rd-lead-agent", "CEO Idea → R&D"),
    # Tool / plugin mention
    (r"(plugin|tool|extension|cli|sdk)\b", "TOOL", "LOW",  "kho/plugins/",            "strix-agent",        "Tool/Plugin mention"),
]

def classify(text: str) -> Classification:
    text_clean = text.strip()
    for pattern, typ, conf, route, agent, label in RULES:
        if re.search(pattern, text_clean, re.IGNORECASE):
            return Classification(typ, conf, route, agent, label)
    return Classification("UNKNOWN", "LOW", "brain/knowledge/notes/", "content-analyst-agent", "Unknown — manual review")

def main():
    if "--stdin" in sys.argv:
        text = sys.stdin.read().strip()
    elif len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        print("Usage: civ_classifier.py <url_or_text>")
        return

    c = classify(text)
    result = {
        "input": text[:100],
        "type": c.type,
        "confidence": c.confidence,
        "route": c.route,
        "agent": c.agent,
        "label": c.label,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result

if __name__ == "__main__":
    main()
