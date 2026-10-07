#!/usr/bin/env python3
"""Combine PNG frames into a looping GIF with one shared palette (no flicker)."""

import sys
from pathlib import Path

from PIL import Image


def main() -> None:
    frame_dir, target, fps = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
    paths = sorted(frame_dir.glob("*.png"))
    # 從多張影格取樣建立共用調色盤，避免每格顏色跳動（取樣縮小一半以節省記憶體）
    step = max(1, len(paths) // 8)
    samples = [Image.open(p).convert("RGB") for p in paths[::step]]
    w, h = samples[0].width // 2, samples[0].height // 2
    sheet = Image.new("RGB", (w, h * len(samples)))
    for i, im in enumerate(samples):
        sheet.paste(im.resize((w, h)), (0, i * h))
    palette = sheet.quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    # 逐張讀取並轉成調色盤影格，1080P 也不會一次佔用大量記憶體
    out = [Image.open(p).convert("RGB").quantize(palette=palette, dither=Image.Dither.NONE) for p in paths]
    out[0].save(target, save_all=True, append_images=out[1:], duration=round(1000 / fps), loop=0, optimize=True, disposal=1)
    print(f"{target.name}: {len(out)} frames, {target.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
