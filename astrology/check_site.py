#!/usr/bin/env python3
"""Check generated astrology pages and local links."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
SITE_ROOT = ROOT.parent


class Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.ids: set[str] = set()
        self.h1 = 0
        self.title = 0
        self.details = 0
        self.sections = 0
        self.sources = 0

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
            self.h1 += 1
        if tag == "title":
            self.title += 1
        if tag == "details":
            self.details += 1
        classes = (values.get("class") or "").split()
        if "lesson-section" in classes:
            self.sections += 1
        if "sources" in classes and tag == "section":
            self.sources += 1


def main() -> None:
    errors: list[str] = []
    pages = sorted(ROOT.rglob("*.html"))
    unit_pages = sorted((ROOT / "units").glob("*.html"))
    if len(pages) != 44:
        errors.append(f"expected 44 astrology pages, found {len(pages)}")
    if len(unit_pages) != 36:
        errors.append(f"expected 36 unit pages, found {len(unit_pages)}")
    for path in pages:
        parser = Parser()
        parser.feed(path.read_text(encoding="utf-8"))
        relative = path.relative_to(SITE_ROOT)
        if parser.h1 != 1:
            errors.append(f"{relative}: expected one h1, found {parser.h1}")
        if parser.title != 1:
            errors.append(f"{relative}: expected one title, found {parser.title}")
        if path in unit_pages:
            expected_sections = 5 if 12 <= int(path.name.split("-")[1]) <= 23 else 4
            if parser.sections != expected_sections:
                errors.append(f"{relative}: expected {expected_sections} teaching sections, found {parser.sections}")
            if parser.details != 3:
                errors.append(f"{relative}: expected three quiz details, found {parser.details}")
            if parser.sources != 1:
                errors.append(f"{relative}: expected one sources section")
        for raw in parser.links:
            parsed = urlsplit(raw)
            if parsed.scheme or raw.startswith("//"):
                continue
            target_path = unquote(parsed.path)
            if not target_path:
                if parsed.fragment and parsed.fragment not in parser.ids:
                    errors.append(f"{relative}: missing fragment #{parsed.fragment}")
                continue
            target = (path.parent / target_path).resolve()
            try:
                target.relative_to(SITE_ROOT.resolve())
            except ValueError:
                errors.append(f"{relative}: link escapes site root: {raw}")
                continue
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                errors.append(f"{relative}: missing target {raw}")
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        raise SystemExit(1)
    print("Checked 44 astrology pages, including 36 complete units, with no broken local links.")


if __name__ == "__main__":
    main()
