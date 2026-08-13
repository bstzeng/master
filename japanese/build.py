#!/usr/bin/env python3
"""Generate the complete Japanese beginner learning topic."""

from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path

from romanization import romanize


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "curriculum.json"
KANA_DATA = ROOT / "data" / "kana.json"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def load_data() -> dict:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    units = []
    for path in sorted((ROOT / "data").glob("phase-[1-5].json")):
        units.extend(json.loads(path.read_text(encoding="utf-8")))
    units.sort(key=lambda item: item["number"])
    data["units"] = units
    return data


def load_kana() -> dict:
    return json.loads(KANA_DATA.read_text(encoding="utf-8"))


def audio_filename(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16] + ".mp3"


def unit_filename(unit: dict) -> str:
    return f"unit-{unit['number']:02d}-{unit['slug']}.html"


def lesson_filename(lesson: dict) -> str:
    return f"{lesson['number']:02d}-{lesson['slug']}.html"


def unit_href(unit: dict, prefix: str = "") -> str:
    return f"{prefix}units/{unit_filename(unit)}"


def lesson_href(unit: dict, lesson: dict, prefix: str = "") -> str:
    return f"{prefix}lessons/unit-{unit['number']:02d}/{lesson_filename(lesson)}"


def phase_for_unit(data: dict, unit_number: int) -> int:
    return next(item["phase"] for item in data["outline_units"] if item["number"] == unit_number)


def header(prefix: str, active: str = "") -> str:
    return f"""
    <header class="site-header">
      <a class="brand" href="{prefix}../index.html" aria-label="回到 MASTER 首頁"><span class="brand-dot"></span><span>MASTER</span></a>
      <nav aria-label="日文課程選單">
        <a class="{'is-active' if active == 'course' else ''}" href="{prefix}index.html">課程首頁</a>
        <a class="{'is-active' if active == 'kana' else ''}" href="{prefix}kana.html">假名系統</a>
        <a class="{'is-active' if active == 'outline' else ''}" href="{prefix}outline.html">完整大綱</a>
      </nav>
      <span class="header-note">JAPANESE / 15 MIN A DAY</span>
    </header>"""


def footer(prefix: str) -> str:
    return f"""
    <footer><span>MASTER / JAPANESE</span><p>読んで、聞いて、話そう。</p><a href="{prefix}index.html">課程首頁 ↑</a></footer>"""


def shell(*, title: str, description: str, body: str, prefix: str, active: str = "") -> str:
    document = f"""<!doctype html>
<html lang="zh-Hant">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="{esc(description)}" />
    <meta name="theme-color" content="#612940" />
    <title>{esc(title)}｜MASTER</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Noto+Sans+JP:wght@400;500;600;700&family=Noto+Sans+TC:wght@400;500;600;700&family=Noto+Serif+JP:wght@500;700&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="{prefix}styles.css" />
    <script src="{prefix}script.js?v=complete-1" defer></script>
  </head>
  <body>{header(prefix, active)}<main>{body}</main>{footer(prefix)}<div class="speech-status" data-speech-status aria-live="polite"></div></body>
</html>"""
    return "\n".join(line.rstrip() for line in document.splitlines()) + "\n"


def phase_card(phase: dict, outline_units: list[dict], built_units: list[dict]) -> str:
    phase_units = [item for item in outline_units if item["phase"] == phase["number"]]
    built = {item["number"]: item for item in built_units}
    ready = all(item["number"] in built for item in phase_units)
    rows = []
    for item in phase_units:
        title = esc(item["title"])
        if item["number"] in built:
            title = f'<a href="{unit_href(built[item["number"]])}">{title}</a>'
        rows.append(f'<li><span>{item["number"]:02d}</span><b>{title}</b></li>')
    action = f'<a href="phase-{phase["number"]}.html">查看第 {phase["number"]} 階段 <span>→</span></a>' if ready else '<span class="coming-soon">製作中</span>'
    return f"""<article class="roadmap-card {'is-ready' if ready else ''}"><div class="roadmap-card-head"><span>PHASE {phase['number']:02d}</span><span>{esc(phase['range'])}</span></div><h3>{esc(phase['title'])}</h3><p>{esc(phase['summary'])}</p><ol>{''.join(rows)}</ol>{action}</article>"""


