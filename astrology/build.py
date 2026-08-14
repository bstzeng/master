#!/usr/bin/env python3
"""Build the static astrology course."""

from __future__ import annotations

import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from data.course import PHASES, SOURCES, all_units  # noqa: E402


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def unit_file(unit: dict) -> str:
    return f"unit-{unit['number']:02d}-{unit['slug']}.html"


def wheel() -> str:
    glyphs = ["♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"]
    items = "".join(f'<span style="--i:{index}">{glyph}</span>' for index, glyph in enumerate(glyphs))
    return f'<div class="zodiac-wheel" aria-hidden="true"><div class="wheel-orbit">{items}</div><div class="wheel-core"><b>12</b><small>SIGNS</small></div></div>'


def shell(*, title: str, description: str, body: str, prefix: str = "", active: str = "") -> str:
    nav = [
        ("course", "課程首頁", f"{prefix}index.html"),
        ("outline", "完整大綱", f"{prefix}outline.html"),
        ("sources", "資料與界線", f"{prefix}sources.html"),
    ]
    links = "".join(f'<a class="{"is-active" if key == active else ""}" href="{href}">{label}</a>' for key, label, href in nav)
    og = "https://bstzeng.github.io/master/astrology/assets/og.png"
    return f'''<!doctype html>
<html lang="zh-Hant">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="{esc(description)}" />
    <meta name="theme-color" content="#11152a" />
    <meta property="og:title" content="{esc(title)}｜星座學習地圖" />
    <meta property="og:description" content="{esc(description)}" />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="{og}" />
    <meta name="twitter:card" content="summary_large_image" />
    <title>{esc(title)}｜MASTER</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Noto+Sans+TC:wght@400;500;600;700&family=Noto+Serif+TC:wght@600;700;900&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="{prefix}styles.css" />
    <script src="{prefix}script.js" defer></script>
  </head>
  <body>
    <div class="reading-progress" aria-hidden="true"><span></span></div>
    <header class="site-header">
      <a class="brand" href="{prefix}../index.html" aria-label="回到 MASTER 首頁"><span class="brand-star">✦</span><span>MASTER</span></a>
      <nav aria-label="星座課程選單">{links}</nav>
      <span class="header-note">ASTROLOGY / CULTURE & SELF-REFLECTION</span>
    </header>
    <main>{body}</main>
    <footer><span>MASTER / TOPIC 04</span><p>用星座提問，不用星座替人定義。</p><span>© <b id="current-year"></b> PATRICK</span></footer>
  </body>
</html>
'''


def phase_for(number: int) -> dict:
    return next(phase for phase in PHASES if number in phase["units"])


def unit_card(unit: dict, prefix: str = "") -> str:
    glyph = unit.get("glyph", f"{unit['number']:02d}")
    return f'''<article class="unit-card">
      <a href="{prefix}units/{unit_file(unit)}" aria-label="閱讀單元 {unit['number']:02d}：{esc(unit['title'])}"></a>
      <div class="unit-card-top"><span>UNIT {unit['number']:02d}</span><b>{esc(glyph)}</b></div>
      <p>{esc(unit['english'])}</p><h3>{esc(unit['title'])}</h3><div>{esc(unit['subtitle'])}</div><i>完整教學頁 →</i>
    </article>'''


