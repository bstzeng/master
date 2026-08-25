#!/usr/bin/env python3
"""Build the complete Token-Efficient Agentic AI course."""

from __future__ import annotations

import html
from pathlib import Path

from data.chapters_01_04 import CHAPTERS_01_04
from data.chapters_05_08 import CHAPTERS_05_08
from data.chapters_09_12 import CHAPTERS_09_12
from data.course import CHAPTERS, PHASES

ROOT = Path(__file__).resolve().parent
LESSONS = CHAPTERS_01_04 + CHAPTERS_05_08 + CHAPTERS_09_12
META_BY_NUMBER = {chapter["number"]: chapter for chapter in CHAPTERS}


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def shell(*, title, description, body, active="outline", image="assets/phase-1-cost-map.png"):
    image_url = f"https://bstzeng.github.io/master/agentic-ai-token/{image}"
    active_number = int(active.split("-")[1]) if active.startswith("chapter-") else 0

    def nav(first, last, href, label):
        state = "is-active" if first <= active_number <= last else ""
        return f'<a class="{state}" href="{href}">{label}</a>'

    return f'''<!doctype html>
<html lang="zh-Hant">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="{esc(description)}" />
    <meta name="theme-color" content="#11142d" />
    <meta property="og:title" content="{esc(title)}｜Agentic AI Token 節省實戰" />
    <meta property="og:description" content="{esc(description)}" />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="{image_url}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{esc(title)}｜Agentic AI Token 節省實戰" />
    <meta name="twitter:description" content="{esc(description)}" />
    <meta name="twitter:image" content="{image_url}" />
    <title>{esc(title)}｜MASTER</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Noto+Sans+TC:wght@400;500;600;700&family=Noto+Serif+TC:wght@700;900&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="styles.css" />
    <script src="script.js" defer></script>
  </head>
  <body>
    <div class="reading-progress" aria-hidden="true"><span></span></div>
    <header class="site-header">
      <a class="brand" href="../index.html" aria-label="回到 MASTER 首頁"><span class="brand-mark">M</span><span>MASTER</span></a>
      <nav aria-label="Agentic AI Token 課程選單">
        <a class="{'is-active' if active == 'outline' else ''}" href="index.html">完整大綱</a>
        {nav(1, 2, 'chapter-01-token-cost-map.html', '01–02')}
        {nav(3, 5, 'chapter-03-lean-prompts.html', '03–05')}
        {nav(6, 8, 'chapter-06-tool-surface.html', '06–08')}
        {nav(9, 11, 'chapter-09-model-routing.html', '09–11')}
        {nav(12, 12, 'chapter-12-production-playbook.html', '12')}
      </nav>
      <span class="header-note">AGENTIC AI / TOKEN EFFICIENCY</span>
    </header>
    <main>{body}</main>
    <footer><span>MASTER / TOPIC 07</span><p>Spend tokens where they change the outcome.</p><span>© <b id="current-year"></b> PATRICK</span></footer>
    <dialog class="image-dialog" aria-label="放大圖片"><button type="button" aria-label="關閉圖片">×</button><img src="" alt="放大圖片預覽" /></dialog>
  </body>
</html>'''


def render_visual(visual):
    items = []
    for item in visual["items"]:
        tone = esc(item.get("tone", ""))
        items.append(f'<article class="{tone}"><span>{esc(item["label"])}</span><b>{esc(item["title"])}</b><p>{esc(item["text"])}</p></article>')
    return f'<div class="teaching-visual visual-{esc(visual["mode"])}" role="img" aria-label="{esc(visual["aria"])}">{"".join(items)}</div><p class="diagram-caption"><b>{esc(visual["caption_title"])}</b> {esc(visual["caption"])}</p>'


def render_source_cards(sources):
    return "".join(f'<li><a href="{esc(source["url"])}" target="_blank" rel="noreferrer"><b>{esc(source["title"])}</b><span>{esc(source["note"])}</span></a></li>' for source in sources)