def build_home(data: dict) -> None:
    units = data["units"]
    lesson_count = sum(len(unit["lessons"]) for unit in units)
    cards = "".join(phase_card(phase, data["outline_units"], units) for phase in data["phases"])
    body = f"""
      <section class="course-hero japanese-hero"><div class="course-hero-copy"><a class="breadcrumb" href="../index.html">MASTER / TOPIC 03</a><p class="eyebrow">ZERO TO DAILY JAPANESE · 一日15分</p><h1>從假名開始，<em>讀懂真實日文。</em></h1><p class="hero-intro">給完全零基礎的日文學習路線。以街頭閱讀、旅行會話與關鍵字聽力為主；中文旁有 Hepburn 羅馬拼音，每個日文都能直接播放。</p><div class="course-stats"><div><strong>5</strong><span>個階段</span></div><div><strong>{len(units)}</strong><span>個單元</span></div><div><strong>{lesson_count}</strong><span>堂課</span></div></div><div class="hero-actions"><a class="primary-button" href="kana.html">先學完整假名表 <span>→</span></a><a class="text-link" href="phase-1.html">第一階段課程</a></div></div>
        <div class="kana-poster"><span class="poster-label">KANA / かな / 001</span><button class="poster-speak" type="button" lang="ja" data-speak="こんにちは" data-audio="audio/{audio_filename('こんにちは')}" data-rate="1" aria-label="播放日文：こんにちは"><span>あ</span><small>點一下，聽日文</small></button><div class="poster-words"><span>ひらがな</span><span>カタカナ</span><span>漢字</span></div><p>READ 50% · SPEAK 30% · LISTEN 20%</p></div>
      </section>
      <section class="daily-method"><p class="section-index">00 / DAILY ROUTINE</p><div><h2>每天只要<br />15 分鐘</h2><p>固定短時間，把文字、羅馬拼音與真正的日文聲音連在一起。</p></div><ol><li><span>03 MIN</span>複習昨天的聲音</li><li><span>07 MIN</span>閱讀今天的新觀念</li><li><span>03 MIN</span>播放日文、跟讀</li><li><span>02 MIN</span>測驗與情境任務</li></ol></section>
      <section class="alphabet-entry"><div><p class="section-index">01 / SYSTEMATIC KANA</p><h2>先建立完整假名地圖，<br />再逐堂練習。</h2><p>平假名與片假名都依五十音行列整理；每個字都有 Hepburn 羅馬拼音、例詞與網站內建發音。</p></div><a href="kana.html"><span lang="ja">ひらがな 46</span><span lang="ja">カタカナ 46</span><b>打開假名系統課 →</b></a></section>
      <section class="phase-overview"><div class="section-head"><div><p class="section-index">02 / ROADMAP</p><h2>五階段學習地圖</h2></div><p>從讀出假名、理解生活文字，到建立句子、完成會話與整合閱讀聽力。</p></div><div class="roadmap-grid">{cards}</div></section>
      <section class="course-method japanese-method"><div><p class="section-index">03 / LEARNING FOCUS</p><h2>看得懂，<br />也聽得到。</h2></div><div class="method-grid"><article><span>50%</span><h3>閱讀</h3><p>從假名、招牌、菜單到交通資訊，建立真實辨識力。</p></article><article><span>30%</span><h3>會話</h3><p>優先學問候、點餐、購物、問路與求助。</p></article><article><span>20%</span><h3>聽力</h3><p>先抓數字、地名與關鍵動詞，再適應自然語速。</p></article><article><span>—</span><h3>不學打字</h3><p>把時間集中在閱讀、理解、跟讀與聆聽。</p></article></div></section>"""
    (ROOT / "index.html").write_text(shell(title="零基礎日文", description="每天15分鐘，從假名到街頭閱讀、旅行會話與基礎聽力。", body=body, prefix="", active="course"), encoding="utf-8")


