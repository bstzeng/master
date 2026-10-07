#!/usr/bin/env python3
"""Combine PNG frames into a looping GIF with one shared palette (no flicker)."""

import sys
from pathlib import Path

from PIL import Image


def main() -> None:
    frame_dir, target, fps = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
    frames = [Image.open(p).convert("RGB") for p in sorted(frame_dir.glob("*.png"))]
    # 從多張影格取樣建立共用調色盤，避免每格顏色跳動
    step = max(1, len(frames) // 8)
    samples = frames[::step]
    sheet = Image.new("RGB", (frames[0].width, frames[0].height * len(samples)))
    for i, im in enumerate(samples):
        sheet.paste(im, (0, i * frames[0].height))
    palette = sheet.quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    out = [im.quantize(palette=palette, dither=Image.Dither.NONE) for im in frames]
    out[0].save(target, save_all=True, append_images=out[1:], duration=round(1000 / fps), loop=0, optimize=True, disposal=1)
    print(f"{target.name}: {len(out)} frames, {target.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