def chapter_card(chapter):
    tags = "".join(f'<li>{esc(topic)}</li>' for topic in chapter["topics"])
    return f'''<article class="chapter-card is-ready"><div class="chapter-card-head"><span>CHAPTER {chapter['number']:02d}</span><b>COMPLETE</b></div><p>{esc(chapter['english'])}</p><h3>{esc(chapter['title'])}</h3><div class="chapter-summary">{esc(chapter['summary'])}</div><ul>{tags}</ul><div class="chapter-foot"><span>{esc(chapter['duration'])}</span><a class="card-action" href="{esc(chapter['href'])}">閱讀完整第 {chapter['number']} 章 <span>→</span></a></div></article>'''


def build_outline():
    phases = []
    phase_nav = []
    for phase in PHASES:
        phase_nav.append(f'<a href="#phase-{phase["number"]}"><span>{phase["number"]:02d}</span>{esc(phase["title"])}</a>')
        cards = "".join(chapter_card(chapter) for chapter in CHAPTERS if chapter["phase"] == phase["number"])
        phases.append(f'''<section class="phase" id="phase-{phase['number']}"><div class="phase-head"><div><p class="section-index">PHASE {phase['number']:02d} / {esc(phase['english'])}</p><h2>{esc(phase['title'])}</h2></div><p>{esc(phase['summary'])}</p></div><div class="chapter-grid">{cards}</div></section>''')

    body = f'''
      <section class="outline-hero">
        <div class="outline-copy"><a class="breadcrumb" href="../index.html">MASTER / TOPIC 07</a><p class="eyebrow">TOKEN-EFFICIENT AGENTIC AI · COMPLETE COURSE</p><h1>不是一味少說，<br /><em>而是少做無效工作。</em></h1><p class="hero-intro">從 Token 成本地圖、Prompt 與 Context，到工具輸出、Loop Guard、模型路由、多 Agent、快取與正式環境治理。全課程 12 個大型章節，每章都有圖解、前後案例、模板、作業與品質驗證。</p><div class="course-stats"><div><strong>12 / 12</strong><span>完整大型章節</span></div><div><strong>18+</strong><span>可直接套用模板</span></div><div><strong>5</strong><span>原創階段主視覺</span></div></div><a class="primary-button" href="chapter-01-token-cost-map.html">從成本地圖開始 <span>→</span></a></div>
        <figure class="hero-image"><button class="zoom-image" type="button" data-image="assets/phase-1-cost-map.png" data-alt="大量資料經 Agent 工作流過濾成精準結果的課程主視覺"><img src="assets/phase-1-cost-map.png" alt="大量資料經 Agent 工作流過濾成精準結果的課程主視覺" /><span>點擊放大 ↗</span></button><figcaption>GPT 原創主視覺｜所有精確術語以網頁大字圖解呈現</figcaption></figure>
      </section>
      <section class="course-contract"><p class="section-index">00 / COURSE PRINCIPLE</p><div><h2>衡量每個成功任務，<br />不是追求最少字數。</h2><p>Token 只有和品質、延遲、重試、工具費用與人工修正一起看才有意義。任何縮減都先通過必要證據與安全邊界，再比較總成本。</p></div><ol><li><span>01</span><b>先量測</b><p>建立固定任務與成本地圖，拒絕只憑感覺優化。</p></li><li><span>02</span><b>再縮減</b><p>優先移除重送、無關與可在工具端處理的內容。</p></li><li><span>03</span><b>最後營運</b><p>用預算、Evals、告警與回復持續控制正式環境。</p></li></ol></section>
      <nav class="phase-nav" aria-label="快速前往課程階段">{''.join(phase_nav)}</nav>
      <div class="full-outline">{''.join(phases)}</div>
      <section class="token-lab" id="token-lab"><div><p class="section-index">QUICK LAB / TOKEN MULTIPLIER</p><h2>先感受『重送』的乘數。</h2><p>這不是平台報價計算器，而是一個結構估算：同一份背景、工具結果與多 Agent 複製，如何在完整 Run 裡放大。</p></div><form class="token-calculator"><label>每回合背景 Token<input id="base-tokens" type="number" min="0" value="8000" /></label><label>每回合工具結果 Token<input id="tool-tokens" type="number" min="0" value="3000" /></label><label>模型呼叫回合<input id="call-count" type="number" min="1" value="6" /></label><label>平行 Agent 數<input id="agent-count" type="number" min="1" value="1" /></label><label>最終輸出 Token<input id="output-tokens" type="number" min="0" value="900" /></label><output><span>粗估工作量</span><strong id="token-estimate">—</strong><small>Token-equivalent context volume</small></output></form></section>
      <section class="resource-library"><div><p class="section-index">READY-TO-USE / TOOLKIT</p><h2>課程隨附工具包</h2><p>下載後直接替換成自己的任務與數字。</p></div><div class="resource-grid"><a href="templates/token-scorecard.csv"><span>CSV</span><b>Token Scorecard</b><p>每回合Usage、工具、重試、成功與成本欄位。</p></a><a href="templates/prompt-review.md"><span>MD</span><b>Prompt Review</b><p>任務契約、去重、輸出預算與Ablation清單。</p></a><a href="templates/agent-handoff.md"><span>MD</span><b>Agent Handoff</b><p>Checkpoint與子 Agent固定交接格式。</p></a><a href="templates/production-playbook.md"><span>MD</span><b>Production Playbook</b><p>Budget、SLO、降級、告警與30天計畫。</p></a></div></section>
      <section class="density-promise"><div><p class="section-index">READING GUIDE</p><h2>每一章怎麼讀</h2></div><div class="density-list"><p>先讀核心模型，再跑頁尾作業。所有大字流程圖由 HTML/CSS 繪製，手機也能閱讀；主視覺只負責建立直覺，不把小字塞進圖片。</p><ul><li>8 個深度段落／章</li><li>8 張大字流程圖／章</li><li>1 組浪費／優化案例</li><li>4 步實作作業</li><li>5 題自我檢查</li><li>官方文件延伸閱讀</li></ul><a href="chapter-01-token-cost-map.html">開始第一章 →</a></div></section>'''
    (ROOT / "index.html").write_text(shell(title="完整大綱", description="12章完整Agentic AI省Token課程：從成本量測、Prompt與Context，到工具、多Agent、快取與正式環境治理。", body=body), encoding="utf-8")