def build_outline(data: dict) -> None:
    built = {unit["number"]: unit for unit in data["units"]}
    sections = []
    for phase in data["phases"]:
        cards = []
        for item in [row for row in data["outline_units"] if row["phase"] == phase["number"]]:
            title = esc(item["title"])
            status = '<span class="status">製作中</span>'
            if item["number"] in built:
                title = f'<a href="{unit_href(built[item["number"]])}">{title}</a>'
                status = '<span class="status ready">已完成</span>'
            topics = "".join(f"<li>{esc(topic)}</li>" for topic in item["topics"])
            cards.append(f'<article class="outline-unit"><div><span>UNIT {item["number"]:02d}</span>{status}</div><h3>{title}</h3><p>{esc(item["summary"])}</p><ul>{topics}</ul></article>')
        sections.append(f'<section class="outline-phase"><div class="outline-phase-head"><div><p class="section-index">PHASE {phase["number"]:02d} / {esc(phase["range"])}</p><h2>{esc(phase["title"])}</h2></div><p><b>階段目標</b>{esc(phase["goal"])}</p></div><div class="outline-unit-grid">{"".join(cards)}</div></section>')
    body = f'<section class="simple-hero"><a class="breadcrumb" href="index.html">JAPANESE / LEARNING MAP</a><p class="eyebrow">5 PHASES · 26 UNITS</p><h1>完整課程大綱</h1><p class="hero-intro">從平假名、片假名開始，逐步讀懂生活文字、完成旅行會話並聽出關鍵資訊。</p></section><div class="full-outline">{"".join(sections)}</div><section class="phase-next"><p>READY TO START?</p><h2>先把假名讀出來，之後每一個路牌與菜單都會變得更清楚。</h2><a href="phase-1.html">開始第一階段 <span>→</span></a></section>'
    (ROOT / "outline.html").write_text(shell(title="日文完整課程大綱", description="零基礎日文五階段、26單元完整學習地圖。", body=body, prefix="", active="outline"), encoding="utf-8")


def kana_card(item: dict) -> str:
    spoken = item.get("speak", item["reading"])
    return f'<article class="alphabet-card"><button type="button" lang="ja" data-speak="{esc(spoken)}" data-audio="audio/{audio_filename(spoken)}" data-rate="1" aria-label="播放日文：{esc(item["letter"])}"><span>{esc(item["letter"])}</span><i>▶</i></button><div><b>{esc(item["romaji"])}</b><small>{esc(item["example"])}</small></div></article>'


def build_kana_page(kana: dict) -> None:
    def groups_html(groups: list[dict], prefix: str) -> str:
        rows = []
        for index, group in enumerate(groups, 1):
            cards = "".join(kana_card(item) for item in group["items"])
            rows.append(f'<section class="alphabet-group"><div class="alphabet-group-head"><span>{prefix}{index:02d}</span><div><h3>{esc(group["title"])}</h3><p>{esc(group["summary"])}</p></div></div><div class="alphabet-card-grid kana-grid">{cards}</div></section>')
        return "".join(rows)
    patterns = "".join(f'<article><span>{index:02d}</span><h3>{esc(item["title"])}</h3><p>{" · ".join(esc(value) for value in item["items"])}</p></article>' for index, item in enumerate(kana["special_patterns"], 1))
    body = f"""
      <section class="simple-hero alphabet-hero"><a class="breadcrumb" href="index.html">JAPANESE / SYSTEMATIC KANA</a><p class="eyebrow">46 HIRAGANA · 46 KATAKANA · HEPBURN</p><h1>日文假名系統課</h1><p class="hero-intro">一次看懂完整五十音地圖。羅馬拼音採 Hepburn 作記憶提示，真正發音仍以網站內建音檔為準。</p><div class="hero-actions"><a class="primary-button" href="#hiragana">先學平假名 <span>↓</span></a><a class="text-link" href="#katakana">前往片假名</a></div></section>
      <section class="system-path"><p class="section-index">00 / FIXED ORDER</p><div><h2>固定四步驟，<br />不再零散背誦。</h2><p>辨認字形、看羅馬拼音、播放聆聽、遮住答案自測。</p></div><ol><li><span>01</span>五個核心母音</li><li><span>02</span>平假名行列</li><li><span>03</span>片假名行列</li><li><span>04</span>濁音與特殊拼讀</li></ol></section>
      <section class="alphabet-schedule"><div class="section-head"><div><p class="section-index">12 DAYS / 15 MIN</p><h2>十二天假名路線</h2></div><p>每天一到兩組，前5分鐘辨字，中間5分鐘播放跟讀，最後5分鐘遮住答案自測。</p></div><div class="schedule-grid"><article><span>DAY 01–05</span><b>平假名</b><p>あ行 → ん</p></article><article><span>DAY 06</span><b>平假名總複習</b><p>46 characters</p></article><article><span>DAY 07–11</span><b>片假名</b><p>ア行 → ン</p></article><article><span>DAY 12</span><b>片假名總複習</b><p>46 characters</p></article></div></section>
      <section class="alphabet-system" id="hiragana"><div class="section-head"><div><p class="section-index">01 / HIRAGANA</p><h2>46 個平假名</h2></div><p>依五十音行列建立規律，用於日文原生詞、文法功能與漢字讀音提示。</p></div>{groups_html(kana['hiragana_groups'], 'H')}</section>
      <section class="alphabet-system consonant-system" id="katakana"><div class="section-head"><div><p class="section-index">02 / KATAKANA</p><h2>46 個片假名</h2></div><p>聲音與平假名相同，主要用於外來語、擬聲詞與醒目標示。</p></div>{groups_html(kana['katakana_groups'], 'K')}</section>
      <section class="special-patterns"><div class="section-head"><div><p class="section-index">03 / SPECIAL PATTERNS</p><h2>五種特殊拼讀</h2></div><p>濁點、圈點、小寫假名與長音符號會改變聲音，但都能接回五十音系統。</p></div><div class="pattern-grid">{patterns}</div></section>
      <section class="romanization-note"><p class="section-index">04 / HOW TO USE ROMAJI</p><div><h2>羅馬拼音是扶手，<br />不是終點。</h2><p>先用 Hepburn 提示聲音，再立刻播放音檔跟讀；熟悉後逐步把視線留在假名與漢字。</p></div><a href="phase-1.html">進入第一階段逐堂練習 →</a></section>"""
    (ROOT / "kana.html").write_text(shell(title="日文假名系統課", description="系統化學習46個平假名、46個片假名、Hepburn羅馬拼音與點擊發音。", body=body, prefix="", active="kana"), encoding="utf-8")


