#!/usr/bin/env python3
"""Build the complete static Tolkien legendarium course."""

from __future__ import annotations

import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from data.course import PHASES, all_sources, all_units  # noqa: E402


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def unit_file(current: dict) -> str:
    return f"unit-{current['number']:02d}-{current['slug']}.html"


def phase_for(number: int) -> dict:
    return next(phase for phase in PHASES if number in phase["units"])


def shell(*, title: str, description: str, body: str, prefix: str = "", active: str = "") -> str:
    nav = [
        ("course", "課程首頁", f"{prefix}index.html"),
        ("outline", "完整大綱", f"{prefix}outline.html"),
        ("sources", "文本與來源", f"{prefix}sources.html"),
    ]
    links = "".join(
        f'<a class="{"is-active" if key == active else ""}" href="{href}">{label}</a>'
        for key, label, href in nav
    )
    return f'''<!doctype html>
<html lang="zh-Hant">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="{esc(description)}" />
    <meta name="theme-color" content="#172018" />
    <meta property="og:title" content="{esc(title)}｜魔戒深度解說" />
    <meta property="og:description" content="{esc(description)}" />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="https://bstzeng.github.io/master/lotr/assets/og.png" />
    <meta name="twitter:card" content="summary_large_image" />
    <title>{esc(title)}｜MASTER</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=DM+Mono:wght@400;500&family=Noto+Sans+TC:wght@400;500;600;700&family=Noto+Serif+TC:wght@600;700;900&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="{prefix}styles.css" />
    <script src="{prefix}script.js" defer></script>
  </head>
  <body>
    <div class="reading-progress" aria-hidden="true"><span></span></div>
    <header class="site-header">
      <a class="brand" href="{prefix}../index.html" aria-label="回到 MASTER 首頁"><span class="brand-mark">M</span><span>MASTER</span></a>
      <nav aria-label="魔戒課程選單">{links}</nav>
      <span class="header-note">TOLKIEN / LEGENDARIUM STUDY</span>
    </header>
    <main>{body}</main>
    <footer><span>MASTER / TOPIC 05</span><p>Not all those who wander need the same reading order.</p><span>© <b id="current-year"></b> PATRICK</span></footer>
  </body>
</html>
'''


def journey_art() -> str:
    return '''<div class="journey-art" aria-hidden="true"><span class="sun"></span><span class="peak peak-a"></span><span class="peak peak-b"></span><span class="peak peak-c"></span><span class="road"></span><b>Ⅰ</b><b>Ⅱ</b><b>Ⅲ</b><b>Ⅳ</b><small>FROM THE MUSIC<br />TO THE GREY HAVENS</small></div>'''


def unit_card(current: dict, prefix: str = "") -> str:
    return f'''<article class="unit-card">
      <a href="{prefix}units/{unit_file(current)}" aria-label="閱讀單元 {current['number']:02d}：{esc(current['title'])}"></a>
      <div class="unit-card-top"><span>UNIT {current['number']:02d}</span><b>{esc(current['timeframe'])}</b></div>
      <p>{esc(current['english'])}</p><h3>{esc(current['title'])}</h3><div>{esc(current['subtitle'])}</div><i>進入完整教學 →</i>
    </article>'''


