#!/usr/bin/env python3
"""Validate the compact, large-chapter course model."""

from data.course import CHAPTERS, PHASES, SOURCES


def main() -> None:
    assert len(PHASES) == 5, "expected five phases"
    assert len(CHAPTERS) == 12, "expected twelve large chapters"
    assert [chapter["number"] for chapter in CHAPTERS] == list(range(1, 13))
    assert sorted(number for phase in PHASES for number in phase["chapters"]) == list(range(1, 13))
    assert [chapter["number"] for chapter in CHAPTERS if chapter["ready"]] == list(range(1, 13))
    assert [chapter["href"] for chapter in CHAPTERS] == [
        "chapter-01-attack-surface.html",
        "chapter-02-http-request.html",
        "chapter-03-information-exposure.html",
        "chapter-04-identity.html",
        "chapter-05-authorization.html",
        "chapter-06-injection.html",
        "chapter-07-browser-security.html",
        "chapter-08-file-security.html",
        "chapter-09-ssrf-api.html",
        "chapter-10-deployment-security.html",
        "chapter-11-availability.html",
        "chapter-12-incident-response.html",
    ]
    for chapter in CHAPTERS:
        assert chapter["title"] and chapter["english"] and chapter["summary"] and chapter["duration"]
        assert len(chapter["topics"]) == 5
    assert len(SOURCES) >= 4
    assert all(source["url"].startswith("https://") for source in SOURCES)
    print("Validated 5 phases and all 12 complete large chapters.")


if __name__ == "__main__":
    main()
