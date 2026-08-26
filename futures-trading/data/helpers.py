"""Helpers used by the futures course data modules."""


def source(title, url, note):
    return {"title": title, "url": url, "note": note}


def section(toc, title, concept, application, decision, trap, items, *, formula=None, callout=None):
    """Create one dense lesson section with two explanatory paragraphs and a diagram."""
    return {
        "toc": toc,
        "title": title,
        "paragraphs": [
            f"{concept} {application}",
            f"實際決策時，{decision}。{trap}",
        ],
        "items": items,
        "formula": formula,
        "callout": callout,
    }


def item(label, title, text, tone=""):
    return {"label": label, "title": title, "text": text, "tone": tone}


def assignment(title, intro, steps):
    return {"title": title, "intro": intro, "steps": steps}

