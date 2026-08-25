#!/usr/bin/env python3
"""Validate course data before rendering."""

from data.chapters_01_04 import CHAPTERS_01_04
from data.chapters_05_08 import CHAPTERS_05_08
from data.chapters_09_12 import CHAPTERS_09_12
from data.course import CHAPTERS, PHASES


def main():
    lessons = CHAPTERS_01_04 + CHAPTERS_05_08 + CHAPTERS_09_12
    assert len(PHASES) == 5
    assert len(CHAPTERS) == len(lessons) == 12
    assert [lesson["number"] for lesson in lessons] == list(range(1, 13))
    for meta, lesson in zip(CHAPTERS, lessons):
        assert meta["ready"] and len(meta["topics"]) == 5
        assert len(lesson["sections"]) == 8
        assert len(lesson["questions"]) == 5
        assert len(lesson["recap"]) == 4
        assert len(lesson["assignment"]["steps"]) == 4
        assert len(lesson["sources"]) >= 3
        for section in lesson["sections"]:
            assert len(section["paragraphs"]) == 2
            assert len(section["visual"]["items"]) == 4
    print("Validated 5 phases and 12 complete high-density chapters.")


if __name__ == "__main__":
    main()
