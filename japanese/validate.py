#!/usr/bin/env python3
"""Validate the complete Japanese curriculum data."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "curriculum.json"
KANA_DATA = ROOT / "data" / "kana.json"
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
KANJI = re.compile(r"[一-龯々〆ヶ]")
KANA = re.compile(r"[ぁ-ゖァ-ヺー]")
EXPECTED_LESSONS = {
    1: 4, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5,
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
    units = []
    for path in sorted((ROOT / "data").glob("phase-[1-5].json")):
        units.extend(json.loads(path.read_text(encoding="utf-8")))
    units.sort(key=lambda item: item["number"])
    phases = data["phases"]
    outline = data["outline_units"]
    require([item["number"] for item in phases] == list(range(1, 6)), "phases must be 1 through 5", errors)
    require([item["number"] for item in outline] == list(range(1, 27)), "outline units must be 1 through 26", errors)
    require([item["number"] for item in units] == list(range(1, 27)), "ready units must be 1 through 26", errors)
    require(sum(len(item.get("lessons", [])) for item in units) == 143, "course must contain exactly 143 lessons", errors)
    outline_by_number = {item["number"]: item for item in outline}
    unit_slugs: set[str] = set()
    for unit in units:
        label = f"unit {unit.get('number', '?')}"
        slug = str(unit.get("slug", ""))
        require(SLUG.fullmatch(slug) is not None, f"{label}: invalid slug", errors)
        require(slug not in unit_slugs, f"{label}: duplicate slug", errors)
        unit_slugs.add(slug)
        require(unit.get("title") == outline_by_number.get(unit.get("number"), {}).get("title"), f"{label}: title must match outline", errors)
        require(bool(unit.get("japanese_title")), f"{label}: missing Japanese title", errors)
        require(len(unit.get("prerequisites", [])) == 3, f"{label}: needs 3 prerequisites", errors)
        require(len(unit.get("outcomes", [])) == 4, f"{label}: needs 4 outcomes", errors)
        lessons = unit.get("lessons", [])
        require(len(lessons) == EXPECTED_LESSONS.get(unit.get("number")), f"{label}: unexpected lesson count", errors)
        require([item.get("number") for item in lessons] == list(range(1, len(lessons) + 1)), f"{label}: lesson numbers must be consecutive", errors)
        lesson_slugs: set[str] = set()
        for lesson in lessons:
            lesson_label = f"{label}, lesson {lesson.get('number', '?')}"
            lesson_slug = str(lesson.get("slug", ""))
            require(SLUG.fullmatch(lesson_slug) is not None, f"{lesson_label}: invalid slug", errors)
            require(lesson_slug not in lesson_slugs, f"{lesson_label}: duplicate slug", errors)
            lesson_slugs.add(lesson_slug)
            require(len(lesson.get("objectives", [])) == 3, f"{lesson_label}: needs 3 objectives", errors)
            require(len(lesson.get("sections", [])) == 3, f"{lesson_label}: needs 3 sections", errors)
            require(len(lesson.get("takeaways", [])) == 3, f"{lesson_label}: needs 3 takeaways", errors)
            require(len(lesson.get("quiz", [])) == 2, f"{lesson_label}: needs 2 quiz items", errors)
            require(len(lesson.get("practice", [])) == 2, f"{lesson_label}: needs 2 practice items", errors)
            for index, section in enumerate(lesson.get("sections", []), 1):
                section_label = f"{lesson_label}, section {index}"
                require(bool(section.get("heading")), f"{section_label}: missing heading", errors)
                require(len(section.get("paragraphs", [])) == 1, f"{section_label}: needs 1 paragraph", errors)
                require(len(section.get("bullets", [])) == 3, f"{section_label}: needs 3 bullets", errors)
                require(2 <= len(section.get("audio", [])) <= 4, f"{section_label}: needs 2 to 4 audio items", errors)
                for audio in section.get("audio", []):
                    reading = str(audio.get("reading", ""))
                    text = str(audio.get("text", ""))
                    spoken = str(audio.get("speak", text))
                    require(bool(audio.get("text")), f"{section_label}: audio missing text", errors)
                    require(bool(reading), f"{section_label}: audio missing reading", errors)
                    require(bool(audio.get("meaning")), f"{section_label}: audio missing meaning", errors)
                    require(KANA.search(reading) is not None, f"{section_label}: reading needs kana: {reading}", errors)
                    require(KANJI.search(reading) is None, f"{section_label}: reading must not contain kanji: {reading}", errors)
                    require(re.search(r"[A-Za-z]", reading) is None, f"{section_label}: reading must not contain roman letters: {reading}", errors)
                    require(KANA.search(spoken) is not None or KANJI.search(spoken) is not None, f"{section_label}: TTS target needs Japanese: {spoken}", errors)
                    if re.search(r"[0-9%+/:]", text):
                        require(bool(audio.get("speak")), f"{section_label}: numeric or symbolic text needs speak: {text}", errors)
            for quiz in lesson.get("quiz", []):
                require(bool(quiz.get("question")) and bool(quiz.get("answer")), f"{lesson_label}: incomplete quiz", errors)
    kana = json.loads(KANA_DATA.read_text(encoding="utf-8"))
    hiragana = [item for group in kana["hiragana_groups"] for item in group["items"]]
    katakana = [item for group in kana["katakana_groups"] for item in group["items"]]
    require(len(hiragana) == 46, "kana page must contain 46 hiragana", errors)
    require(len(katakana) == 46, "kana page must contain 46 katakana", errors)
    require(len({item["letter"] for item in hiragana}) == 46, "hiragana must be unique", errors)
    require(len({item["letter"] for item in katakana}) == 46, "katakana must be unique", errors)
    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors))
        raise SystemExit(1)
    print("Validated 46 hiragana, 46 katakana, 5 phases, 26 units and 143 lessons.")


if __name__ == "__main__":
    main()