def unit_card(unit: dict) -> str:
    lessons = "".join(f'<li><a href="{lesson_href(unit, lesson)}"><span>{lesson["number"]:02d}</span>{esc(lesson["title"])}</a></li>' for lesson in unit["lessons"])
    return f'<article class="unit-card"><div class="unit-card-head"><span class="unit-no">UNIT {unit["number"]:02d}</span><span class="lesson-count">{len(unit["lessons"])} LESSONS</span></div><p class="japanese-unit-title" lang="ja">{esc(unit["japanese_title"])}</p><h3><a href="{unit_href(unit)}">{esc(unit["title"])}</a></h3><p>{esc(unit["summary"])}</p><ol class="mini-lessons">{lessons}</ol><a class="unit-link" href="{unit_href(unit)}">查看單元介紹 <span>↗</span></a></article>'


def build_phase_pages(data: dict) -> None:
    words = {1: "かな", 2: "標識", 3: "文", 4: "会話", 5: "総合"}
    for phase in data["phases"]:
        number = phase["number"]
        units = [unit for unit in data["units"] if phase_for_unit(data, unit["number"]) == number]
        lesson_count = sum(len(unit["lessons"]) for unit in units)
        foundation = '<section class="phase-foundation-link"><div><p class="section-index">00 / START HERE</p><h2>先看完整假名地圖</h2><p>用系統課掌握46個平假名與46個片假名，再回來依單元練習。</p></div><a href="kana.html">打開日文假名系統課 <span>→</span></a></section>' if number == 1 else ""
        next_link = f'<a href="phase-{number + 1}.html">前往第 {number + 1} 階段 <span>→</span></a>' if number < 5 else '<a href="outline.html">回到完整學習地圖 <span>→</span></a>'
        body = f'<section class="phase-hero japanese-phase-hero"><div><a class="breadcrumb" href="index.html">JAPANESE / LEARNING MAP</a><p class="eyebrow">{esc(phase["range"])} · {lesson_count} LESSONS</p><h1>第 {number} 階段｜{esc(phase["title"])}</h1><p class="hero-intro">{esc(phase["summary"])} 每天15分鐘，依照編號完成一堂課。</p><div class="course-stats"><div><strong>{len(units)}</strong><span>個單元</span></div><div><strong>{lesson_count}</strong><span>堂課</span></div><div><strong>15</strong><span>分鐘／天</span></div></div></div><aside><span>PHASE {number:02d}</span><div class="phase-hangul" lang="ja">{words[number]}</div><h2>{esc(phase["goal"])}</h2></aside></section>{foundation}<section class="outline-section"><div class="section-head"><div><p class="section-index">01 / FULL OUTLINE</p><h2>第 {number} 階段課程</h2></div><p>每堂先讀3個小段落，再聽正常與慢速音檔，最後完成兩題自我檢查。</p></div><div class="unit-grid">{"".join(unit_card(unit) for unit in units)}</div></section><section class="phase-next"><p>PHASE {number:02d} GOAL</p><h2>{esc(phase["goal"])}</h2>{next_link}</section>'
        (ROOT / f"phase-{number}.html").write_text(shell(title=f"第 {number} 階段｜{phase['title']}", description=phase["summary"], body=body, prefix="", active="outline"), encoding="utf-8")


