#!/usr/bin/env python3
"""Validate the sixty-unit Tolkien legendarium course source data."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from data.course import PHASES, all_units  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    units = all_units()
    require(len(PHASES) == 10, "course must have ten phases")
    require(len(units) == 60, f"course must have 60 units, found {len(units)}")
    require([item["number"] for item in units] == list(range(1, 61)), "unit numbers must be continuous")
    require(sum(len(phase["units"]) for phase in PHASES) == 60, "phase unit counts must total 60")
    require({number for phase in PHASES for number in phase["units"]} == set(range(1, 61)), "phase coverage must be exact")
    slugs = set()
    total_sections = 0
    total_quiz = 0
    for item in units:
        label = f"unit {item['number']:02d}"
        require(re.fullmatch(r"[a-z0-9-]+", item["slug"]) is not None, f"{label}: invalid slug")
        require(item["slug"] not in slugs, f"{label}: duplicate slug")
        slugs.add(item["slug"])
        expected_phase = next(phase["number"] for phase in PHASES if item["number"] in phase["units"])
        require(item["phase"] == expected_phase, f"{label}: wrong phase")
        for field in ("title", "english", "timeframe", "subtitle", "opening", "practice"):
            require(str(item.get(field, "")).strip(), f"{label}: missing {field}")
        require(len(item["opening"]) >= 70, f"{label}: opening is shorter than 70 characters")
        require(len(item["objectives"]) == 3, f"{label}: expected three objectives")
        require(len(item["sections"]) == 4, f"{label}: expected four sections")
        total_sections += len(item["sections"])
        for index, section in enumerate(item["sections"], 1):
            for field in ("heading", "body", "lens"):
                require(str(section.get(field, "")).strip(), f"{label} section {index}: missing {field}")
            require(len(section["body"]) >= 90, f"{label} section {index}: body shorter than 90 characters")
            require(len(section["points"]) == 4, f"{label} section {index}: expected four points")
            require(len(section["lens"]) >= 30, f"{label} section {index}: lens shorter than 30 characters")
        require(3 <= len(item["characters"]) <= 6, f"{label}: expected three to six characters")
        for index, character in enumerate(item["characters"], 1):
            for field in ("name", "role", "arc"):
                require(str(character.get(field, "")).strip(), f"{label} character {index}: missing {field}")
            require(len(character["arc"]) >= 25, f"{label} character {index}: arc shorter than 25 characters")
        require(len(item["connections"]) == 3, f"{label}: expected three connections")
        require(len(item["takeaways"]) == 4, f"{label}: expected four takeaways")
        require(len(item["quiz"]) == 3, f"{label}: expected three quiz questions")
        total_quiz += len(item["quiz"])
        for index, qa in enumerate(item["quiz"], 1):
            require(isinstance(qa, tuple) and len(qa) == 2, f"{label} quiz {index}: expected question-answer tuple")
            require(all(str(value).strip() for value in qa), f"{label} quiz {index}: empty question or answer")
        require(2 <= len(item["sources"]) <= 4, f"{label}: expected two to four sources")
        for index, source in enumerate(item["sources"], 1):
            for field in ("title", "url", "note"):
                require(str(source.get(field, "")).strip(), f"{label} source {index}: missing {field}")
            require(source["url"].startswith("https://"), f"{label} source {index}: URL must use HTTPS")
    require(total_sections == 240, f"expected 240 sections, found {total_sections}")
    require(total_quiz == 180, f"expected 180 quiz questions, found {total_quiz}")
    print("Validated 10 phases, 60 units, 240 teaching sections and 180 quiz questions.")


if __name__ == "__main__":
    main()
