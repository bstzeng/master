"""Shared renderer for the complete chapters 04–12."""

from __future__ import annotations

import html


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def render_visual(visual: dict) -> str:
    items = []
    for item in visual["items"]:
        tone = f' {esc(item.get("tone", ""))}' if item.get("tone") else ""
        items.append(
            f'<article class="{tone.strip()}"><span>{esc(item["label"])}</span>'
            f'<b>{esc(item["title"])}</b><p>{esc(item["text"])}</p></article>'
        )
    mode = esc(visual.get("mode", "grid"))
    return (
        f'<div class="teaching-visual visual-{mode}" role="img" aria-label="{esc(visual["aria"])}">'
        f'{"".join(items)}</div><p class="diagram-caption"><b>{esc(visual["caption_title"])}</b> '
        f'{esc(visual["caption"])}</p>'
    )


def body(chapter: dict, source_cards: str) -> str:
    number = chapter["number"]
    parts = []
    toc = []
    for index, section in enumerate(chapter["sections"], start=1):
        toc.append(f'<li><a href="#part-{index}"><span>{index:02d}</span>{esc(section["toc"])}</a></li>')
        callout = ""
        if section.get("callout"):
            callout = (
                f'<aside class="chapter-callout"><b>{esc(section["callout"]["title"])}</b>'
                f'<p>{esc(section["callout"]["text"])}</p></aside>'
            )
        parts.append(
            f'<section class="lesson-part" id="part-{index}">'
            f'<div class="part-label"><span>{index:02d}</span><p>{esc(section["label"])}</p></div>'
            f'<h2>{esc(section["title"])}</h2>'
            f'<p>{esc(section["paragraphs"][0])}</p><p>{esc(section["paragraphs"][1])}</p>'
            f'{render_visual(section["visual"])}{callout}</section>'
        )

    assignment_steps = "".join(
        f'<li><span>{esc(step[0])}</span><p><b>{esc(step[1])}</b>{esc(step[2])}</p></li>'
        for step in chapter["assignment"]["steps"]
    )
    questions = "".join(
        f'<details><summary>{esc(question["q"])}</summary><p>{esc(question["a"])}</p></details>'
        for question in chapter["questions"]
    )
    recap = "".join(
        f'<article><span>{index:02d}</span><p>{esc(text)}</p></article>'
        for index, text in enumerate(chapter["recap"], start=1)
    )
    next_link = (
        f'<a class="next" href="{esc(chapter["next"]["href"])}"><small>NEXT CHAPTER →</small>'
        f'<b>{esc(chapter["next"]["title"])}</b><i>繼續閱讀</i></a>'
        if chapter.get("next")
        else '<a class="next" href="index.html"><small>COURSE COMPLETE →</small><b>回到完整課程大綱</b><i>複習 12 章</i></a>'
    )

    return f'''
      <article class="chapter-page">
        <header class="chapter-hero"><div class="chapter-hero-copy"><a class="breadcrumb" href="index.html">COURSE OUTLINE / CHAPTER {number:02d}</a><p class="eyebrow">{esc(chapter["english"])}</p><h1>{esc(chapter["title"])}</h1><p class="chapter-deck">{esc(chapter["deck"])}</p><div class="chapter-meta"><span>{esc(chapter["duration"])}</span><span>8 個完整段落</span><span>{esc(chapter["meta"])}</span><span>授權環境限定</span></div></div><figure class="chapter-cover"><button class="zoom-image" type="button" data-image="assets/{esc(chapter["image"])}" data-alt="{esc(chapter["image_alt"])}"><img src="assets/{esc(chapter["image"])}" alt="{esc(chapter["image_alt"])}" /><span>點擊放大 ↗</span></button><figcaption>GPT 原創概念圖：{esc(chapter["image_caption"])}</figcaption></figure></header>

        <section class="chapter-opening"><div><p class="section-index">LEARNING OUTCOME</p><p>{esc(chapter["learning"])}</p></div><div><p class="section-index">SAFE PRACTICE BOUNDARY</p><p>{esc(chapter["boundary"])}</p></div></section>

        <div class="chapter-layout">
          <aside class="chapter-toc"><p>本章內容</p><ol>{''.join(toc)}</ol><a href="#assignment">前往本章作業 ↓</a></aside>
          <div class="chapter-content">{''.join(parts)}</div>
        </div>

        <section class="assignment" id="assignment"><div><p class="section-index">FIELD ASSIGNMENT</p><h2>{esc(chapter["assignment"]["title"])}</h2><p>{esc(chapter["assignment"]["intro"])}</p></div><ol>{assignment_steps}</ol></section>

        <section class="self-check"><div><p class="section-index">CHECK YOUR MODEL</p><h2>先回答，再展開。</h2></div><div>{questions}</div></section>

        <section class="chapter-recap"><p class="section-index">CHAPTER {number:02d} / RECAP</p><h2>{esc(chapter["recap_title"])}</h2><div>{recap}</div></section>

        <section class="sources"><div><p class="section-index">PRIMARY REFERENCES</p><h2>本章依據</h2><p>{esc(chapter["source_intro"])}</p></div><ul>{source_cards}</ul></section>

        <nav class="chapter-nav"><a href="{esc(chapter["previous"]["href"])}"><span>← PREVIOUS CHAPTER</span><b>{esc(chapter["previous"]["title"])}</b></a>{next_link}</nav>
      </article>'''
