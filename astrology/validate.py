#!/usr/bin/env python3
"""Validate the astrology course source data."""

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
    require(len(PHASES) == 5, "course must have five phases")
    require(len(units) == 36, "course must have 36 units")
    require([unit["number"] for unit in units] == list(range(1, 37)), "unit numbers must be continuous")
    require(sum(len(phase["units"]) for phase in PHASES) == 36, "phase unit counts must total 36")
    require({number for phase in PHASES for number in phase["units"]} == set(range(1, 37)), "phase coverage must be exact")
    slugs = set()
    for unit in units:
        label = f"unit {unit['number']:02d}"
        require(re.fullmatch(r"[a-z0-9-]+", unit["slug"]) is not None, f"{label}: invalid slug")
        require(unit["slug"] not in slugs, f"{label}: duplicate slug")
        slugs.add(unit["slug"])
        for field in ("title", "english", "subtitle", "opening", "practice"):
            require(str(unit.get(field, "")).strip(), f"{label}: missing {field}")
        require(len(unit["objectives"]) == 3, f"{label}: expected three objectives")
        expected_sections = 5 if 12 <= unit["number"] <= 23 else 4
        require(len(unit["sections"]) == expected_sections, f"{label}: expected {expected_sections} sections")
        for index, section in enumerate(unit["sections"], 1):
            for field in ("heading", "body", "note"):
                require(str(section.get(field, "")).strip(), f"{label} section {index}: missing {field}")
            require(3 <= len(section["points"]) <= 6, f"{label} section {index}: expected 3–6 points")
            require(len(section["body"]) >= 25, f"{label} section {index}: body too short")
        require(len(unit["takeaways"]) == 4, f"{label}: expected four takeaways")
        require(len(unit["quiz"]) == 3, f"{label}: expected three quiz questions")
        require(2 <= len(unit["sources"]) <= 4, f"{label}: expected two to four sources")
    print("Validated 5 phases, 36 units, 156 teaching sections and 108 quiz questions.")


if __name__ == "__main__":
    main()