def build_home(units: list[dict]) -> None:
    phase_cards = []
    for phase in PHASES:
        phase_units = [current for current in units if current["phase"] == phase["number"]]
        names = "".join(
            f'<li><a href="units/{unit_file(current)}"><span>{current["number"]:02d}</span>{esc(current["title"])}</a></li>'
            for current in phase_units
        )
        phase_cards.append(
            f'''<article class="phase-card"><div class="phase-card-head"><span>PHASE {phase['number']:02d}</span><b>{esc(phase['era'])}</b></div><p>{esc(phase['english'])}</p><h3>{esc(phase['title'])}</h3><div>{esc(phase['summary'])}</div><ol>{names}</ol><a class="phase-link" href="phase-{phase['number']}.html">閱讀本階段 →</a></article>'''
        )
    body = f'''
      <section class="course-hero">
        <div class="course-hero-copy"><a class="breadcrumb" href="../index.html">MASTER / TOPIC 05</a><p class="eyebrow">A DEEP GUIDE TO TOLKIEN'S LEGENDARIUM</p><h1>從創世之歌，<br /><em>走到灰港岸。</em></h1><p class="hero-intro">依中土世界內部年代前進，完整讀懂《精靈寶鑽》《哈比人》《魔戒》與第四紀元；再以人物、權力、死亡、自然與影視改編重新串連六十個單元。</p><div class="course-stats"><div><strong>10</strong><span>個階段</span></div><div><strong>60</strong><span>個完整單元</span></div><div><strong>240</strong><span>個深度章節</span></div></div><div class="hero-actions"><a class="primary-button" href="phase-1.html">從第一單元開始 <span>→</span></a><a class="text-link" href="outline.html">查看完整大綱</a></div></div>
        {journey_art()}
      </section>
      <section class="spoiler-note"><span>SPOILER NOTICE</span><p>本課程以完整解析為目標，包含《精靈寶鑽》《哈比人》《魔戒》正文、附錄與影視改編的重要結局。第一次閱讀者可依單元 60 的建議調整順序。</p></section>
      <section class="reading-principles"><p class="section-index">00 / READING METHOD</p><div><h2>先分版本，<br />再談故事。</h2><p>托爾金的傳說體系歷經長期修訂，死後出版材料也包含不同階段。課程採三條原則保持清楚。</p></div><ol><li><span>01</span><b>原著為主</b><p>文本、附錄與書信各自標明用途。</p></li><li><span>02</span><b>保留差異</b><p>不把遺稿強行拼成唯一正史。</p></li><li><span>03</span><b>改編分層</b><p>電影與影集作為獨立版本比較。</p></li></ol></section>
      <section class="roadmap"><div class="section-head"><div><p class="section-index">01 / THE ROAD</p><h2>十階段學習地圖</h2></div><p>每個單元都是一頁完整教學，包含事件因果、人物動機、主題閱讀、前後連結、測驗、練習與來源。</p></div><div class="phase-grid">{''.join(phase_cards)}</div></section>
      <section class="citation-banner"><div><p class="section-index">02 / TEXT FIRST</p><h2>這不是角色百科，<br />而是一條因果之路。</h2></div><div><p>你會看見一個早期誓言如何穿過數千年，一次憐憫如何在計畫失效後改變結局，以及勝利為什麼必須包含告別。</p><a href="sources.html">閱讀文本層級與來源 →</a></div></section>'''
    (ROOT / "index.html").write_text(shell(title="魔戒深度解說", description="10 階段、60 個完整單元，從創世之歌讀到灰港岸與影視改編。", body=body, active="course"), encoding="utf-8")


def build_outline(units: list[dict]) -> None:
    sections = []
    for phase in PHASES:
        cards = "".join(unit_card(current) for current in units if current["phase"] == phase["number"])
        sections.append(f'''<section class="outline-phase" id="phase-{phase['number']}"><div class="outline-phase-head"><div><p class="section-index">PHASE {phase['number']:02d} / {esc(phase['range'])}</p><h2>{esc(phase['title'])}</h2><span>{esc(phase['english'])}</span></div><p><b>階段目標</b>{esc(phase['goal'])}</p></div><div class="unit-grid">{cards}</div></section>''')
    body = f'''<section class="simple-hero"><a class="breadcrumb" href="index.html">THE LEGENDARIUM / LEARNING MAP</a><p class="eyebrow">10 PHASES · 60 COMPLETE UNITS</p><h1>完整課程大綱</h1><p class="hero-intro">依內部年代從創世、第一紀元、第二紀元走到《哈比人》《魔戒》與第四紀元，再進入跨文本主題與影視改編。</p></section><nav class="era-nav" aria-label="快速前往階段">{''.join(f'<a href="#phase-{phase["number"]}"><span>{phase["number"]:02d}</span>{esc(phase["title"])}</a>' for phase in PHASES)}</nav><div class="full-outline">{''.join(sections)}</div><section class="page-next"><p>BEGIN AT THE BEGINNING</p><h2>先建立文本與版本地圖，後面的年代才不會彼此混淆。</h2><a href="phase-1.html">前往第一階段 →</a></section>'''
    (ROOT / "outline.html").write_text(shell(title="魔戒完整課程大綱", description="10 階段、60 單元的托爾金傳說體系完整學習地圖。", body=body, active="outline"), encoding="utf-8")


