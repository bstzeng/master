#!/usr/bin/env python3
"""Check Japanese HTML, links, romaji labels and bundled audio."""

from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


SITE_ROOT = Path(__file__).resolve().parent.parent
JAPANESE_ROOT = Path(__file__).resolve().parent


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.ids: set[str] = set()
        self.h1_count = 0
        self.title_count = 0
        self.speech_buttons = 0
        self.audio_sources: list[str] = []
        self.romanization_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        if tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")
        if tag == "link" and values.get("href"):
            self.links.append(values["href"] or "")
        if tag == "script" and values.get("src"):
            self.links.append(values["src"] or "")
        if tag == "h1":
            self.h1_count += 1
        if tag == "title":
            self.title_count += 1
        if tag == "button" and values.get("data-speak"):
            self.speech_buttons += 1
            if values.get("data-audio"):
                self.audio_sources.append(values["data-audio"] or "")
        if "romanization" in (values.get("class") or "").split():
            self.romanization_count += 1


def main() -> None:
    errors: list[str] = []
    pages = [SITE_ROOT / "index.html", *sorted(JAPANESE_ROOT.rglob("*.html"))]
    lesson_pages = list((JAPANESE_ROOT / "lessons").rglob("*.html"))
    unit_pages = list((JAPANESE_ROOT / "units").glob("*.html"))
    require_manifest = JAPANESE_ROOT / "audio" / "manifest.json"
    if len(lesson_pages) != 143:
        errors.append(f"expected 143 lesson pages, found {len(lesson_pages)}")
    if len(unit_pages) != 26:
        errors.append(f"expected 26 unit pages, found {len(unit_pages)}")
    if not require_manifest.exists():
        errors.append("missing audio manifest")
        expected_files: set[str] = set()
    else:
        expected_files = set(json.loads(require_manifest.read_text(encoding="utf-8"))["files"].values())
    actual_files = {path.name for path in (JAPANESE_ROOT / "audio").glob("*.mp3")}
    if actual_files != expected_files:
        errors.append(f"audio manifest mismatch: {len(expected_files)} expected, {len(actual_files)} present")
    for audio_file in (JAPANESE_ROOT / "audio").glob("*.mp3"):
        if audio_file.stat().st_size <= 1_000:
            errors.append(f"{audio_file.relative_to(SITE_ROOT)}: empty audio")
    for path in pages:
        parser = PageParser()
        parser.feed(path.read_text(encoding="utf-8"))
        if parser.h1_count != 1:
            errors.append(f"{path.relative_to(SITE_ROOT)}: expected one h1, found {parser.h1_count}")
        if parser.title_count != 1:
            errors.append(f"{path.relative_to(SITE_ROOT)}: expected one title, found {parser.title_count}")
        is_lesson = JAPANESE_ROOT / "lessons" in path.parents
        if is_lesson and parser.speech_buttons < 12:
            errors.append(f"{path.relative_to(SITE_ROOT)}: expected at least twelve speech controls")
        if is_lesson and len(parser.audio_sources) != parser.speech_buttons:
            errors.append(f"{path.relative_to(SITE_ROOT)}: every speech control needs bundled audio")
        if is_lesson and parser.romanization_count * 2 != parser.speech_buttons:
            errors.append(f"{path.relative_to(SITE_ROOT)}: every normal/slow pair needs one romaji label")
        if path == JAPANESE_ROOT / "kana.html" and parser.speech_buttons != 92:
            errors.append(f"{path.relative_to(SITE_ROOT)}: expected 92 kana controls")
        for source in parser.audio_sources:
            if not (path.parent / unquote(source)).resolve().exists():
                errors.append(f"{path.relative_to(SITE_ROOT)}: missing audio {source}")
        for raw_link in parser.links:
            parsed = urlsplit(raw_link)
            if parsed.scheme or raw_link.startswith("//"):
                continue
            target_path = unquote(parsed.path)
            if not target_path:
                if parsed.fragment and parsed.fragment not in parser.ids:
                    errors.append(f"{path.relative_to(SITE_ROOT)}: missing fragment #{parsed.fragment}")
                continue
            target = (path.parent / target_path).resolve()
            try:
                target.relative_to(SITE_ROOT.resolve())
            except ValueError:
                errors.append(f"{path.relative_to(SITE_ROOT)}: link escapes site root: {raw_link}")
                continue
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                errors.append(f"{path.relative_to(SITE_ROOT)}: missing target {raw_link}")
    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors))
        raise SystemExit(1)
    print(f"Checked {len(pages)} pages, including 143 lessons, with no broken links or audio.")


if __name__ == "__main__":
    main()
