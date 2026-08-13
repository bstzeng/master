#!/usr/bin/env python3
"""Generate the Korean beginner learning topic from curriculum.json."""

from __future__ import annotations

import html
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "curriculum.json"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def load_data() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def audio_filename(text: str) -> str:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    return f"{digest}.mp3"


def unit_filename(unit: dict) -> str:
    return f"unit-{unit['number']:02d}-{unit['slug']}.html"


def lesson_filename(lesson: dict) -> str:
    return f"{lesson['number']:02d}-{lesson['slug']}.html"


def unit_href(unit: dict, prefix: str = "") -> str:
    return f"{prefix}units/{unit_filename(unit)}"


def lesson_href(unit: dict, lesson: dict, prefix: str = "") -> str:
    return f"{prefix}lessons/unit-{unit['number']:02d}/{lesson_filename(lesson)}"


def header(prefix: str, active: str = "") -> str:
    return f"""
    <header class="site-header">
      <a class="brand" href="{prefix}../index.html" aria-label="回到 MASTER 首頁"><span class="brand-dot"></span><span>MASTER</span></a>
      <nav aria-label="韓文課程選單">
        <a class="{'is-active' if active == 'course' else ''}" href="{prefix}index.html">課程首頁</a>
        <a class="{'is-active' if active == 'outline' else ''}" href="{prefix}outline.html">完整大綱</a>
        <a class="{'is-active' if active == 'phase1' else ''}" href="{prefix}phase-1.html">第一階段</a>
      </nav>
      <span class="header-note">KOREAN / 15 MIN A DAY</span>
    </header>"""


def footer(prefix: str) -> str:
    return f"""
    <footer>
      <span>MASTER / KOREAN</span>
      <p>읽고, 듣고, 말해요.</p>
      <a href="{prefix}index.html">課程首頁 ↑</a>
    </footer>"""


def shell(*, title: str, description: str, body: str, prefix: str, active: str = "") -> str:
    document = f"""<!doctype html>
<html lang="zh-Hant">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="{esc(description)}" />
    <meta name="theme-color" content="#173f5f" />
    <title>{esc(title)}｜MASTER</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Gowun+Batang:wght@400;700&family=Noto+Sans+KR:wght@400;500;600;700&family=Noto+Sans+TC:wght@400;500;600;700&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="{prefix}styles.css" />
    <script src="{prefix}script.js?v=audio-1" defer></script>
  </head>
  <body>
    {header(prefix, active)}
    <main>{body}</main>
    {footer(prefix)}
    <div class="speech-status" data-speech-status aria-live="polite"></div>
  </body>
</html>"""
    return "\n".join(line.rstrip() for line in document.splitlines()) + "\n"


def phase_card(phase: dict, units: list[dict]) -> str:
    phase_units = [unit for unit in units if unit["phase"] == phase["number"]]
    ready = phase["number"] == 1
    items = "".join(
        f'<li><span>{unit["number"]:02d}</span><b>{esc(unit["title"])}</b></li>'
        for unit in phase_units
    )
    action = '<a href="phase-1.html">開始第一階段 <span>→</span></a>' if ready else '<span class="coming-soon">後續製作</span>'
    return f"""
      <article class="roadmap-card {'is-ready' if ready else ''}">
        <div class="roadmap-card-head"><span>PHASE {phase['number']:02d}</span><span>{esc(phase['range'])}</span></div>
        <h3>{esc(phase['title'])}</h3>
        <p>{esc(phase['summary'])}</p>
        <ol>{items}</ol>
        {action}
      </article>"""