def build_unit_pages(data: dict) -> None:
    for unit in data["units"]:
        phase_number = phase_for_unit(data, unit["number"])
        lessons = "".join(f'<article class="lesson-row"><span>{lesson["number"]:02d}</span><div><p>ZERO BEGINNER · 15 MIN</p><h3>{esc(lesson["title"])}</h3><b>{esc(lesson["subtitle"])}</b></div><a href="../{lesson_href(unit, lesson)}">開始學習 →</a></article>' for lesson in unit["lessons"])
        prereqs = "".join(f"<li>{esc(item)}</li>" for item in unit["prerequisites"])
        outcomes = "".join(f"<li>{esc(item)}</li>" for item in unit["outcomes"])
        body = f'<section class="unit-hero japanese-unit-hero"><div><a class="breadcrumb" href="../phase-{phase_number}.html">PHASE {phase_number:02d} / UNIT {unit["number"]:02d}</a><p class="eyebrow" lang="ja">{esc(unit["japanese_title"])}</p><h1>{esc(unit["title"])}</h1><p class="hero-intro">{esc(unit["summary"])}</p><a class="primary-button" href="#lessons">查看 {len(unit["lessons"])} 堂課 <span>↓</span></a></div><aside><span>UNIT</span><strong>{unit["number"]:02d}</strong><p>{esc(unit["goal"])}</p></aside></section><section class="unit-info"><div><p class="section-index">BEFORE YOU START</p><h2>開始之前</h2><ul>{prereqs}</ul></div><div><p class="section-index">AFTER THIS UNIT</p><h2>完成後你能夠</h2><ul>{outcomes}</ul></div></section><section class="lesson-section" id="lessons"><div class="section-head"><div><p class="section-index">LESSON LIST</p><h2>本單元課程</h2></div><p>先聽正常速度，再用慢速確認，最後不看提示自己讀一次。</p></div><div class="lesson-list">{lessons}</div></section><nav class="bottom-nav"><a href="../phase-{phase_number}.html">← 返回第 {phase_number} 階段</a><a href="../outline.html">完整學習地圖 ↑</a></nav>'
        output = ROOT / "units" / unit_filename(unit)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(shell(title=f"單元 {unit['number']:02d}｜{unit['title']}", description=unit["summary"], body=body, prefix="../", active="outline"), encoding="utf-8")


def render_audio(items: list[dict]) -> str:
    cards = []
    for item in items:
        text = item["text"]
        spoken = item.get("speak", text)
        romaji = item.get("romanization") or romanize(item["reading"])
        note = f'<small>{esc(item["note"])}</small>' if item.get("note") else ""
        cards.append(f'<article class="audio-card"><button class="speak-main" type="button" lang="ja" data-speak="{esc(spoken)}" data-audio="../../audio/{audio_filename(spoken)}" data-rate="1" aria-label="播放日文：{esc(text)}"><span>{esc(text)}</span><i aria-hidden="true">▶</i></button><div><span class="translation-line"><b>{esc(item["meaning"])}</b><span class="romanization"><i>H</i>{esc(romaji)}</span></span>{note}</div><button class="slow-button" type="button" data-speak="{esc(spoken)}" data-audio="../../audio/{audio_filename(spoken)}" data-rate="0.72" aria-label="慢速播放日文：{esc(text)}">慢速 0.72×</button></article>')
    return f'<div class="audio-grid">{"".join(cards)}</div>'