def build_phase_pages(units: list[dict]) -> None:
    numerals = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
    for phase in PHASES:
        phase_units = [current for current in units if current["phase"] == phase["number"]]
        cards = "".join(unit_card(current) for current in phase_units)
        if phase["number"] < 10:
            next_link = f'<a href="phase-{phase["number"] + 1}.html">前往第 {phase["number"] + 1} 階段 →</a>'
        else:
            next_link = '<a href="sources.html">回到文本與來源 →</a>'
        body = f'''<section class="phase-hero"><div><a class="breadcrumb" href="outline.html">THE LEGENDARIUM / PHASE {phase['number']:02d}</a><p class="eyebrow">{esc(phase['era'])}</p><h1>第 {phase['number']} 階段<br />{esc(phase['title'])}</h1><p class="hero-intro">{esc(phase['summary'])}</p><div class="course-stats"><div><strong>{len(phase_units)}</strong><span>個完整單元</span></div><div><strong>{phase_units[0]['number']:02d}</strong><span>起始單元</span></div><div><strong>{phase_units[-1]['number']:02d}</strong><span>完成單元</span></div></div></div><aside><span>PHASE</span><b>{numerals[phase['number'] - 1]}</b><small>{esc(phase['english'])}</small></aside></section><section class="phase-units"><div class="section-head"><div><p class="section-index">FULL UNITS</p><h2>本階段課程</h2></div><p>依序閱讀最能看見因果；也可以直接選擇人物或事件頁，再用「前後呼應」回到時間線。</p></div><div class="unit-grid">{cards}</div></section><section class="page-next"><p>PHASE {phase['number']:02d} GOAL</p><h2>{esc(phase['goal'])}</h2>{next_link}</section>'''
        (ROOT / f"phase-{phase['number']}.html").write_text(shell(title=f"第 {phase['number']} 階段｜{phase['title']}", description=phase["summary"], body=body, active="outline"), encoding="utf-8")


def section_html(section: dict, index: int) -> str:
    bullets = "".join(f"<li>{esc(point)}</li>" for point in section["points"])
    return f'''<section class="lesson-section" id="section-{index}"><span class="section-number">{index:02d}</span><div><h2>{esc(section['heading'])}</h2><p>{esc(section['body'])}</p><ul>{bullets}</ul><aside><b>深度閱讀</b><p>{esc(section['lens'])}</p></aside></div></section>'''


def build_unit_pages(units: list[dict]) -> None:
    output_dir = ROOT / "units"
    output_dir.mkdir(parents=True, exist_ok=True)
    for position, current in enumerate(units):
        phase = phase_for(current["number"])
        objectives = "".join(f"<li>{esc(item)}</li>" for item in current["objectives"])
        sections = "".join(section_html(section, index) for index, section in enumerate(current["sections"], 1))
        toc = "".join(f'<li><a href="#section-{index}"><span>{index:02d}</span>{esc(section["heading"])}</a></li>' for index, section in enumerate(current["sections"], 1))
        people = "".join(f'<article><h3>{esc(item["name"])}</h3><span>{esc(item["role"])}</span><p>{esc(item["arc"])}</p></article>' for item in current["characters"])
        connections = "".join(f'<li><span>{index:02d}</span><p>{esc(item)}</p></li>' for index, item in enumerate(current["connections"], 1))
        takeaways = "".join(f'<li><span>{index:02d}</span>{esc(item)}</li>' for index, item in enumerate(current["takeaways"], 1))
        quiz = "".join(f'<details><summary>{esc(question)}</summary><p>{esc(answer)}</p></details>' for question, answer in current["quiz"])
        sources = "".join(f'<li><a href="{esc(source["url"])}" target="_blank" rel="noreferrer"><b>{esc(source["title"])}</b><span>{esc(source["note"])}</span></a></li>' for source in current["sources"])
        previous = units[position - 1] if position else None
        following = units[position + 1] if position + 1 < len(units) else None
        previous_link = f'<a href="{unit_file(previous)}"><span>← 上一單元</span><b>{esc(previous["title"])}</b></a>' if previous else '<a href="../outline.html"><span>← 返回</span><b>完整課程大綱</b></a>'
        next_link = f'<a class="next" href="{unit_file(following)}"><span>下一單元 →</span><b>{esc(following["title"])}</b></a>' if following else '<a class="next" href="../index.html"><span>完成課程 →</span><b>回到主題首頁</b></a>'
        body = f'''<article class="unit-page"><header class="unit-hero"><div><a class="breadcrumb" href="../phase-{phase['number']}.html">PHASE {phase['number']:02d} / UNIT {current['number']:02d}</a><p class="eyebrow">{esc(current['english'])}</p><h1>{esc(current['title'])}</h1><p class="unit-deck">{esc(current['subtitle'])}</p><div class="unit-meta"><span>{esc(current['timeframe'])}</span><span>4 個深度章節</span><span>原著為主</span></div></div><aside><span>UNIT</span><b>{current['number']:02d}</b><small>{current['number']:02d} / 60</small></aside></header><section class="unit-opening"><div><p class="section-index">WHY THIS MATTERS</p><p>{esc(current['opening'])}</p></div><div><p class="section-index">LEARNING GOALS</p><ul>{objectives}</ul></div></section><div class="unit-body"><aside class="contents"><p>本頁章節</p><ol>{toc}</ol><a href="#practice">前往練習 ↓</a></aside><div class="unit-content">{sections}</div></div><section class="character-field"><div><p class="section-index">CHARACTERS & FORCES</p><h2>人物、勢力與轉變</h2></div><div class="character-grid">{people}</div></section><section class="connections"><div><p class="section-index">ECHOES ACROSS AGES</p><h2>前後呼應</h2></div><ol>{connections}</ol></section><section class="takeaways"><p class="section-index">RECAP</p><h2>這個單元要帶走的事</h2><ol>{takeaways}</ol></section><section class="quiz"><div><p class="section-index">CHECK YOURSELF</p><h2>先想一想，<br />再展開答案。</h2></div><div>{quiz}</div></section><section class="practice" id="practice"><p class="section-index">READING PRACTICE</p><h2>把劇情轉成分析</h2><p>{esc(current['practice'])}</p></section><section class="sources"><div><p class="section-index">SOURCES & FURTHER READING</p><h2>文本與資料來源</h2><p>課程以托爾金原著和官方文本資訊為主；遺稿版本與影視改編另行標示，不以單一版本抹平差異。</p></div><ul>{sources}</ul></section><nav class="unit-nav">{previous_link}{next_link}</nav></article>'''
        (output_dir / unit_file(current)).write_text(shell(title=f"單元 {current['number']:02d}｜{current['title']}", description=current["subtitle"], body=body, prefix="../", active="outline"), encoding="utf-8")


