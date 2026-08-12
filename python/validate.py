#!/usr/bin/env python3
"""Validate course data before generating pages."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
REQUIRED_UNIT_FIELDS = {"number", "phase", "slug", "title", "english", "summary", "goal", "prerequisites", "outcomes", "lessons"}
REQUIRED_LESSON_FIELDS = {"number", "slug", "title", "subtitle", "duration", "difficulty", "summary", "objectives", "sections", "takeaways", "quiz", "practice"}
REQUIRED_SECTION_FIELDS = {"heading", "paragraphs", "bullets"}
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> None:
    errors: list[str] = []
    paths = sorted(DATA_DIR.glob("unit-*.json"))
    units = []
    for path in paths:
        try:
            unit = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path.name}: invalid JSON: {exc}")
            continue
        units.append(unit)
        label = path.name
        require(REQUIRED_UNIT_FIELDS <= unit.keys(), f"{label}: missing unit fields {REQUIRED_UNIT_FIELDS - unit.keys()}", errors)
        require(SLUG.match(str(unit.get("slug", ""))) is not None, f"{label}: invalid unit slug", errors)
        require(isinstance(unit.get("lessons"), list) and len(unit["lessons"]) >= 4, f"{label}: needs at least 4 lessons", errors)
        lesson_numbers = []
        lesson_slugs = set()
        for lesson in unit.get("lessons", []):
            lesson_label = f"{label} lesson {lesson.get('number', '?')}"
            require(REQUIRED_LESSON_FIELDS <= lesson.keys(), f"{lesson_label}: missing lesson fields {REQUIRED_LESSON_FIELDS - lesson.keys()}", errors)
            require(SLUG.match(str(lesson.get("slug", ""))) is not None, f"{lesson_label}: invalid slug", errors)
            require(lesson.get("slug") not in lesson_slugs, f"{lesson_label}: duplicate slug", errors)
            lesson_slugs.add(lesson.get("slug"))
            lesson_numbers.append(lesson.get("number"))
            require(len(lesson.get("objectives", [])) >= 2, f"{lesson_label}: needs at least 2 objectives", errors)
            require(len(lesson.get("sections", [])) >= 3, f"{lesson_label}: needs at least 3 sections", errors)
            require(len(lesson.get("takeaways", [])) >= 3, f"{lesson_label}: needs at least 3 takeaways", errors)
            require(len(lesson.get("quiz", [])) >= 2, f"{lesson_label}: needs at least 2 quiz items", errors)
            require(len(lesson.get("practice", [])) >= 2, f"{lesson_label}: needs at least 2 practice items", errors)
            for section_index, section in enumerate(lesson.get("sections", []), 1):
                require(REQUIRED_SECTION_FIELDS <= section.keys(), f"{lesson_label} section {section_index}: missing {REQUIRED_SECTION_FIELDS - section.keys()}", errors)
                require(bool(section.get("paragraphs")), f"{lesson_label} section {section_index}: paragraphs cannot be empty", errors)
            for quiz_index, quiz in enumerate(lesson.get("quiz", []), 1):
                require(bool(quiz.get("question")) and bool(quiz.get("answer")), f"{lesson_label} quiz {quiz_index}: needs question and answer", errors)
        require(lesson_numbers == list(range(1, len(lesson_numbers) + 1)), f"{label}: lesson numbers must be consecutive from 1", errors)

    unit_numbers = [unit.get("number") for unit in units]
    if len(paths) == 16:
        require(unit_numbers == list(range(1, 17)), "unit numbers must be 1 through 16", errors)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        raise SystemExit(1)
    print(f"Validated {len(units)} units and {sum(len(unit['lessons']) for unit in units)} lessons.")


if __name__ == "__main__":
    main()