def build_home(data: dict) -> None:
    phases = data["phases"]
    units = data["outline_units"]
    cards = "".join(phase_card(phase, units) for phase in phases)
    body = f"""
      <section class="course-hero korean-hero">
        <div class="course-hero-copy">
          <a class="breadcrumb" href="../index.html">MASTER / TOPIC 02</a>
          <p class="eyebrow">ZERO TO DAILY KOREAN · 하루 15분</p>
          <h1>從看懂字母開始，<em>走進真實韓文。</em></h1>
          <p class="hero-intro">給完全零基礎的韓文學習路線。以閱讀街頭文字為主軸，搭配日常會話與基礎聽力；每天 15 分鐘，點擊每個韓文就能直接聽發音。</p>
          <div class="course-stats"><div><strong>5</strong><span>個階段</span></div><div><strong>26</strong><span>個單元</span></div><div><strong>29</strong><span>堂課已完成</span></div></div>
          <div class="hero-actions"><a class="primary-button" href="phase-1.html">開始第一階段 <span>→</span></a><a class="text-link" href="outline.html">查看完整大綱</a></div>
        </div>
        <div class="hangul-poster">
          <span class="poster-label">HANGUL / 한글 / 001</span>
          <button class="poster-speak" type="button" lang="ko" data-speak="안녕하세요" data-audio="audio/{audio_filename('안녕하세요')}" data-rate="1" aria-label="播放韓文：안녕하세요"><span>한</span><small>點一下，聽韓文</small></button>
          <div class="poster-words"><span>읽기</span><span>듣기</span><span>말하기</span></div>
          <p>READ 50% · SPEAK 30% · LISTEN 20%</p>
        </div>
      </section>
      <section class="daily-method">
        <p class="section-index">00 / DAILY ROUTINE</p>
        <div><h2>每天只要<br />15 分鐘</h2><p>固定短時間，比偶爾一次學很多更容易把文字和聲音連起來。</p></div>
        <ol><li><span>03 MIN</span>複習昨天的聲音</li><li><span>07 MIN</span>閱讀今天的新觀念</li><li><span>03 MIN</span>點擊韓文、跟讀</li><li><span>02 MIN</span>自我測驗與街頭任務</li></ol>
      </section>
      <section class="phase-overview">
        <div class="section-head"><div><p class="section-index">01 / ROADMAP</p><h2>五階段學習地圖</h2></div><p>第一階段已完成全部內容，其餘階段先保留清楚的大綱。之後會沿著同一條路線逐單元擴充。</p></div>
        <div class="roadmap-grid">{cards}</div>
      </section>
      <section class="course-method korean-method">
        <div><p class="section-index">02 / LEARNING FOCUS</p><h2>看得懂，<br />也聽得到。</h2></div>
        <div class="method-grid"><article><span>50%</span><h3>閱讀</h3><p>從字母、招牌、菜單到交通資訊，建立實際可用的辨識力。</p></article><article><span>30%</span><h3>會話</h3><p>優先學會問候、點餐、購物、問路與需要幫助時的句子。</p></article><article><span>20%</span><h3>聽力</h3><p>每個韓文都可點擊播放，先抓關鍵字，再逐步適應自然語速。</p></article><article><span>—</span><h3>不學打字</h3><p>目前不安排韓文鍵盤，把時間集中在閱讀、理解、跟讀與聆聽。</p></article></div>
      </section>"""
    (ROOT / "index.html").write_text(shell(title="零基礎韓文", description="每天 15 分鐘，從韓文字母到街頭閱讀、日常會話與基礎聽力。", body=body, prefix="", active="course"), encoding="utf-8")