def build_home(units: list[dict]) -> None:
    phase_cards = []
    for phase in PHASES:
        phase_units = [unit for unit in units if unit["phase"] == phase["number"]]
        names = "".join(f'<li><a href="units/{unit_file(unit)}"><span>{unit["number"]:02d}</span>{esc(unit["title"])}</a></li>' for unit in phase_units)
        phase_cards.append(f'''<article class="phase-card"><div class="phase-card-head"><span>PHASE {phase['number']:02d}</span><b>{esc(phase['range'])}</b></div><h3>{esc(phase['title'])}</h3><p>{esc(phase['summary'])}</p><ol>{names}</ol><a class="phase-link" href="phase-{phase['number']}.html">進入第 {phase['number']} 階段 →</a></article>''')
    body = f'''
      <section class="course-hero">
        <div class="course-hero-copy"><a class="breadcrumb" href="../index.html">MASTER / TOPIC 04</a><p class="eyebrow">ORIGIN · PERSONALITY · RELATIONSHIPS</p><h1>讀懂星座，<em>也保留思考。</em></h1><p class="hero-intro">從星座起源、十二星座人格，到感情、友情、家庭、職場與基礎星盤。占星作為文化與自我觀察語言；重要判斷仍回到證據、界線與真實行為。</p><div class="course-stats"><div><strong>5</strong><span>個階段</span></div><div><strong>36</strong><span>個單元</span></div><div><strong>36</strong><span>完整教學頁</span></div></div><div class="hero-actions"><a class="primary-button" href="phase-1.html">從起源開始 <span>→</span></a><a class="text-link" href="outline.html">查看完整大綱</a></div></div>
        <div class="hero-wheel"><p>THE ZODIAC / A SYMBOLIC MAP</p>{wheel()}<small>ASTRONOMY ≠ ASTROLOGY</small></div>
      </section>
      <section class="course-principles"><p class="section-index">00 / HOW TO READ</p><div><h2>三條閱讀原則</h2><p>保留星座的歷史、神話與自我反思價值，同時避免把象徵變成不可改變的人格判決。</p></div><ol><li><span>01</span><b>先理解起源</b><p>區分天空、星座與十二宮。</p></li><li><span>02</span><b>把描述當假設</b><p>回到情境與實際行為驗證。</p></li><li><span>03</span><b>關係先看安全</b><p>同意、界線與修復永遠優先。</p></li></ol></section>
      <section class="roadmap"><div class="section-head"><div><p class="section-index">01 / ROADMAP</p><h2>五階段學習地圖</h2></div><p>每個單元就是一頁完整教學，依序閱讀能從歷史建立框架，再進入人格、關係與星盤。</p></div><div class="phase-grid">{''.join(phase_cards)}</div></section>
      <section class="evidence-banner"><div><p class="section-index">02 / IMPORTANT BOUNDARY</p><h2>星座可以是鏡子，<br />不是診斷書。</h2></div><div><p>現有科學證據不支持用出生星盤可靠預測人格。課程仍會完整介紹占星傳統，但用「可能、傾向、提問」而不是「一定、命定、天生如此」。</p><a href="sources.html">閱讀資料來源與使用界線 →</a></div></section>
      <section class="sign-entry"><div><p class="section-index">03 / TWELVE SIGNS</p><h2>十二星座，<br />十二種完整閱讀。</h2><p>每一頁固定包含神話、元素模式、核心動機、優勢陰影、感情友情、家庭職場與成長練習。</p><a class="primary-button" href="phase-3.html">進入十二星座 <span>→</span></a></div>{wheel()}</section>'''
    (ROOT / "index.html").write_text(shell(title="星座學習地圖", description="36個完整單元，系統理解星座起源、人格、關係與基礎星盤。", body=body, active="course"), encoding="utf-8")


def build_outline(units: list[dict]) -> None:
    sections = []
    for phase in PHASES:
        cards = "".join(unit_card(unit) for unit in units if unit["phase"] == phase["number"])
        sections.append(f'''<section class="outline-phase" id="phase-{phase['number']}"><div class="outline-phase-head"><div><p class="section-index">PHASE {phase['number']:02d} / {esc(phase['range'])}</p><h2>{esc(phase['title'])}</h2></div><p><b>階段目標</b>{esc(phase['goal'])}</p></div><div class="unit-grid">{cards}</div></section>''')
    body = f'''<section class="simple-hero"><a class="breadcrumb" href="index.html">ASTROLOGY / LEARNING MAP</a><p class="eyebrow">5 PHASES · 36 COMPLETE UNITS</p><h1>完整課程大綱</h1><p class="hero-intro">從人類仰望星空開始，依序理解十二星座人格、關係互動、基礎星盤與科學思考。</p></section><div class="full-outline">{''.join(sections)}</div><section class="page-next"><p>READY TO START?</p><h2>先知道星座從哪裡來，之後的人格閱讀才有穩固的地基。</h2><a href="phase-1.html">開始第一階段 →</a></section>'''
    (ROOT / "outline.html").write_text(shell(title="星座完整課程大綱", description="五階段、36單元的星座起源、人格、關係與星盤課程。", body=body, active="outline"), encoding="utf-8")


