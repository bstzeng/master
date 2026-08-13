#!/usr/bin/env python3
"""Check Korean HTML pages for broken local links and required structure."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


SITE_ROOT = Path(__file__).resolve().parent.parent
KOREAN_ROOT = Path(__file__).resolve().parent


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
    pages = [SITE_ROOT / "index.html", *sorted(KOREAN_ROOT.rglob("*.html"))]
    lesson_pages = list((KOREAN_ROOT / "lessons").rglob("*.html"))
    audio_files = list((KOREAN_ROOT / "audio").glob("*.mp3"))
    if len(lesson_pages) != 143:
        errors.append(f"expected 143 lesson pages, found {len(lesson_pages)}")
    unit_pages = list((KOREAN_ROOT / "units").glob("*.html"))
    if len(unit_pages) != 26:
        errors.append(f"expected 26 unit pages, found {len(unit_pages)}")
    manifest_path = KOREAN_ROOT / "audio" / "manifest.json"
    if not manifest_path.exists():
        errors.append("missing audio manifest")
        expected_audio_count = 0
    else:
        import json
        expected_audio_count = json.loads(manifest_path.read_text(encoding="utf-8"))["count"]
    if len(audio_files) != expected_audio_count:
        errors.append(f"expected {expected_audio_count} bundled audio files, found {len(audio_files)}")
    for audio_file in audio_files:
        if audio_file.stat().st_size <= 1_000:
            errors.append(f"{audio_file.relative_to(SITE_ROOT)}: audio file is empty")

    for path in pages:
        parser = PageParser()
        parser.feed(path.read_text(encoding="utf-8"))
        if parser.h1_count != 1:
            errors.append(f"{path.relative_to(SITE_ROOT)}: expected one h1, found {parser.h1_count}")
        if parser.title_count != 1:
            errors.append(f"{path.relative_to(SITE_ROOT)}: expected one title, found {parser.title_count}")
        if KOREAN_ROOT / "lessons" in path.parents and parser.speech_buttons < 4:
            errors.append(f"{path.relative_to(SITE_ROOT)}: expected at least four speech controls")
        if KOREAN_ROOT / "lessons" in path.parents and len(parser.audio_sources) != parser.speech_buttons:
            errors.append(f"{path.relative_to(SITE_ROOT)}: every speech control needs bundled audio")
        if KOREAN_ROOT / "lessons" in path.parents and parser.romanization_count * 2 != parser.speech_buttons:
            errors.append(f"{path.relative_to(SITE_ROOT)}: every normal/slow audio pair needs one RR label")
        if path == KOREAN_ROOT / "alphabet.html" and parser.speech_buttons != 40:
            errors.append(f"{path.relative_to(SITE_ROOT)}: expected 21 vowel and 19 consonant controls")
        for raw_source in parser.audio_sources:
            target = (path.parent / unquote(raw_source)).resolve()
            if not target.exists():
                errors.append(f"{path.relative_to(SITE_ROOT)}: missing bundled audio {raw_source}")
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
        print("\n".join(f"ERROR: {error}" for error in errors))
        raise SystemExit(1)
    print(f"Checked {len(pages)} pages, including 143 lessons, with no broken local links.")


if __name__ == "__main__":
    main()
