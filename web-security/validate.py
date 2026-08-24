#!/usr/bin/env python3
"""Validate the compact, large-chapter course model."""

from data.course import CHAPTERS, PHASES, SOURCES


def main() -> None:
    assert len(PHASES) == 5, "expected five phases"
    assert len(CHAPTERS) == 12, "expected twelve large chapters"
    assert [chapter["number"] for chapter in CHAPTERS] == list(range(1, 13))
    assert sorted(number for phase in PHASES for number in phase["chapters"]) == list(range(1, 13))
    assert [chapter["number"] for chapter in CHAPTERS if chapter["ready"]] == [1]
    assert CHAPTERS[0]["href"] == "chapter-01-attack-surface.html"
    for chapter in CHAPTERS:
        assert chapter["title"] and chapter["english"] and chapter["summary"] and chapter["duration"]
        assert len(chapter["topics"]) == 5
    assert len(SOURCES) >= 4
    assert all(source["url"].startswith("https://") for source in SOURCES)
    print("Validated 5 phases, 12 large chapters, and 4 primary references.")


if __name__ == "__main__":
    main()