def build_phase_pages(units: list[dict]) -> None:
    phase_words = {1: "ORIGIN", 2: "FRAME", 3: "SIGNS", 4: "RELATE", 5: "CHART"}
    for phase in PHASES:
        phase_units = [unit for unit in units if unit["phase"] == phase["number"]]
        cards = "".join(unit_card(unit) for unit in phase_units)
        next_link = f'<a href="phase-{phase["number"] + 1}.html">前往第 {phase["number"] + 1} 階段 →</a>' if phase["number"] < 5 else '<a href="sources.html">閱讀資料與科學界線 →</a>'
        body = f'''<section class="phase-hero"><div><a class="breadcrumb" href="outline.html">ASTROLOGY / PHASE {phase['number']:02d}</a><p class="eyebrow">{esc(phase['range'])}</p><h1>第 {phase['number']} 階段｜{esc(phase['title'])}</h1><p class="hero-intro">{esc(phase['summary'])}</p><div class="course-stats"><div><strong>{len(phase_units)}</strong><span>個完整單元</span></div><div><strong>{phase_units[0]['number']:02d}</strong><span>起始單元</span></div><div><strong>{phase_units[-1]['number']:02d}</strong><span>完成單元</span></div></div></div><aside><span>PHASE {phase['number']:02d}</span><b>{phase_words[phase['number']]}</b><p>{esc(phase['goal'])}</p></aside></section><section class="phase-units"><div class="section-head"><div><p class="section-index">FULL UNITS</p><h2>本階段課程</h2></div><p>每頁都有完整觀念、例子、重點整理、測驗、練習與資料來源。</p></div><div class="unit-grid">{cards}</div></section><section class="page-next"><p>PHASE {phase['number']:02d} GOAL</p><h2>{esc(phase['goal'])}</h2>{next_link}</section>'''
        (ROOT / f"phase-{phase['number']}.html").write_text(shell(title=f"第 {phase['number']} 階段｜{phase['title']}", description=phase["summary"], body=body, active="outline"), encoding="utf-8")


def section_html(section: dict, index: int) -> str:
    bullets = "".join(f"<li>{esc(point)}</li>" for point in section["points"])
    return f'''<section class="lesson-section" id="section-{index}"><span class="section-number">{index:02d}</span><div><h2>{esc(section['heading'])}</h2><p>{esc(section['body'])}</p><ul>{bullets}</ul><aside><b>閱讀提示</b><p>{esc(section['note'])}</p></aside></div></section>'''


def build_unit_pages(units: list[dict]) -> None:
    output_dir = ROOT / "units"
    output_dir.mkdir(parents=True, exist_ok=True)
    for position, unit in enumerate(units):
        phase = phase_for(unit["number"])
        objectives = "".join(f"<li>{esc(item)}</li>" for item in unit["objectives"])
        profile = ""
        if unit.get("profile"):
            profile_items = "".join(f'<div><span>{label}</span><b>{esc(value)}</b></div>' for label, value in [("約略日期", unit["profile"]["dates"]), ("元素", unit["profile"]["element"] + "象"), ("模式", unit["profile"]["mode"] + "宮"), ("守護星", unit["profile"]["ruler"]), ("極性", unit["profile"]["polarity"])])
            profile = f'<section class="sign-profile"><span class="sign-glyph">{esc(unit["profile"]["glyph"])}</span><div class="profile-grid">{profile_items}</div></section>'
        sections = "".join(section_html(section, index) for index, section in enumerate(unit["sections"], 1))
        toc = "".join(f'<li><a href="#section-{index}"><span>{index:02d}</span>{esc(section["heading"])}</a></li>' for index, section in enumerate(unit["sections"], 1))
        takeaways = "".join(f'<li><span>{index:02d}</span>{esc(item)}</li>' for index, item in enumerate(unit["takeaways"], 1))
        quiz = "".join(f'<details><summary>{esc(question)}</summary><p>{esc(answer)}</p></details>' for question, answer in unit["quiz"])
        sources = "".join(f'<li><a href="{esc(source["url"])}" target="_blank" rel="noreferrer"><b>{esc(source["title"])}</b><span>{esc(source["note"])}</span></a></li>' for source in unit["sources"])
        previous = units[position - 1] if position else None
        following = units[position + 1] if position + 1 < len(units) else None
        previous_link = f'<a href="{unit_file(previous)}"><span>← 上一單元</span><b>{esc(previous["title"])}</b></a>' if previous else '<a href="../outline.html"><span>← 返回</span><b>完整課程大綱</b></a>'
        next_link = f'<a class="next" href="{unit_file(following)}"><span>下一單元 →</span><b>{esc(following["title"])}</b></a>' if following else '<a class="next" href="../index.html"><span>完成課程 →</span><b>回到主題首頁</b></a>'
        glyph = unit.get("glyph", f"{unit['number']:02d}")
        body = f'''<article class="unit-page"><header class="unit-hero"><div><a class="breadcrumb" href="../phase-{phase['number']}.html">PHASE {phase['number']:02d} / UNIT {unit['number']:02d}</a><p class="eyebrow">{esc(unit['english'])}</p><h1>{esc(unit['title'])}</h1><p class="unit-deck">{esc(unit['subtitle'])}</p><div class="unit-meta"><span>完整教學</span><span>{len(unit['sections'])} 個章節</span><span>附測驗與練習</span></div></div><aside><span>UNIT</span><b>{esc(glyph)}</b><small>{unit['number']:02d} / 36</small></aside></header>{profile}<section class="unit-opening"><div><p class="section-index">WHY THIS MATTERS</p><p>{esc(unit['opening'])}</p></div><div><p class="section-index">LEARNING GOALS</p><ul>{objectives}</ul></div></section><div class="unit-body"><aside class="contents"><p>本頁章節</p><ol>{toc}</ol><a href="#practice">前往練習 ↓</a></aside><div class="unit-content">{sections}</div></div><section class="takeaways"><p class="section-index">RECAP</p><h2>這個單元要帶走的事</h2><ol>{takeaways}</ol></section><section class="quiz"><div><p class="section-index">CHECK YOURSELF</p><h2>先想一想，<br />再展開答案。</h2></div><div>{quiz}</div></section><section class="practice" id="practice"><p class="section-index">OBSERVATION PRACTICE</p><h2>把概念放回生活</h2><p>{esc(unit['practice'])}</p></section><section class="sources"><div><p class="section-index">SOURCES & FURTHER READING</p><h2>資料來源</h2><p>歷史與科學主張連結至館藏、學術或專業機構；人格段落依占星傳統整理，請作為反思語言而非科學診斷。</p></div><ul>{sources}</ul></section><nav class="unit-nav">{previous_link}{next_link}</nav></article>'''
        (output_dir / unit_file(unit)).write_text(shell(title=f"單元 {unit['number']:02d}｜{unit['title']}", description=unit["subtitle"], body=body, prefix="../", active="outline"), encoding="utf-8")