def build_outline(data: dict) -> None:
    sections = []
    for phase in data["phases"]:
        phase_units = [unit for unit in data["outline_units"] if unit["phase"] == phase["number"]]
        unit_cards = []
        for unit in phase_units:
            topics = "".join(f"<li>{esc(topic)}</li>" for topic in unit["topics"])
            if phase["number"] == 1:
                built = next(item for item in data["units"] if item["number"] == unit["number"])
                title = f'<a href="{unit_href(built)}">{esc(unit["title"])}</a>'
                status = '<span class="status ready">已完成</span>'
            else:
                title = esc(unit["title"])
                status = '<span class="status">後續製作</span>'
            unit_cards.append(f'<article class="outline-unit"><div><span>UNIT {unit["number"]:02d}</span>{status}</div><h3>{title}</h3><p>{esc(unit["summary"])}</p><ul>{topics}</ul></article>')
        sections.append(f"""
        <section class="outline-phase">
          <div class="outline-phase-head"><div><p class="section-index">PHASE {phase['number']:02d} / {esc(phase['range'])}</p><h2>{esc(phase['title'])}</h2></div><p><b>階段目標</b>{esc(phase['goal'])}</p></div>
          <div class="outline-unit-grid">{''.join(unit_cards)}</div>
        </section>""")
    body = f"""
      <section class="simple-hero"><a class="breadcrumb" href="index.html">KOREAN / LEARNING MAP</a><p class="eyebrow">5 PHASES · 26 UNITS</p><h1>完整課程大綱</h1><p class="hero-intro">目標是能閱讀生活中常見的韓文、完成基本日常對話，並聽出句子裡的關鍵字。第一階段已完成，後續內容會依此順序製作。</p></section>
      <div class="full-outline">{''.join(sections)}</div>
      <section class="phase-next"><p>READY TO START?</p><h2>先把韓文字母讀出來，之後每一個路牌與菜單都會變得更清楚。</h2><a href="phase-1.html">開始第一階段 <span>→</span></a></section>"""
    (ROOT / "outline.html").write_text(shell(title="韓文完整課程大綱", description="零基礎韓文五階段、二十六單元完整學習地圖。", body=body, prefix="", active="outline"), encoding="utf-8")


def unit_card(unit: dict) -> str:
    lessons = "".join(f'<li><a href="{lesson_href(unit, lesson)}"><span>{lesson["number"]:02d}</span>{esc(lesson["title"])}</a></li>' for lesson in unit["lessons"])
    return f"""
      <article class="unit-card">
        <div class="unit-card-head"><span class="unit-no">UNIT {unit['number']:02d}</span><span class="lesson-count">{len(unit['lessons'])} LESSONS</span></div>
        <p class="korean-unit-title" lang="ko">{esc(unit['korean_title'])}</p><h3><a href="{unit_href(unit)}">{esc(unit['title'])}</a></h3><p>{esc(unit['summary'])}</p>
        <ol class="mini-lessons">{lessons}</ol><a class="unit-link" href="{unit_href(unit)}">查看單元介紹 <span>↗</span></a>
      </article>"""


def build_phase_one(data: dict) -> None:
    units = data["units"]
    body = f"""
      <section class="phase-hero korean-phase-hero">
        <div><a class="breadcrumb" href="index.html">KOREAN / LEARNING MAP</a><p class="eyebrow">UNIT 01—06 · 29 LESSONS</p><h1>第一階段｜先把韓文讀出來</h1><p class="hero-intro">從音節方塊、基本母音與子音開始，學會 받침 和最常遇到的發音變化。每天 15 分鐘，依照編號完成一堂課。</p><div class="course-stats"><div><strong>6</strong><span>個單元</span></div><div><strong>29</strong><span>堂課</span></div><div><strong>15</strong><span>分鐘／天</span></div></div></div>
        <aside><span>PHASE 01</span><div class="phase-hangul" lang="ko">읽기</div><h2>看到陌生的簡單韓文時，能拆開音節、嘗試拼讀。</h2></aside>
      </section>
      <section class="outline-section"><div class="section-head"><div><p class="section-index">01 / FULL OUTLINE</p><h2>第一階段課程</h2></div><p>每堂課先讀 3 個小段落，再點擊韓文聽正常速度與慢速，最後完成兩題自我檢查。</p></div><div class="unit-grid">{''.join(unit_card(unit) for unit in units)}</div></section>
      <section class="phase-next"><p>PHASE 01 GOAL</p><h2>完成後，你會看得出韓文的組成方式，並能拼讀常見招牌與地名。</h2><a href="{unit_href(units[0])}">從 UNIT 01 開始 <span>→</span></a></section>"""
    (ROOT / "phase-1.html").write_text(shell(title="第一階段｜先把韓文讀出來", description="韓文零基礎第一階段：字母、받침 與常見發音變化。", body=body, prefix="", active="phase1"), encoding="utf-8")


