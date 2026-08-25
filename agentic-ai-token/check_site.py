#!/usr/bin/env python3
"""Validate generated course pages, structure, assets, and local links."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent


class Inspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs, self.srcs = [], []
        self.h1 = self.cards = self.parts = self.visuals = self.details = self.workshops = 0
        self.meta_names, self.meta_properties = set(), set()
        self.missing_alt = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        classes = set(values.get("class", "").split())
        if tag == "a" and values.get("href"):
            self.hrefs.append(values["href"])
        if tag in {"img", "script"} and values.get("src"):
            self.srcs.append(values["src"])
        if tag == "link" and values.get("href"):
            self.hrefs.append(values["href"])
        if tag == "h1": self.h1 += 1
        if "chapter-card" in classes: self.cards += 1
        if "lesson-part" in classes: self.parts += 1
        if "teaching-visual" in classes: self.visuals += 1
        if "optimization-workshop" in classes: self.workshops += 1
        if tag == "details": self.details += 1
        if tag == "meta":
            if values.get("name"): self.meta_names.add(values["name"])
            if values.get("property"): self.meta_properties.add(values["property"])
        if tag == "img" and not values.get("alt"):
            self.missing_alt.append(values.get("src", "unknown"))


def check_local(reference, page):
    parsed = urlparse(reference)
    if parsed.scheme or reference.startswith(("#", "mailto:", "tel:")):
        return
    if parsed.path:
        target = (page.parent / parsed.path).resolve()
        assert target.exists(), f"broken local reference in {page.name}: {reference}"


def main():
    pages = sorted(ROOT.glob("*.html"))
    assert len(pages) == 13, f"expected 13 pages, found {len(pages)}"
    for page in pages:
        inspector = Inspector()
        inspector.feed(page.read_text(encoding="utf-8"))
        assert inspector.h1 == 1, f"{page.name}: expected one h1"
        assert not inspector.missing_alt, f"{page.name}: images missing alt"
        assert "description" in inspector.meta_names
        assert "twitter:card" in inspector.meta_names
        assert {"og:title", "og:description", "og:image"} <= inspector.meta_properties
        for reference in inspector.hrefs + inspector.srcs:
            check_local(reference, page)
        if page.name == "index.html":
            assert inspector.cards == 12
        else:
            assert inspector.parts == 8, f"{page.name}: expected 8 sections"
            assert inspector.visuals == 8, f"{page.name}: expected 8 visuals"
            assert inspector.details == 5, f"{page.name}: expected 5 checks"
            assert inspector.workshops == 1, f"{page.name}: expected one workshop"
    assert len(list((ROOT / "assets").glob("*.png"))) == 5
    assert len(list((ROOT / "templates").iterdir())) == 4
    print("Checked 13 pages: 12 chapters × 8 sections, 8 visuals, 5 checks, plus all assets and links.")


if __name__ == "__main__":
    main()