def build_sources() -> None:
    cards = "".join(f'<article><span>{index:02d}</span><div><h3><a href="{esc(source["url"])}" target="_blank" rel="noreferrer">{esc(source["title"])} ↗</a></h3><p>{esc(source["note"])}</p></div></article>' for index, source in enumerate(SOURCES.values(), 1))
    body = f'''<section class="simple-hero"><a class="breadcrumb" href="index.html">ASTROLOGY / SOURCES</a><p class="eyebrow">HISTORY · EVIDENCE · RESPONSIBLE USE</p><h1>資料來源與使用界線</h1><p class="hero-intro">本課程完整介紹西洋占星的歷史與象徵，同時清楚區分天文事實、占星傳統與科學證據。</p></section><section class="boundary-grid"><article><span>01</span><h2>天文事實</h2><p>星座邊界、黃道、歲差與天體位置，以國際天文聯合會等天文資料為準。</p></article><article><span>02</span><h2>占星傳統</h2><p>元素、模式、行星與人格關鍵詞是歷史形成的象徵語言，不宣稱具有已證實的因果作用。</p></article><article><span>03</span><h2>科學證據</h2><p>現有研究不支持出生星盤能可靠描述或配對人格；主觀準確感也可能受巴納姆效應影響。</p></article><article><span>04</span><h2>負責任使用</h2><p>不用星座做醫療、心理、法律、財務或人事判斷，也不用它合理化控制、暴力與歧視。</p></article></section><section class="source-library"><div class="section-head"><div><p class="section-index">SOURCE LIBRARY</p><h2>本課程引用資料</h2></div><p>連結直接前往原始研究、專業機構或博物館館藏頁面。</p></div><div>{cards}</div></section><section class="evidence-banner"><div><p class="section-index">A USEFUL POSITION</p><h2>可以享受象徵，<br />也可以要求證據。</h2></div><div><p>兩者並不衝突。只要清楚說明自己正在使用的是文化隱喻、個人經驗或可檢驗主張，就能讓討論更誠實。</p><a href="units/unit-36-critical-thinking-and-summary.html">閱讀最後一單元 →</a></div></section>'''
    (ROOT / "sources.html").write_text(shell(title="資料來源與使用界線", description="星座課程的天文、歷史、心理學資料來源與負責任使用原則。", body=body, active="sources"), encoding="utf-8")


def main() -> None:
    units = all_units()
    build_home(units)
    build_outline(units)
    build_phase_pages(units)
    build_unit_pages(units)
    build_sources()
    print(f"Built astrology topic: {len(PHASES)} phases, {len(units)} complete unit pages.")


if __name__ == "__main__":
    main()