def build_unit_pages(data: dict) -> None:
    for unit in data["units"]:
        lessons = "".join(f"""
        <article class="lesson-row"><span>{lesson['number']:02d}</span><div><p>ZERO BEGINNER · 15 MIN</p><h3>{esc(lesson['title'])}</h3><b>{esc(lesson['subtitle'])}</b></div><a href="../{lesson_href(unit, lesson)}">開始學習 →</a></article>""" for lesson in unit["lessons"])
        prereqs = "".join(f"<li>{esc(item)}</li>" for item in unit["prerequisites"])
        outcomes = "".join(f"<li>{esc(item)}</li>" for item in unit["outcomes"])
        body = f"""
      <section class="unit-hero korean-unit-hero"><div><a class="breadcrumb" href="../phase-1.html">PHASE 01 / UNIT {unit['number']:02d}</a><p class="eyebrow" lang="ko">{esc(unit['korean_title'])}</p><h1>{esc(unit['title'])}</h1><p class="hero-intro">{esc(unit['summary'])}</p><a class="primary-button" href="#lessons">查看 {len(unit['lessons'])} 堂課 <span>↓</span></a></div><aside><span>UNIT</span><strong>{unit['number']:02d}</strong><p>{esc(unit['goal'])}</p></aside></section>
      <section class="unit-info"><div><p class="section-index">BEFORE YOU START</p><h2>開始之前</h2><ul>{prereqs}</ul></div><div><p class="section-index">AFTER THIS UNIT</p><h2>完成後你能夠</h2><ul>{outcomes}</ul></div></section>
      <section class="lesson-section" id="lessons"><div class="section-head"><div><p class="section-index">LESSON LIST</p><h2>本單元課程</h2></div><p>每堂約 15 分鐘。建議先聽正常速度，再用慢速確認聲音，最後不看提示自己讀一次。</p></div><div class="lesson-list">{lessons}</div></section>
      <nav class="bottom-nav"><a href="../phase-1.html">← 返回第一階段</a><a href="../outline.html">完整學習地圖 ↑</a></nav>"""
        output = ROOT / "units" / unit_filename(unit)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(shell(title=f"單元 {unit['number']:02d}｜{unit['title']}", description=unit["summary"], body=body, prefix="../", active="phase1"), encoding="utf-8")


def render_audio(items: list[dict]) -> str:
    cards = []
    for item in items:
        text = item["text"]
        spoken = item.get("speak", text)
        note = f'<small>{esc(item["note"])}</small>' if item.get("note") else ""
        cards.append(f"""
        <article class="audio-card">
          <button class="speak-main" type="button" lang="ko" data-speak="{esc(spoken)}" data-audio="../../audio/{audio_filename(spoken)}" data-rate="1" aria-label="播放韓文：{esc(text)}"><span>{esc(text)}</span><i aria-hidden="true">▶</i></button>
          <div><b>{esc(item.get('meaning', ''))}</b>{note}</div>
          <button class="slow-button" type="button" data-speak="{esc(spoken)}" data-audio="../../audio/{audio_filename(spoken)}" data-rate="0.72" aria-label="慢速播放韓文：{esc(text)}">慢速 0.72×</button>
        </article>""")
    return f'<div class="audio-grid">{"".join(cards)}</div>'


def render_section(section: dict, index: int) -> str:
    paragraphs = "".join(f"<p>{esc(text)}</p>" for text in section.get("paragraphs", []))
    bullets = "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in section.get("bullets", [])) + "</ul>"
    audio = render_audio(section["audio"]) if section.get("audio") else ""
    callout = f'<aside class="concept-callout"><b>記住這件事</b><p>{esc(section["callout"])}</p></aside>' if section.get("callout") else ""
    return f'<section class="content-section" id="section-{index}"><span class="content-index">{index:02d}</span><div><h2>{esc(section["heading"])}</h2>{paragraphs}{bullets}{audio}{callout}</div></section>'