def render_section(section: dict, index: int) -> str:
    paragraphs = "".join(f"<p>{esc(item)}</p>" for item in section["paragraphs"])
    bullets = "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in section["bullets"]) + "</ul>"
    callout = f'<aside class="concept-callout"><b>記住這件事</b><p>{esc(section["callout"])}</p></aside>' if section.get("callout") else ""
    return f'<section class="content-section" id="section-{index}"><span class="content-index">{index:02d}</span><div><h2>{esc(section["heading"])}</h2>{paragraphs}{bullets}{render_audio(section["audio"])}{callout}</div></section>'


def build_lesson_pages(data: dict) -> None:
    all_lessons = [(unit, lesson) for unit in data["units"] for lesson in unit["lessons"]]
    for position, (unit, lesson) in enumerate(all_lessons):
        objectives = "".join(f"<li>{esc(item)}</li>" for item in lesson["objectives"])
        sections = "".join(render_section(section, index) for index, section in enumerate(lesson["sections"], 1))
        takeaways = "".join(f'<li><span>{index:02d}</span>{esc(item)}</li>' for index, item in enumerate(lesson["takeaways"], 1))
        quiz = "".join(f'<details><summary>{esc(item["question"])}</summary><p>{esc(item["answer"])}</p></details>' for item in lesson["quiz"])
        practice = "".join(f"<li>{esc(item)}</li>" for item in lesson["practice"])
        previous_link = next_link = ""
        if position:
            previous_unit, previous = all_lessons[position - 1]
            previous_link = f'<a href="../unit-{previous_unit["number"]:02d}/{lesson_filename(previous)}"><span>← 上一課</span><b>{esc(previous["title"])}</b></a>'
        if position + 1 < len(all_lessons):
            following_unit, following = all_lessons[position + 1]
            next_link = f'<a class="next" href="../unit-{following_unit["number"]:02d}/{lesson_filename(following)}"><span>下一課 →</span><b>{esc(following["title"])}</b></a>'
        body = f'<article class="lesson-page"><header class="lesson-hero"><a class="breadcrumb" href="../../units/{unit_filename(unit)}">UNIT {unit["number"]:02d} / LESSON {lesson["number"]:02d}</a><p class="eyebrow" lang="ja">{esc(unit["japanese_title"])}</p><h1>{esc(lesson["title"])}</h1><p class="lesson-deck">{esc(lesson["subtitle"])}</p><div class="lesson-meta"><span>零基礎</span><span>15 分鐘</span><span>點擊發音</span></div></header><section class="lesson-opening"><div><p class="section-index">TODAY / 15 MIN</p><p>{esc(lesson["summary"])}</p></div><div><p class="section-index">LEARNING GOALS</p><ul>{objectives}</ul></div></section><div class="lesson-content">{sections}</div><section class="takeaways"><p class="section-index">RECAP</p><h2>今天要帶走的事</h2><ol>{takeaways}</ol></section><section class="quiz"><div><p class="section-index">CHECK YOURSELF</p><h2>先想一想，再看答案</h2></div><div>{quiz}</div></section><section class="practice"><p class="section-index">2 MIN PRACTICE</p><h2>今天的練習</h2><ol>{practice}</ol></section><nav class="lesson-nav">{previous_link}{next_link}</nav></article>'
        output = ROOT / "lessons" / f"unit-{unit['number']:02d}" / lesson_filename(lesson)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(shell(title=f"{unit['number']:02d}.{lesson['number']:02d} {lesson['title']}", description=lesson["summary"], body=body, prefix="../../", active="outline"), encoding="utf-8")


def main() -> None:
    data = load_data()
    build_home(data)
    build_outline(data)
    build_kana_page(load_kana())
    build_phase_pages(data)
    build_unit_pages(data)
    build_lesson_pages(data)
    lesson_count = sum(len(unit["lessons"]) for unit in data["units"])
    print(f"Built Japanese topic: {len(data['units'])} units, {lesson_count} lessons.")


if __name__ == "__main__":
    main()
