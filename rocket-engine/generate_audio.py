#!/usr/bin/env python3
"""Generate the rocket-engine narration MP3s and the narration.js manifest."""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "narration.json"
AUDIO = ROOT / "audio"
MANIFEST = ROOT / "narration.js"
MARGIN = 0.15  # 旁白至少要比字幕時段短這麼多秒


def speak_text(sub: dict) -> str | None:
    return sub.get("speak", sub["text"])


def clip_name(scene: int, line: int) -> str:
    return f"s{scene + 1}-{line + 1}.mp3"


def mp3_duration(path: Path) -> float:
    from mutagen.mp3 import MP3

    return float(MP3(path).info.length)


async def create_audio(text: str, target: Path, voice: str, rate: str) -> None:
    import edge_tts

    temporary = target.with_suffix(".part")
    for attempt in range(1, 4):
        try:
            await edge_tts.Communicate(text=text, voice=voice, rate=rate).save(str(temporary))
            if temporary.exists() and temporary.stat().st_size > 1_000:
                temporary.replace(target)
                return
        except Exception:
            if attempt == 3:
                raise
        await asyncio.sleep(attempt)
    raise RuntimeError(f"Generated audio was empty: {text}")


def write_manifest(data: dict, with_audio: bool) -> list[str]:
    problems = []
    scenes = []
    for si, scene in enumerate(data["scenes"]):
        subs = []
        for li, sub in enumerate(scene["subs"]):
            entry = {"start": sub["start"], "end": sub["end"], "text": sub["text"], "audio": None, "duration": 0}
            if sub["end"] > scene["dur"] or sub["start"] >= sub["end"]:
                problems.append(f"{clip_name(si, li)}：字幕時段 {sub['start']}–{sub['end']} 不在場景長度 {scene['dur']} 秒內")
            path = AUDIO / clip_name(si, li)
            if with_audio and speak_text(sub) and path.exists():
                duration = round(mp3_duration(path), 3)
                window = sub["end"] - sub["start"]
                if duration > window - MARGIN:
                    problems.append(f"{path.name}：旁白 {duration:.2f} 秒，超過字幕時段 {window:.2f} 秒，請縮短 speak 文字")
                entry["audio"] = f"audio/{path.name}"
                entry["duration"] = duration
            subs.append(entry)
        scenes.append({"title": scene["title"], "dur": scene["dur"], "subs": subs})
    manifest = {"voice": data["voice"], "scenes": scenes}
    MANIFEST.write_text(
        "// 由 generate_audio.py 產生，請改 data/narration.json 後重新執行\n"
        f"window.ROCKET_NARRATION = {json.dumps(manifest, ensure_ascii=False, indent=2)};\n",
        encoding="utf-8",
    )
    return problems


async def generate(data: dict, force: bool) -> None:
    AUDIO.mkdir(exist_ok=True)
    for si, scene in enumerate(data["scenes"]):
        for li, sub in enumerate(scene["subs"]):
            text = speak_text(sub)
            if not text:
                continue
            target = AUDIO / clip_name(si, li)
            if force or not target.exists():
                await create_audio(text, target, data["voice"], data.get("rate", "+0%"))
                print(f"generated {target.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest-only", action="store_true", help="只重建 narration.js（不呼叫 TTS），沒有音檔的句子會只顯示字幕")
    parser.add_argument("--force", action="store_true", help="重新產生所有 MP3")
    args = parser.parse_args()

    data = json.loads(DATA.read_text(encoding="utf-8"))
    if not args.manifest_only:
        asyncio.run(generate(data, args.force))
    problems = write_manifest(data, with_audio=AUDIO.exists())
    print(f"wrote {MANIFEST.relative_to(ROOT)}")
    if problems:
        raise SystemExit("\n".join(problems))


if __name__ == "__main__":
    main()
