#!/usr/bin/env python3
"""Check generated web-security pages, assets, metadata, and local links."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent


class Inspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs = []
        self.srcs = []
        self.h1_count = 0
        self.chapter_cards = 0
        self.lesson_parts = 0
        self.details = 0
        self.source_links = 0
        self.teaching_visuals = 0
        self.meta_names = set()
        self.meta_properties = set()
        self.images_without_alt = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        classes = set(values.get("class", "").split())
        if tag == "a" and values.get("href"):
            self.hrefs.append(values["href"])
            if any(domain in values["href"] for domain in ("owasp.org", "nist.gov", "cisa.gov", "rfc-editor.org", "developer.mozilla.org", "docs.github.com")):
                self.source_links += 1
        if tag in {"img", "script"} and values.get("src"):
            self.srcs.append(values["src"])
        if tag == "link" and values.get("href"):
            self.hrefs.append(values["href"])
        if tag == "h1":
            self.h1_count += 1
        if "chapter-card" in classes:
            self.chapter_cards += 1
        if "lesson-part" in classes:
            self.lesson_parts += 1
        if "teaching-visual" in classes:
            self.teaching_visuals += 1
        if tag == "details":
            self.details += 1
        if tag == "meta":
            if values.get("name"):
                self.meta_names.add(values["name"])
            if values.get("property"):
                self.meta_properties.add(values["property"])
        if tag == "img" and not values.get("alt"):
            self.images_without_alt.append(values.get("src", "unknown"))


def check_local(reference: str, page: Path) -> None:
    parsed = urlparse(reference)
    if parsed.scheme or reference.startswith(("#", "mailto:", "tel:")):
        return
    clean = parsed.path
    if not clean:
        return
    target = (page.parent / clean).resolve()
    assert target.exists(), f"broken local reference in {page.name}: {reference}"


def main() -> None:
    pages = sorted(ROOT.glob("*.html"))
    chapter_names = [
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
    assert [page.name for page in pages] == sorted(chapter_names + ["index.html"])
    inspectors = {}
    for page in pages:
        inspector = Inspector()
        inspector.feed(page.read_text(encoding="utf-8"))
        inspectors[page.name] = inspector
        assert inspector.h1_count == 1, f"{page.name} must contain one h1"
        assert not inspector.images_without_alt, f"missing alt text: {inspector.images_without_alt}"
        assert "description" in inspector.meta_names
        assert "twitter:card" in inspector.meta_names
        assert {"og:title", "og:description", "og:image"} <= inspector.meta_properties
        for reference in inspector.hrefs + inspector.srcs:
            check_local(reference, page)

    outline = inspectors["index.html"]
    assert outline.chapter_cards == 12
    for chapter_name in chapter_names:
        chapter = inspectors[chapter_name]
        assert chapter.lesson_parts == 8, f"{chapter_name} must have 8 lesson parts"
        assert chapter.details == 5, f"{chapter_name} must have 5 self-check questions"
        assert chapter.source_links == 4, f"{chapter_name} must have 4 primary source links"
    for chapter_name in chapter_names[3:]:
        assert inspectors[chapter_name].teaching_visuals == 8, f"{chapter_name} must have 8 large teaching visuals"
    assert (ROOT / "assets" / "og.png").exists()
    image_names = [
        "chapter-01-attack-surface.png", "chapter-02-http-request.png", "chapter-03-information-exposure.png",
        "chapter-04-identity.png", "chapter-05-authorization.png", "chapter-06-injection.png",
        "chapter-07-browser-security.png", "chapter-08-file-security.png", "chapter-09-ssrf-api.png",
        "chapter-10-deployment-security.png", "chapter-11-availability.png", "chapter-12-incident-response.png",
    ]
    assert all((ROOT / "assets" / image_name).exists() for image_name in image_names)
    print("Checked 13 pages, 12 chapter cards, and all 12 chapters with 8 parts, 5 questions, and 4 sources each.")


if __name__ == "__main__":
    main()