def build_sources() -> None:
    source_cards = "".join(f'<article><span>{index:02d}</span><div><h3><a href="{esc(source["url"])}" target="_blank" rel="noreferrer">{esc(source["title"])} ↗</a></h3><p>{esc(source["note"])}</p></div></article>' for index, source in enumerate(all_sources(), 1))
    body = f'''<section class="simple-hero"><a class="breadcrumb" href="index.html">THE LEGENDARIUM / SOURCES</a><p class="eyebrow">TEXT · VERSION · ADAPTATION</p><h1>文本層級與資料來源</h1><p class="hero-intro">這個世界不是一套由作者一次寫定的百科。先知道自己正在讀哪一層材料，才能誠實處理矛盾與改編。</p></section><section class="source-principles"><article><span>01</span><h2>生前出版核心</h2><p>《哈比人》《魔戒》及附錄是主要閱讀錨點；不同版本仍可能有作者修訂。</p></article><article><span>02</span><h2>死後整理作品</h2><p>《精靈寶鑽》由克里斯多福・托爾金整理出版，提供宏觀主線，也帶有編輯歷史。</p></article><article><span>03</span><h2>遺稿與多版本</h2><p>《未完的故事》《中土世界的歷史》等保留演變過程，矛盾是研究資料，不必強行消失。</p></article><article><span>04</span><h2>影視獨立分層</h2><p>電影與影集會壓縮、合併、重排和原創；可分析其藝術功能，但不能直接回填原著正史。</p></article></section><section class="source-library"><div class="section-head"><div><p class="section-index">SOURCE LIBRARY</p><h2>課程連結資料</h2></div><p>以 Tolkien Estate 的作者生平、書信、文本專文與作品資訊為骨架；改編單元另連官方節目或電影頁。</p></div><div>{source_cards}</div></section><section class="citation-banner"><div><p class="section-index">COPYRIGHT BOUNDARY</p><h2>用摘要與分析，<br />尊重原作文字。</h2></div><div><p>本站不重製官方地圖、插畫、字體、戒文、歌詩或長篇原文。人物與事件以教學摘要呈現，閱讀仍應回到合法出版的作品。</p><a href="outline.html">回到完整大綱 →</a></div></section>'''
    (ROOT / "sources.html").write_text(shell(title="文本層級與資料來源", description="魔戒深度解說的原著、遺稿、版本、改編與引用界線。", body=body, active="sources"), encoding="utf-8")


def main() -> None:
    units = all_units()
    build_home(units)
    build_outline(units)
    build_phase_pages(units)
    build_unit_pages(units)
    build_sources()
    print(f"Built Tolkien topic: {len(PHASES)} phases, {len(units)} complete unit pages.")


if __name__ == "__main__":
    main()
