#!/usr/bin/env python3
"""Validate content density and structure of generated futures pages."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def visible_text(source: str) -> str:
    source = re.sub(r"<script[\s\S]*?</script>", "", source, flags=re.I)
    source = re.sub(r"<style[\s\S]*?</style>", "", source, flags=re.I)
    source = re.sub(r"<[^>]+>", "", source)
    return re.sub(r"\s+", "", source)


def main():
    files = sorted(ROOT.glob("chapter-*.html"))
    assert len(files) == 12, f"expected 12 chapters, got {len(files)}"
    assert (ROOT / "index.html").exists()
    for path in files:
        source = path.read_text(encoding="utf-8")
        assert source.count('class="lesson-part"') == 8, f"{path.name}: section count"
        assert source.count("<details>") == 5, f"{path.name}: question count"
        assert source.count('class="teaching-visual visual-flow"') == 8, f"{path.name}: visual count"
        assert source.count("OFFICIAL REFERENCES") == 1, f"{path.name}: sources"
        assert "損失可能超過初始保證金" in source, f"{path.name}: risk warning"
        count = len(visible_text(source))
        assert count >= 5000, f"{path.name}: only {count} visible chars"
        print(f"OK {path.name}: {count} visible chars")
    print("Validated outline + 12 dense chapters.")


if __name__ == "__main__":
    main()
