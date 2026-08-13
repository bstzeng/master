#!/usr/bin/env python3
"""Validate the Korean curriculum data before generating pages."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "curriculum.json"
ALPHABET_DATA = ROOT / "data" / "alphabet.json"
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
EXPECTED_LESSONS = {
    1: 4, 2: 4, 3: 5, 4: 5, 5: 5, 6: 6,
    7: 6, 8: 6, 9: 5, 10: 5, 11: 5,
    12: 5, 13: 6, 14: 5, 15: 6, 16: 5, 17: 5,
    18: 5, 19: 6, 20: 5, 21: 6, 22: 5, 23: 6,
    24: 7, 25: 7, 26: 8,
}


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> None:
    errors: list[str] = []
    data = json.loads(DATA.read_text(encoding="utf-8"))
    units = list(data.get("units", []))
    for path in sorted((ROOT / "data").glob("phase-[2-5].json")):
        units.extend(json.loads(path.read_text(encoding="utf-8")))
    units.sort(key=lambda item: item["number"])
    data["units"] = units
    alphabet = json.loads(ALPHABET_DATA.read_text(encoding="utf-8"))
    phases = data.get("phases", [])
    outline = data.get("outline_units", [])
    units = data.get("units", [])

    require([item.get("number") for item in phases] == list(range(1, 6)), "phases must be numbered 1 through 5", errors)
    require([item.get("number") for item in outline] == list(range(1, 27)), "outline units must be numbered 1 through 26", errors)
    require([item.get("number") for item in units] == list(range(1, 27)), "ready units must be numbered 1 through 26", errors)
    require(sum(len(item.get("lessons", [])) for item in units) == sum(EXPECTED_LESSONS.values()), "course must contain exactly 143 lessons", errors)
    vowels = [item for group in alphabet.get("vowel_groups", []) for item in group.get("items", [])]
    consonants = [item for group in alphabet.get("consonant_groups", []) for item in group.get("items", [])]
    require(len(vowels) == 21, "alphabet course must contain exactly 21 vowels", errors)
    require(len(consonants) == 19, "alphabet course must contain exactly 19 consonants", errors)
    require(len({item.get("letter") for item in vowels}) == 21, "vowel letters must be unique", errors)
    require(len({item.get("letter") for item in consonants}) == 19, "consonant letters must be unique", errors)
    for item in vowels + consonants:
        require(bool(item.get("speak")), f"alphabet {item.get('letter', '?')}: missing speech target", errors)
    for item in vowels:
        require(bool(item.get("romanization")), f"vowel {item.get('letter', '?')}: missing RR", errors)
    for item in consonants:
        require(bool(item.get("name_rr")) and bool(item.get("onset")), f"consonant {item.get('letter', '?')}: missing RR", errors)

    outline_by_number = {item["number"]: item for item in outline}
    unit_slugs: set[str] = set()
    for unit in units:
        label = f"unit {unit.get('number', '?')}"
        unit_slug = str(unit.get("slug", ""))
        require(SLUG.fullmatch(unit_slug) is not None, f"{label}: invalid slug", errors)
        require(unit_slug not in unit_slugs, f"{label}: duplicate unit slug", errors)
        unit_slugs.add(unit_slug)
        require(unit.get("title") == outline_by_number.get(unit.get("number"), {}).get("title"), f"{label}: title must match outline", errors)
        require(len(unit.get("prerequisites", [])) >= 2, f"{label}: needs prerequisites", errors)
        require(len(unit.get("outcomes", [])) >= 3, f"{label}: needs outcomes", errors)
        if unit.get("number", 0) > 6:
            require(len(unit.get("prerequisites", [])) == 3, f"{label}: needs exactly 3 prerequisites", errors)
            require(len(unit.get("outcomes", [])) == 4, f"{label}: needs exactly 4 outcomes", errors)
        lessons = unit.get("lessons", [])
        require(len(lessons) == EXPECTED_LESSONS.get(unit.get("number")), f"{label}: unexpected lesson count", errors)
        require([item.get("number") for item in lessons] == list(range(1, len(lessons) + 1)), f"{label}: lesson numbers must be consecutive", errors)
        lesson_slugs: set[str] = set()
        for lesson in lessons:
            lesson_label = f"{label}, lesson {lesson.get('number', '?')}"
            slug = str(lesson.get("slug", ""))
            require(SLUG.fullmatch(slug) is not None, f"{lesson_label}: invalid slug", errors)
            require(slug not in lesson_slugs, f"{lesson_label}: duplicate slug", errors)
            lesson_slugs.add(slug)
            require(len(lesson.get("objectives", [])) >= 2, f"{lesson_label}: needs at least 2 objectives", errors)
            if unit.get("number", 0) > 6:
                require(len(lesson.get("objectives", [])) == 3, f"{lesson_label}: needs exactly 3 objectives", errors)
            require(len(lesson.get("sections", [])) == 3, f"{lesson_label}: needs exactly 3 sections", errors)
            require(len(lesson.get("takeaways", [])) == 3, f"{lesson_label}: needs exactly 3 takeaways", errors)
            require(len(lesson.get("quiz", [])) == 2, f"{lesson_label}: needs exactly 2 quiz items", errors)
            require(len(lesson.get("practice", [])) == 2, f"{lesson_label}: needs exactly 2 practice items", errors)
            audio_count = 0
            for index, section in enumerate(lesson.get("sections", []), 1):
                require(bool(section.get("heading")), f"{lesson_label}, section {index}: missing heading", errors)
                require(bool(section.get("paragraphs")), f"{lesson_label}, section {index}: missing paragraphs", errors)
                require(bool(section.get("bullets")), f"{lesson_label}, section {index}: missing bullets", errors)
                if unit.get("number", 0) > 6:
                    require(len(section.get("paragraphs", [])) == 1, f"{lesson_label}, section {index}: needs exactly 1 paragraph", errors)
                    require(len(section.get("bullets", [])) == 3, f"{lesson_label}, section {index}: needs exactly 3 bullets", errors)
                    require(2 <= len(section.get("audio", [])) <= 4, f"{lesson_label}, section {index}: needs 2 to 4 audio items", errors)
                for audio in section.get("audio", []):
                    audio_count += 1
                    require(bool(audio.get("text")), f"{lesson_label}, section {index}: audio needs text", errors)
                    require(bool(audio.get("meaning")), f"{lesson_label}, section {index}: audio needs meaning", errors)
            require(audio_count >= 2, f"{lesson_label}: needs at least 2 pronunciation items", errors)
            for index, quiz in enumerate(lesson.get("quiz", []), 1):
                require(bool(quiz.get("question")) and bool(quiz.get("answer")), f"{lesson_label}, quiz {index}: needs question and answer", errors)

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        raise SystemExit(1)
    lesson_count = sum(len(item.get("lessons", [])) for item in units)
    print(f"Validated 21 vowels, 19 consonants, {len(phases)} phases, {len(outline)} outline units, {len(units)} ready units and {lesson_count} lessons.")


if __name__ == "__main__":
    main()
