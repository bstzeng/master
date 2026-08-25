"""Small helpers that keep the chapter data readable."""


def point(label, title, text, tone=""):
    return {"label": label, "title": title, "text": text, "tone": tone}


def section(toc, label, title, p1, p2, points, *, mode="grid", caption="", callout=None, code=None):
    return {
        "toc": toc,
        "label": label,
        "title": title,
        "paragraphs": [p1, p2],
        "visual": {
            "mode": mode,
            "aria": title,
            "caption_title": f"圖解｜{toc}",
            "caption": caption or "把每一步的輸入、判斷與輸出分開，才看得見真正可以縮減的地方。",
            "items": points,
        },
        "callout": callout,
        "code": code,
    }


def source(title, url, note):
    return {"title": title, "url": url, "note": note}
