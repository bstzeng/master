#!/usr/bin/env python3
"""Generate deterministic Korean MP3 assets for the static course site."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
from pathlib import Path

import edge_tts


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "curriculum.json"
DEFAULT_OUTPUT = ROOT / "audio"
DEFAULT_VOICE = "ko-KR-SunHiNeural"


def audio_filename(text: str) -> str:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    return f"{digest}.mp3"


def collect_phrases(data: dict) -> list[str]:
    phrases = {"안녕하세요"}
    for unit in data["units"]:
        for lesson in unit["lessons"]:
            for section in lesson["sections"]:
                for item in section.get("audio", []):
                    phrases.add(str(item.get("speak", item["text"])).strip())
    return sorted(phrase for phrase in phrases if phrase)


async def create_audio(text: str, target: Path, voice: str, semaphore: asyncio.Semaphore) -> None:
    if target.exists() and target.stat().st_size > 1_000:
        return
    temporary = target.with_suffix(".part")
    async with semaphore:
        for attempt in range(1, 4):
            try:
                communicate = edge_tts.Communicate(text=text, voice=voice)
                await communicate.save(str(temporary))
                if temporary.exists() and temporary.stat().st_size > 1_000:
                    temporary.replace(target)
                    return
            except Exception:
                if attempt == 3:
                    raise
            await asyncio.sleep(attempt)
    raise RuntimeError(f"Generated audio was empty: {text}")


async def generate(output: Path, voice: str, concurrency: int) -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    phrases = collect_phrases(data)
    output.mkdir(parents=True, exist_ok=True)
    semaphore = asyncio.Semaphore(concurrency)
    tasks = [create_audio(text, output / audio_filename(text), voice, semaphore) for text in phrases]
    completed = 0
    for task in asyncio.as_completed(tasks):
        await task
        completed += 1
        if completed % 20 == 0 or completed == len(tasks):
            print(f"Generated or verified {completed}/{len(tasks)} audio files.")

    manifest = {
        "voice": voice,
        "format": "mp3",
        "count": len(phrases),
        "files": {text: audio_filename(text) for text in phrases},
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--voice", default=DEFAULT_VOICE)
    parser.add_argument("--concurrency", type=int, default=4)
    args = parser.parse_args()
    asyncio.run(generate(args.output, args.voice, max(1, args.concurrency)))


if __name__ == "__main__":
    main()