def build_chapter(lesson):
    meta = META_BY_NUMBER[lesson["number"]]
    number = meta["number"]
    toc, parts = [], []
    for index, section in enumerate(lesson["sections"], start=1):
        toc.append(f'<li><a href="#part-{index}"><span>{index:02d}</span>{esc(section["toc"])}</a></li>')
        callout = ""
        if section.get("callout"):
            callout = f'<aside class="chapter-callout"><b>{esc(section["callout"]["title"])}</b><p>{esc(section["callout"]["text"])}</p></aside>'
        code = f'<pre class="lesson-code"><code>{esc(section["code"])}</code></pre>' if section.get("code") else ""
        parts.append(f'<section class="lesson-part" id="part-{index}"><div class="part-label"><span>{index:02d}</span><p>{esc(section["label"])}</p></div><h2>{esc(section["title"])}</h2><p>{esc(section["paragraphs"][0])}</p><p>{esc(section["paragraphs"][1])}</p>{code}{render_visual(section["visual"])}{callout}</section>')

    assignment = "".join(f'<li><span>{esc(step[0])}</span><p><b>{esc(step[1])}</b>{esc(step[2])}</p></li>' for step in lesson["assignment"]["steps"])
    questions = "".join(f'<details><summary>{esc(item["q"])}</summary><p>{esc(item["a"])}</p></details>' for item in lesson["questions"])
    recap = "".join(f'<article><span>{i:02d}</span><p>{esc(text)}</p></article>' for i, text in enumerate(lesson["recap"], start=1))
    previous = CHAPTERS[number - 2] if number > 1 else None
    next_chapter = CHAPTERS[number] if number < len(CHAPTERS) else None
    previous_link = f'<a href="{esc(previous["href"])}"><span>← PREVIOUS CHAPTER</span><b>{esc(previous["title"])}</b></a>' if previous else '<a href="index.html"><span>← COURSE OUTLINE</span><b>回到12章完整大綱</b></a>'
    next_link = f'<a class="next" href="{esc(next_chapter["href"])}"><small>NEXT CHAPTER →</small><b>{esc(next_chapter["title"])}</b><i>繼續閱讀</i></a>' if next_chapter else '<a class="next" href="index.html"><small>COURSE COMPLETE →</small><b>回到完整大綱</b><i>開始30天計畫</i></a>'
    workshop = lesson["workshop"]

    body = f'''
      <article class="chapter-page">
        <header class="chapter-hero"><div class="chapter-hero-copy"><a class="breadcrumb" href="index.html">COURSE OUTLINE / CHAPTER {number:02d}</a><p class="eyebrow">{esc(meta['english'])}</p><h1>{esc(meta['title'])}</h1><p class="chapter-deck">{esc(lesson['deck'])}</p><div class="chapter-meta"><span>{esc(meta['duration'])}</span><span>8 個完整段落</span><span>實例＋模板＋作業</span><span>品質優先</span></div></div><figure class="chapter-cover"><button class="zoom-image" type="button" data-image="assets/{esc(lesson['image'])}" data-alt="{esc(lesson['image_alt'])}"><img src="assets/{esc(lesson['image'])}" alt="{esc(lesson['image_alt'])}" /><span>點擊放大 ↗</span></button><figcaption>GPT 原創概念圖｜{esc(lesson['image_caption'])}</figcaption></figure></header>
        <section class="chapter-opening"><div><p class="section-index">LEARNING OUTCOME</p><p>{esc(lesson['learning'])}</p></div><div><p class="section-index">IMPORTANT BOUNDARY</p><p>{esc(lesson['boundary'])}</p></div></section>
        <div class="chapter-layout"><aside class="chapter-toc"><p>本章內容</p><ol>{''.join(toc)}</ol><a href="#workshop">前往前後對照 ↓</a></aside><div class="chapter-content">{''.join(parts)}</div></div>
        <section class="optimization-workshop" id="workshop"><div><p class="section-index">BEFORE / AFTER</p><h2>{esc(workshop['title'])}</h2></div><div class="workshop-grid"><article class="waste"><span>WASTEFUL</span><p>{esc(workshop['before'])}</p></article><article class="optimized"><span>OPTIMIZED</span><p>{esc(workshop['after'])}</p></article><article class="result"><span>WHY IT WORKS</span><p>{esc(workshop['result'])}</p></article></div></section>
        <section class="assignment" id="assignment"><div><p class="section-index">FIELD ASSIGNMENT</p><h2>{esc(lesson['assignment']['title'])}</h2><p>{esc(lesson['assignment']['intro'])}</p></div><ol>{assignment}</ol></section>
        <section class="self-check"><div><p class="section-index">CHECK YOUR MODEL</p><h2>先回答，再展開。</h2></div><div>{questions}</div></section>
        <section class="chapter-recap"><p class="section-index">CHAPTER {number:02d} / RECAP</p><h2>{esc(lesson['recap_title'])}</h2><div>{recap}</div></section>
        <section class="sources"><div><p class="section-index">OFFICIAL REFERENCES</p><h2>本章延伸閱讀</h2><p>課程使用平台無關的工程原則，API名稱與現行功能以OpenAI官方文件作案例；部署前仍應依你使用的平台重新驗證。</p></div><ul>{render_source_cards(lesson['sources'])}</ul></section>
        <nav class="chapter-nav">{previous_link}{next_link}</nav>
      </article>'''
    (ROOT / meta["href"]).write_text(shell(title=f'{number:02d}｜{meta["title"]}', description=meta["summary"], body=body, active=f"chapter-{number}", image=f'assets/{lesson["image"]}'), encoding="utf-8")


def main():
    build_outline()
    for lesson in LESSONS:
        build_chapter(lesson)
    print("Built complete Agentic AI Token course: outline + 12 chapters.")


if __name__ == "__main__":
    main()
