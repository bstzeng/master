#!/usr/bin/env python3
"""Check local links and assets in the futures course."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ATTR = re.compile(r'(?:href|src)="([^"]+)"')


def main():
    pages = [ROOT / "index.html", *sorted(ROOT.glob("chapter-*.html"))]
    missing = []
    for page in pages:
        source = page.read_text(encoding="utf-8")
        for target in ATTR.findall(source):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            local = target.split("#", 1)[0].split("?", 1)[0]
            if not local:
                continue
            resolved = (page.parent / local).resolve()
            if not resolved.exists():
                missing.append((page.name, target))
    if missing:
        for page, target in missing:
            print(f"MISSING {page}: {target}")
        raise SystemExit(1)
    print(f"Checked {len(pages)} pages: all local links and assets exist.")


if __name__ == "__main__":
    main()