def build_lesson_pages(data: dict) -> None:
    all_lessons = [(unit, lesson) for unit in data["units"] for lesson in unit["lessons"]]
    for global_index, (unit, lesson) in enumerate(all_lessons):
        sections = "".join(render_section(section, index) for index, section in enumerate(lesson["sections"], 1))
        objectives = "".join(f"<li>{esc(item)}</li>" for item in lesson["objectives"])
        takeaways = "".join(f"<li><span>{index:02d}</span>{esc(item)}</li>" for index, item in enumerate(lesson["takeaways"], 1))
        quiz = "".join(f'<details><summary>{esc(item["question"])}</summary><p>{esc(item["answer"])}</p></details>' for item in lesson["quiz"])
        practice = "".join(f"<li>{esc(item)}</li>" for item in lesson["practice"])
        previous = all_lessons[global_index - 1] if global_index else None
        following = all_lessons[global_index + 1] if global_index + 1 < len(all_lessons) else None
        previous_link = ""
        next_link = ""
        if previous:
            prev_unit, prev_lesson = previous
            previous_link = f'<a href="../unit-{prev_unit["number"]:02d}/{lesson_filename(prev_lesson)}"><span>← 上一課</span><b>{esc(prev_lesson["title"])}</b></a>'
        if following:
            next_unit, next_lesson = following
            next_link = f'<a class="next" href="../unit-{next_unit["number"]:02d}/{lesson_filename(next_lesson)}"><span>下一課 →</span><b>{esc(next_lesson["title"])}</b></a>'
        body = f"""
      <article class="lesson-page">
        <header class="lesson-hero"><a class="breadcrumb" href="../../units/{unit_filename(unit)}">UNIT {unit['number']:02d} / LESSON {lesson['number']:02d}</a><p class="eyebrow" lang="ko">{esc(unit['korean_title'])}</p><h1>{esc(lesson['title'])}</h1><p class="lesson-deck">{esc(lesson['subtitle'])}</p><div class="lesson-meta"><span>零基礎</span><span>15 分鐘</span><span>點擊發音</span></div></header>
        <section class="lesson-opening"><div><p class="section-index">TODAY / 15 MIN</p><p>{esc(lesson['summary'])}</p></div><div><p class="section-index">LEARNING GOALS</p><ul>{objectives}</ul></div></section>
        <div class="lesson-content">{sections}</div>
        <section class="takeaways"><p class="section-index">RECAP</p><h2>今天要帶走的事</h2><ol>{takeaways}</ol></section>
        <section class="quiz"><div><p class="section-index">CHECK YOURSELF</p><h2>先想一想，再看答案</h2></div><div>{quiz}</div></section>
        <section class="practice"><p class="section-index">2 MIN PRACTICE</p><h2>今天的練習</h2><ol>{practice}</ol></section>
        <nav class="lesson-nav">{previous_link}{next_link}</nav>
      </article>"""
        output = ROOT / "lessons" / f"unit-{unit['number']:02d}" / lesson_filename(lesson)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(shell(title=f"{unit['number']:02d}.{lesson['number']:02d} {lesson['title']}", description=lesson["summary"], body=body, prefix="../../", active="phase1"), encoding="utf-8")


def main() -> None:
    data = load_data()
    build_home(data)
    build_outline(data)
    build_phase_one(data)
    build_unit_pages(data)
    build_lesson_pages(data)
    lesson_count = sum(len(unit["lessons"]) for unit in data["units"])
    print(f"Built Korean topic: {len(data['phases'])} phases, {len(data['units'])} ready units, {lesson_count} lessons.")


if __name__ == "__main__":
    main()
