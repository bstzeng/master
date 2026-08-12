#!/usr/bin/env python3
"""Check generated HTML for broken local links and basic page structure."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent.parent


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.ids: set[str] = set()
        self.h1_count = 0
        self.title_count = 0

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


def main() -> None:
    errors: list[str] = []
    html_files = sorted(ROOT.rglob("*.html"))
    generated = [path for path in html_files if path == ROOT / "index.html" or ROOT / "python" in path.parents]
    for path in generated:
        parser = PageParser()
        parser.feed(path.read_text(encoding="utf-8"))
        if parser.h1_count != 1:
            errors.append(f"{path.relative_to(ROOT)}: expected one h1, found {parser.h1_count}")
        if parser.title_count != 1:
            errors.append(f"{path.relative_to(ROOT)}: expected one title, found {parser.title_count}")
        for raw_link in parser.links:
            parsed = urlsplit(raw_link)
            if parsed.scheme or raw_link.startswith("//"):
                continue
            target_path = unquote(parsed.path)
            if not target_path:
                if parsed.fragment and parsed.fragment not in parser.ids:
                    errors.append(f"{path.relative_to(ROOT)}: missing fragment #{parsed.fragment}")
                continue
            target = (path.parent / target_path).resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{path.relative_to(ROOT)}: link escapes site root: {raw_link}")
                continue
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                errors.append(f"{path.relative_to(ROOT)}: missing target {raw_link}")
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        raise SystemExit(1)
    print(f"Checked {len(generated)} HTML pages with no broken local links.")


if __name__ == "__main__":
    main()
