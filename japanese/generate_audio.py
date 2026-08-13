#!/usr/bin/env python3
"""Generate bundled Japanese MP3 assets for the static course."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
from pathlib import Path

import edge_tts


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "curriculum.json"
KANA_DATA = ROOT / "data" / "kana.json"
DEFAULT_OUTPUT = ROOT / "audio"
DEFAULT_VOICE = "ja-JP-NanamiNeural"


def audio_filename(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16] + ".mp3"


def collect_phrases() -> list[str]:
    phrases = {"こんにちは"}
    for path in sorted((ROOT / "data").glob("phase-[1-5].json")):
        for unit in json.loads(path.read_text(encoding="utf-8")):
            for lesson in unit["lessons"]:
                for section in lesson["sections"]:
                    for item in section["audio"]:
                        phrases.add(str(item.get("speak", item["text"])).strip())
    kana = json.loads(KANA_DATA.read_text(encoding="utf-8"))
    for group in kana["hiragana_groups"] + kana["katakana_groups"]:
        for item in group["items"]:
            phrases.add(str(item.get("speak", item["reading"])).strip())
    return sorted(item for item in phrases if item)


async def create_audio(text: str, target: Path, voice: str, semaphore: asyncio.Semaphore) -> None:
    if target.exists() and target.stat().st_size > 1_000:
        return
    temporary = target.with_suffix(".part")
    async with semaphore:
        for attempt in range(1, 4):
            try:
                await edge_tts.Communicate(text=text, voice=voice).save(str(temporary))
                if temporary.exists() and temporary.stat().st_size > 1_000:
                    temporary.replace(target)
                    return
            except Exception:
                if attempt == 3:
                    raise
            await asyncio.sleep(attempt)
    raise RuntimeError(f"Generated audio was empty: {text}")


async def generate(output: Path, voice: str, concurrency: int) -> None:
    phrases = collect_phrases()
    output.mkdir(parents=True, exist_ok=True)
    semaphore = asyncio.Semaphore(concurrency)
    tasks = [create_audio(text, output / audio_filename(text), voice, semaphore) for text in phrases]
    completed = 0
    for task in asyncio.as_completed(tasks):
        await task
        completed += 1
        if completed % 20 == 0 or completed == len(tasks):
            print(f"Generated or verified {completed}/{len(tasks)} audio files.")
    manifest = {"voice": voice, "format": "mp3", "count": len(phrases), "files": {text: audio_filename(text) for text in phrases}}
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--voice", default=DEFAULT_VOICE)
    parser.add_argument("--concurrency", type=int, default=6)
    args = parser.parse_args()
    asyncio.run(generate(args.output, args.voice, max(1, args.concurrency)))


if __name__ == "__main__":
    main()
