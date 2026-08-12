#!/usr/bin/env python3
"""Generate the static Python algorithms course from unit JSON files."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

PHASES = {
    1: {
        "title": "第一階段｜基本功",
        "short": "資料結構與演算法基本功",
        "range": "UNIT 01—10",
        "summary": "從複雜度與 Python 內建結構開始，依序掌握陣列、搜尋、排序、鏈結串列、堆疊、樹與圖。",
        "goal": "建立分析效率、選擇資料結構、讀懂並親手寫出經典演算法的能力。",
    },
    2: {
        "title": "第二階段｜進階解題",
        "short": "進階演算法與綜合解題",
        "range": "UNIT 11—16",
        "summary": "進入加權圖、貪心、動態規劃、字串演算法與進階資料結構，最後整合成一套解題方法。",
        "goal": "面對陌生問題時，能分析限制、選擇策略、證明正確性並評估效能。",
    },
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def load_units() -> list[dict]:
    units = []
    for path in sorted(DATA_DIR.glob("unit-*.json")):
        with path.open(encoding="utf-8") as file:
            unit = json.load(file)
        unit["_file"] = path.name
        units.append(unit)
    units.sort(key=lambda item: item["number"])
    return units


def unit_filename(unit: dict) -> str:
    return f"unit-{unit['number']:02d}-{unit['slug']}.html"


def lesson_filename(unit: dict, lesson: dict) -> str:
    return f"{lesson['number']:02d}-{lesson['slug']}.html"


def header(prefix: str, active: str = "") -> str:
    return f"""
    <header class="site-header">
      <a class="brand" href="{prefix}../index.html" aria-label="回到 MASTER 首頁"><span class="brand-dot"></span><span>MASTER</span></a>
      <nav aria-label="Python 課程選單">
        <a class="{'is-active' if active == 'course' else ''}" href="{prefix}index.html">課程總覽</a>
        <a class="{'is-active' if active == 'phase1' else ''}" href="{prefix}phase-1.html">第一階段</a>
        <a class="{'is-active' if active == 'phase2' else ''}" href="{prefix}phase-2.html">第二階段</a>
      </nav>
      <span class="header-note">PYTHON / DATA STRUCTURES / ALGORITHMS</span>
    </header>"""


def footer(prefix: str) -> str:
    return f"""
    <footer>
      <span>MASTER / PYTHON</span>
      <p>Understand it. Trace it. Build it.</p>
      <a href="{prefix}index.html">課程總覽 ↑</a>
    </footer>"""


def shell(*, title: str, description: str, body: str, prefix: str, active: str = "") -> str:
    document = f"""<!doctype html>
<html lang="zh-Hant">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="{esc(description)}" />
    <meta name="theme-color" content="#101713" />
    <title>{esc(title)}｜MASTER</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Noto+Sans+TC:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,700;1,700&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="{prefix}styles.css" />
    <script src="{prefix}script.js" defer></script>
  </head>
  <body>
    {header(prefix, active)}
    <main>{body}</main>
    {footer(prefix)}
  </body>
</html>
"""
    return "\n".join(line.rstrip() for line in document.splitlines()) + "\n"


def unit_href(unit: dict, prefix: str = "") -> str:
    return f"{prefix}units/{unit_filename(unit)}"


def lesson_href(unit: dict, lesson: dict, prefix: str = "") -> str:
    return f"{prefix}lessons/unit-{unit['number']:02d}/{lesson_filename(unit, lesson)}"


def unit_card(unit: dict, *, prefix: str = "") -> str:
    lesson_items = "".join(
        f'<li><a href="{lesson_href(unit, lesson, prefix)}"><span>{lesson["number"]:02d}</span>{esc(lesson["title"])}</a></li>'
        for lesson in unit["lessons"]
    )
    return f"""
      <article class="unit-card">
        <div class="unit-card-head">
          <span class="unit-no">UNIT {unit['number']:02d}</span>
          <span class="lesson-count">{len(unit['lessons'])} LESSONS</span>
        </div>
        <h3><a href="{unit_href(unit, prefix)}">{esc(unit['title'])}</a></h3>
        <p>{esc(unit['summary'])}</p>
        <ol class="mini-lessons">{lesson_items}</ol>
        <a class="unit-link" href="{unit_href(unit, prefix)}">查看單元介紹 <span>↗</span></a>
      </article>"""


def build_topic_home(units: list[dict]) -> None:
    phase_cards = []
    for phase_number, phase in PHASES.items():
        phase_units = [unit for unit in units if unit["phase"] == phase_number]
        unit_list = "".join(
            f'<li><span>{unit["number"]:02d}</span><a href="{unit_href(unit)}">{esc(unit["title"])}</a></li>'
            for unit in phase_units
        )
        phase_cards.append(f"""
        <article class="phase-card phase-{phase_number}">
          <p>{phase['range']}</p>
          <h2>{phase['title']}</h2>
          <p>{phase['summary']}</p>
          <ol>{unit_list}</ol>
          <a href="phase-{phase_number}.html">查看完整大綱 <span>→</span></a>
        </article>""")

    total_lessons = sum(len(unit["lessons"]) for unit in units)
    body = f"""
      <section class="course-hero">
        <div class="course-hero-copy">
          <a class="breadcrumb" href="../index.html">MASTER / TOPIC 01</a>
          <p class="eyebrow">PYTHON · DATA STRUCTURES · ALGORITHMS</p>
          <h1>不只寫得出來，<em>還要知道為什麼。</em></h1>
          <p class="hero-intro">從 Python 熟悉的容器出發，建立資料結構、演算法與複雜度的完整地圖。每一課都會先用直覺理解，再手動推演、閱讀程式碼，最後練習判斷何時該使用它。</p>
          <div class="course-stats"><div><strong>2</strong><span>個階段</span></div><div><strong>{len(units)}</strong><span>個單元</span></div><div><strong>{total_lessons}</strong><span>堂課</span></div></div>
          <a class="primary-button" href="phase-1.html">從第一階段開始 <span>↓</span></a>
        </div>
        <div class="code-poster" aria-hidden="true">
          <span class="poster-label">LEARNING MAP / 001</span>
          <div class="poster-code"><i>def</i> learn(problem):<br />&nbsp;&nbsp;understand(problem)<br />&nbsp;&nbsp;trace(problem)<br />&nbsp;&nbsp;<b>return</b> solve(problem)</div>
          <div class="poster-orbit"><span>O(n)</span><span>O(log n)</span><span>O(1)</span></div>
          <p>READ → TRACE → IMPLEMENT → EXPLAIN</p>
        </div>
      </section>
      <section class="learning-principles">
        <p class="section-index">00 / HOW TO LEARN</p>
        <div><h2>每一課都走過<br />四個步驟</h2><p>先理解問題，再追蹤資料如何移動；接著讀懂 Python 實作，最後用自己的話解釋複雜度與適用情境。</p></div>
        <ol><li><span>01</span>建立直覺</li><li><span>02</span>手動推演</li><li><span>03</span>閱讀實作</li><li><span>04</span>練習判斷</li></ol>
      </section>
      <section class="phase-overview" id="roadmap">
        <div class="section-head"><div><p class="section-index">01 / ROADMAP</p><h2>完整學習路線</h2></div><p>依照編號前進。第一階段先打好基本功，完成後再進入需要更多組合與判斷的第二階段。</p></div>
        <div class="phase-grid">{''.join(phase_cards)}</div>
      </section>
      <section class="course-method">
        <div><p class="section-index">02 / COURSE FORMAT</p><h2>不是背模板，<br />是建立判斷力。</h2></div>
        <div class="method-grid"><article><span>A</span><h3>觀念</h3><p>用清楚的語言建立模型，知道問題真正困難在哪裡。</p></article><article><span>B</span><h3>實作</h3><p>閱讀簡潔的 Python，逐步看見資料與狀態如何改變。</p></article><article><span>C</span><h3>分析</h3><p>比較時間與空間成本，知道解法能不能應付輸入規模。</p></article><article><span>D</span><h3>練習</h3><p>用理解題與延伸題確認自己能辨認、解釋與應用。</p></article></div>
      </section>"""
    (ROOT / "index.html").write_text(shell(title="Python 資料結構與經典演算法", description="從基本資料結構到進階演算法的完整 Python 自學課程。", body=body, prefix="", active="course"), encoding="utf-8")


def build_phase_page(phase_number: int, units: list[dict]) -> None:
    phase = PHASES[phase_number]
    phase_units = [unit for unit in units if unit["phase"] == phase_number]
    total_lessons = sum(len(unit["lessons"]) for unit in phase_units)
    cards = "".join(unit_card(unit) for unit in phase_units)
    next_link = "phase-2.html" if phase_number == 1 else "index.html"
    next_label = "完成後前往第二階段" if phase_number == 1 else "回到完整課程地圖"
    body = f"""
      <section class="phase-hero phase-hero-{phase_number}">
        <div><a class="breadcrumb" href="index.html">PYTHON / LEARNING MAP</a><p class="eyebrow">{phase['range']}</p><h1>{phase['title']}</h1><p class="hero-intro">{phase['summary']}</p><div class="course-stats"><div><strong>{len(phase_units)}</strong><span>個單元</span></div><div><strong>{total_lessons}</strong><span>堂課</span></div><div><strong>{'FOUNDATION' if phase_number == 1 else 'ADVANCED'}</strong><span>學習層級</span></div></div></div>
        <aside><span>PHASE 0{phase_number}</span><h2>{esc(phase['goal'])}</h2></aside>
      </section>
      <section class="outline-section">
        <div class="section-head"><div><p class="section-index">01 / FULL OUTLINE</p><h2>單元與課程大綱</h2></div><p>每個單元先讀單元導覽，再按照課程編號前進。課程頁包含觀念、範例、程式碼、重點與練習。</p></div>
        <div class="unit-grid">{cards}</div>
      </section>
      <section class="phase-next"><p>完成這個階段之後</p><h2>{esc(phase['goal'])}</h2><a href="{next_link}">{next_label} <span>→</span></a></section>"""
    (ROOT / f"phase-{phase_number}.html").write_text(shell(title=phase["title"], description=phase["summary"], body=body, prefix="", active=f"phase{phase_number}"), encoding="utf-8")


def build_unit_page(unit: dict) -> None:
    lessons = "".join(f"""
        <article class="lesson-row">
          <span>{lesson['number']:02d}</span>
          <div><p>{esc(lesson['difficulty'])} · {esc(lesson['duration'])}</p><h3>{esc(lesson['title'])}</h3><b>{esc(lesson['subtitle'])}</b></div>
          <a href="../{lesson_href(unit, lesson)}" aria-label="開始課程：{esc(lesson['title'])}">開始閱讀 →</a>
        </article>""" for lesson in unit["lessons"])
    prereqs = "".join(f"<li>{esc(item)}</li>" for item in unit["prerequisites"])
    outcomes = "".join(f"<li>{esc(item)}</li>" for item in unit["outcomes"])
    body = f"""
      <section class="unit-hero">
        <div><a class="breadcrumb" href="../phase-{unit['phase']}.html">PHASE {unit['phase']:02d} / UNIT {unit['number']:02d}</a><p class="eyebrow">{esc(unit['english'])}</p><h1>{esc(unit['title'])}</h1><p class="hero-intro">{esc(unit['summary'])}</p><a class="primary-button" href="#lessons">查看 {len(unit['lessons'])} 堂課 <span>↓</span></a></div>
        <aside><span>UNIT</span><strong>{unit['number']:02d}</strong><p>{esc(unit['goal'])}</p></aside>
      </section>
      <section class="unit-info"><div><p class="section-index">BEFORE YOU START</p><h2>先備知識</h2><ul>{prereqs}</ul></div><div><p class="section-index">AFTER THIS UNIT</p><h2>完成後你能夠</h2><ul>{outcomes}</ul></div></section>
      <section class="lesson-section" id="lessons"><div class="section-head"><div><p class="section-index">LESSON LIST</p><h2>本單元課程</h2></div><p>建議依序閱讀；每一課約 15–25 分鐘，讀完後先回答理解題，再挑一題延伸練習。</p></div><div class="lesson-list">{lessons}</div></section>
      <nav class="bottom-nav"><a href="../phase-{unit['phase']}.html">← 返回第 {unit['phase']} 階段大綱</a><a href="../index.html">完整學習地圖 ↑</a></nav>"""
    output = ROOT / "units" / unit_filename(unit)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(shell(title=f"單元 {unit['number']:02d}｜{unit['title']}", description=unit["summary"], body=body, prefix="../", active=f"phase{unit['phase']}"), encoding="utf-8")


def render_section(section: dict, index: int) -> str:
    paragraphs = "".join(f"<p>{esc(text)}</p>" for text in section.get("paragraphs", []))
    bullets = ""
    if section.get("bullets"):
        bullets = "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in section["bullets"]) + "</ul>"
    table = ""
    if section.get("table"):
        headers = "".join(f"<th>{esc(item)}</th>" for item in section["table"]["headers"])
        rows = "".join("<tr>" + "".join(f"<td>{esc(cell)}</td>" for cell in row) + "</tr>" for row in section["table"]["rows"])
        table = f'<div class="table-wrap"><table><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table></div>'
    code = ""
    if section.get("code"):
        caption = f'<span>{esc(section.get("code_caption", "Python 3"))}</span>'
        code = f'<figure class="code-block"><figcaption>{caption}<button type="button" data-copy-code>複製</button></figcaption><pre><code>{esc(section["code"])}</code></pre></figure>'
    callout = f'<aside class="concept-callout"><b>KEY IDEA</b><p>{esc(section["callout"])}</p></aside>' if section.get("callout") else ""
    return f'<section class="content-section" id="section-{index}"><span class="content-index">{index:02d}</span><div><h2>{esc(section["heading"])}</h2>{paragraphs}{bullets}{table}{code}{callout}</div></section>'


def build_lesson_pages(units: list[dict]) -> None:
    all_lessons = [(unit, lesson) for unit in units for lesson in unit["lessons"]]
    for global_index, (unit, lesson) in enumerate(all_lessons):
        sections = "".join(render_section(section, index + 1) for index, section in enumerate(lesson["sections"]))
        objectives = "".join(f"<li>{esc(item)}</li>" for item in lesson["objectives"])
        takeaways = "".join(f"<li><span>{index:02d}</span>{esc(item)}</li>" for index, item in enumerate(lesson["takeaways"], 1))
        quiz = "".join(f'<details><summary>{esc(item["question"])}</summary><p>{esc(item["answer"])}</p></details>' for item in lesson["quiz"])
        practice = "".join(f"<li>{esc(item)}</li>" for item in lesson["practice"])
        previous = all_lessons[global_index - 1] if global_index > 0 else None
        following = all_lessons[global_index + 1] if global_index + 1 < len(all_lessons) else None
        previous_link = ""
        if previous:
            prev_unit, prev_lesson = previous
            previous_link = f'<a href="../unit-{prev_unit["number"]:02d}/{lesson_filename(prev_unit, prev_lesson)}"><span>← 上一課</span><b>{esc(prev_lesson["title"])}</b></a>'
        next_link = ""
        if following:
            next_unit, next_lesson = following
            next_link = f'<a class="next" href="../unit-{next_unit["number"]:02d}/{lesson_filename(next_unit, next_lesson)}"><span>下一課 →</span><b>{esc(next_lesson["title"])}</b></a>'
        body = f"""
      <article class="lesson-page">
        <header class="lesson-hero"><a class="breadcrumb" href="../../units/{unit_filename(unit)}">UNIT {unit['number']:02d} / LESSON {lesson['number']:02d}</a><p class="eyebrow">{esc(unit['english'])}</p><h1>{esc(lesson['title'])}</h1><p class="lesson-deck">{esc(lesson['subtitle'])}</p><div class="lesson-meta"><span>{esc(lesson['difficulty'])}</span><span>{esc(lesson['duration'])}</span><span>PYTHON 3</span></div></header>
        <section class="lesson-opening"><div><p class="section-index">WHY THIS MATTERS</p><p>{esc(lesson['summary'])}</p></div><div><p class="section-index">LEARNING GOALS</p><ul>{objectives}</ul></div></section>
        <div class="lesson-content">{sections}</div>
        <section class="takeaways"><p class="section-index">RECAP</p><h2>這堂課要帶走的事</h2><ol>{takeaways}</ol></section>
        <section class="quiz"><div><p class="section-index">CHECK YOURSELF</p><h2>先想一想，再看答案</h2></div><div>{quiz}</div></section>
        <section class="practice"><p class="section-index">PRACTICE</p><h2>延伸練習</h2><ol>{practice}</ol></section>
        <nav class="lesson-nav">{previous_link}{next_link}</nav>
      </article>"""
        output = ROOT / "lessons" / f"unit-{unit['number']:02d}" / lesson_filename(unit, lesson)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(shell(title=f"{unit['number']:02d}.{lesson['number']:02d} {lesson['title']}", description=lesson["summary"], body=body, prefix="../../", active=f"phase{unit['phase']}"), encoding="utf-8")


def main() -> None:
    units = load_units()
    expected = list(range(1, 17))
    actual = [unit["number"] for unit in units]
    if actual != expected:
        raise SystemExit(f"Expected units {expected}, found {actual}")
    build_topic_home(units)
    build_phase_page(1, units)
    build_phase_page(2, units)
    for unit in units:
        build_unit_page(unit)
    build_lesson_pages(units)
    print(f"Built {len(units)} units and {sum(len(unit['lessons']) for unit in units)} lessons.")


if __name__ == "__main__":
    main()
