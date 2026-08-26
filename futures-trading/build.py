#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the complete futures trading course as static HTML."""

from __future__ import annotations

import html
from pathlib import Path

from data.chapters_01_03 import CHAPTERS_01_03
from data.chapters_04_06 import CHAPTERS_04_06
from data.chapters_07_09 import CHAPTERS_07_09
from data.chapters_10_12 import CHAPTERS_10_12
from data.course import CHAPTERS, PHASES

ROOT = Path(__file__).resolve().parent
LESSONS = CHAPTERS_01_03 + CHAPTERS_04_06 + CHAPTERS_07_09 + CHAPTERS_10_12
META = {chapter["number"]: chapter for chapter in CHAPTERS}


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def shell(*, title, description, body, active="outline", image="assets/phase-1-contract.jpg"):
    image_url = f"https://bstzeng.github.io/master/futures-trading/{image}"
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
    <meta name="theme-color" content="#102b2a" />
    <meta property="og:title" content="{esc(title)}｜期貨交易入門" />
    <meta property="og:description" content="{esc(description)}" />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="{image_url}" />
    <meta name="twitter:card" content="summary_large_image" />
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
      <nav aria-label="期貨課程選單">
        <a class="{'is-active' if active == 'outline' else ''}" href="index.html">完整大綱</a>
        {nav(1, 3, 'chapter-01-futures-foundations.html', '01–03 合約')}
        {nav(4, 6, 'chapter-04-order-workflow.html', '04–06 操作')}
        {nav(7, 9, 'chapter-07-market-structure.html', '07–09 策略')}
        {nav(10, 11, 'chapter-10-risk-position-sizing.html', '10–11 風控')}
        {nav(12, 12, 'chapter-12-trade-lifecycle.html', '12 演練')}
      </nav>
      <span class="header-note">FUTURES / PAPER FIRST</span>
    </header>
    <main>{body}</main>
    <footer><span>MASTER / TOPIC 08</span><p>Risk first. Paper trade before capital.</p><span>© <b id="current-year"></b> PATRICK</span></footer>
    <dialog class="image-dialog" aria-label="放大圖片"><button type="button" aria-label="關閉圖片">×</button><img src="" alt="放大圖片預覽" /></dialog>
  </body>
</html>'''


def source_cards(sources):
    return "".join(
        f'<li><a href="{esc(source["url"])}" target="_blank" rel="noreferrer"><b>{esc(source["title"])}</b><span>{esc(source["note"])}</span></a></li>'
        for source in sources
    )


def chapter_card(chapter):
    tags = "".join(f"<li>{esc(topic)}</li>" for topic in chapter["topics"])
    return f'''<article class="chapter-card is-ready">
      <div class="chapter-card-head"><span>CHAPTER {chapter['number']:02d}</span><b>COMPLETE</b></div>
      <p>{esc(chapter['english'])}</p><h3>{esc(chapter['title'])}</h3><div class="chapter-summary">{esc(chapter['summary'])}</div>
      <ul>{tags}</ul><div class="chapter-foot"><span>{esc(chapter['duration'])}</span><a class="card-action" href="{esc(chapter['href'])}">閱讀完整第 {chapter['number']} 章 <span>→</span></a></div>
    </article>'''


def build_outline():
    phase_nav, phases = [], []
    for phase in PHASES:
        phase_nav.append(f'<a href="#phase-{phase["number"]}"><span>{phase["number"]:02d}</span>{esc(phase["title"])}</a>')
        cards = "".join(chapter_card(chapter) for chapter in CHAPTERS if chapter["phase"] == phase["number"])
        phases.append(f'''<section class="phase" id="phase-{phase['number']}">
          <div class="phase-head"><div><p class="section-index">PHASE {phase['number']:02d} / {esc(phase['english'])}</p><h2>{esc(phase['title'])}</h2></div><p>{esc(phase['summary'])}</p></div>
          <figure class="phase-banner"><img src="assets/{esc(phase['image'])}" alt="{esc(phase['title'])}階段概念圖" loading="lazy" /><figcaption>GPT 原創階段視覺｜精確數字與術語使用網頁大字呈現</figcaption></figure>
          <div class="chapter-grid">{cards}</div>
        </section>''')

    body = f'''
      <section class="outline-hero">
        <div class="outline-copy"><a class="breadcrumb" href="../index.html">MASTER / TOPIC 08</a><p class="eyebrow">FUTURES TRADING · COMPLETE FOUNDATION</p>
          <h1>先學會控制損失，<br /><em>再學習表達方向。</em></h1>
          <p class="hero-intro">一套給零基礎自學者的完整期貨課程：從契約、乘數、保證金、下單與多空計算，到市場狀態、做多／做空策略、部位風控、日誌與端到端紙上交易。每章是一頁完整長篇，不切成零散短頁。</p>
          <div class="course-stats"><div><strong>12 / 12</strong><span>完整大型章節</span></div><div><strong>96</strong><span>深度教學段落</span></div><div><strong>4</strong><span>下載練習模板</span></div></div>
          <a class="primary-button" href="chapter-01-futures-foundations.html">從期貨為何存在開始 <span>→</span></a>
        </div>
        <figure class="hero-image"><button class="zoom-image" type="button" data-image="assets/phase-1-contract.jpg" data-alt="標準化期貨契約與每日結算概念圖"><img src="assets/phase-1-contract.jpg" alt="標準化期貨契約與每日結算概念圖" /><span>點擊放大 ↗</span></button><figcaption>GPT 原創主視覺｜不在圖片塞入難讀小字</figcaption></figure>
      </section>
      <section class="risk-banner"><div><span>EDUCATION ONLY</span><h2>這是風險教育，不是獲利承諾。</h2></div><p>期貨有槓桿，損失可能超過最初存入的保證金。所有案例均為假設、所有操作先在模擬環境完成；規格、保證金、費用與制度交易前須查交易所及期貨商最新公告。只使用不影響生活、債務與家庭責任的風險資本。</p></section>
      <section class="course-contract"><p class="section-index">00 / COURSE METHOD</p><div><h2>一章一頁，從觀念走到可驗證作業。</h2><p>每章都包含核心模型、四格大字圖解、公式或決策框架、錯誤／紀律對照、四步作業、五題自我檢查與官方來源。</p></div><ol><li><span>01</span><b>先讀契約</b><p>知道每一點、每一口、每個月份真正代表什麼。</p></li><li><span>02</span><b>再寫風險</b><p>先定失效和金額，口數只能向下取整。</p></li><li><span>03</span><b>最後模擬</b><p>流程、成交、滑價與復盤全數留在資料裡。</p></li></ol></section>
      <nav class="phase-nav" aria-label="快速前往課程階段">{''.join(phase_nav)}</nav>
      <div class="full-outline">{''.join(phases)}</div>
      <section class="futures-lab" id="futures-lab"><div><p class="section-index">QUICK LAB / P&amp;L ESTIMATE</p><h2>先把點數換成帳戶金額。</h2><p>這是教學估算器，不是期貨商對帳單。輸入假設進出價、乘數、方向、口數與完整來回成本，觀察多空公式如何改變淨損益。</p></div>
        <form class="futures-calculator"><label>方向<select id="calc-direction"><option value="long">做多：買進後賣出</option><option value="short">做空：賣出後買回</option></select></label><label>進場價<input id="calc-entry" type="number" step="0.01" value="20000" /></label><label>平倉價<input id="calc-exit" type="number" step="0.01" value="20050" /></label><label>每點乘數<input id="calc-multiplier" type="number" min="0" step="0.01" value="200" /></label><label>口數<input id="calc-contracts" type="number" min="1" step="1" value="1" /></label><label>完整來回成本<input id="calc-cost" type="number" min="0" step="1" value="500" /></label><output><span>假設淨損益</span><strong id="calc-result">—</strong><small id="calc-detail">教學估算，不含未輸入的成本與滑價</small></output></form>
      </section>
      <section class="resource-library"><div><p class="section-index">DOWNLOAD / PRACTICE KIT</p><h2>四份可直接使用的練習模板</h2><p>先用假設數字與模擬資料，所有動態規格都附來源與查閱日期。</p></div><div class="resource-grid"><a href="templates/contract-spec-card.md"><span>MD</span><b>契約規格卡</b><p>乘數、跳動、月份、到期、結算與官方來源。</p></a><a href="templates/risk-calculator.csv"><span>CSV</span><b>風險與口數表</b><p>單口風險、向下取整口數與壓力情境。</p></a><a href="templates/trade-plan.md"><span>MD</span><b>交易計畫</b><p>市場狀態、策略六欄、否決條件與熔斷。</p></a><a href="templates/trade-journal.csv"><span>CSV</span><b>交易日誌</b><p>成交、成本、R、過程評分與策略版本。</p></a></div></section>
      <section class="density-promise"><div><p class="section-index">READING ORDER</p><h2>依序學，不跳過風險。</h2></div><div class="density-list"><p>前三章建立契約與槓桿模型；第四至六章處理操作與多空；第七至九章才談策略；最後三章把口數、日誌與完整模擬閉環收好。</p><ul><li>8 個深度段落／章</li><li>4 格大字教學圖／段</li><li>1 組錯誤／紀律對照</li><li>4 步紙上作業</li><li>5 題可展開自我檢查</li><li>3–4 個官方延伸來源</li></ul><a href="chapter-01-futures-foundations.html">開始第一章 →</a></div></section>'''
    (ROOT / "index.html").write_text(shell(title="完整大綱", description="12章完整期貨入門課程：契約規格、保證金、下單、多空損益、策略、風控、日誌與紙上交易。", body=body), encoding="utf-8")


def render_section(section, index):
    cards = "".join(f'<article class="{esc(it.get("tone", ""))}"><span>{esc(it["label"])}</span><b>{esc(it["title"])}</b><p>{esc(it["text"])}</p></article>' for it in section["items"])
    formula = f'<pre class="formula-box"><code>{esc(section["formula"])}</code></pre>' if section.get("formula") else ""
    callout = f'<aside class="chapter-callout"><b>{esc(section["callout"]["title"])}</b><p>{esc(section["callout"]["text"])}</p></aside>' if section.get("callout") else ""
    return f'''<section class="lesson-part" id="part-{index}"><div class="part-label"><span>{index:02d}</span><p>CORE MODEL</p></div><h2>{esc(section['title'])}</h2><p>{esc(section['paragraphs'][0])}</p><p>{esc(section['paragraphs'][1])}</p>{formula}<div class="teaching-visual visual-flow" role="img" aria-label="{esc(section['title'])}">{cards}</div><p class="diagram-caption"><b>圖解｜{esc(section['toc'])}</b> 依序核對四個節點；任何一格無法回答，就先停止並補齊資料。</p>{callout}</section>'''


def build_chapter(lesson):
    meta = META[lesson["number"]]
    number = lesson["number"]
    toc = "".join(f'<li><a href="#part-{i}"><span>{i:02d}</span>{esc(section["toc"])}</a></li>' for i, section in enumerate(lesson["sections"], 1))
    parts = "".join(render_section(section, i) for i, section in enumerate(lesson["sections"], 1))
    steps = "".join(f'<li><span>{esc(step[0])}</span><p><b>{esc(step[1])}</b>{esc(step[2])}</p></li>' for step in lesson["assignment"]["steps"])
    questions = "".join(f'<details><summary>{esc(q["q"])}</summary><p>{esc(q["a"])}</p></details>' for q in lesson["questions"])
    recap = "".join(f'<article><span>{i:02d}</span><p>{esc(text)}</p></article>' for i, text in enumerate(lesson["recap"], 1))
    workshop = lesson["workshop"]
    decision_cards = "".join(
        f'<li><span>{i:02d}</span><p><b>判斷題</b>{esc(text)}請用一個假設數字或一項官方資料證明你已完成，而不是只勾選「知道」。</p></li>'
        for i, text in enumerate(lesson["recap"], 1)
    )
    previous = CHAPTERS[number - 2] if number > 1 else None
    next_chapter = CHAPTERS[number] if number < 12 else None
    previous_link = f'<a href="{esc(previous["href"])}"><span>← PREVIOUS CHAPTER</span><b>{esc(previous["title"])}</b></a>' if previous else '<a href="index.html"><span>← COURSE OUTLINE</span><b>回到完整大綱</b></a>'
    next_link = f'<a class="next" href="{esc(next_chapter["href"])}"><small>NEXT CHAPTER →</small><b>{esc(next_chapter["title"])}</b><i>繼續依序閱讀</i></a>' if next_chapter else '<a class="next" href="index.html"><small>COURSE COMPLETE →</small><b>回到完整大綱</b><i>開始 30 筆模擬協議</i></a>'

    body = f'''
      <article class="chapter-page">
        <header class="chapter-hero"><div class="chapter-hero-copy"><a class="breadcrumb" href="index.html">COURSE OUTLINE / CHAPTER {number:02d}</a><p class="eyebrow">{esc(meta['english'])}</p><h1>{esc(meta['title'])}</h1><p class="chapter-deck">{esc(lesson['deck'])}</p><div class="chapter-meta"><span>{esc(meta['duration'])}</span><span>8 個完整段落</span><span>公式＋案例＋作業</span><span>先模擬</span></div></div><figure class="chapter-cover"><button class="zoom-image" type="button" data-image="assets/{esc(lesson['image'])}" data-alt="{esc(lesson['image_alt'])}"><img src="assets/{esc(lesson['image'])}" alt="{esc(lesson['image_alt'])}" /><span>點擊放大 ↗</span></button><figcaption>GPT 原創概念圖｜{esc(lesson['image_caption'])}</figcaption></figure></header>
        <section class="chapter-opening"><div><p class="section-index">LEARNING OUTCOME</p><p>{esc(lesson['learning'])}</p></div><div><p class="section-index">RISK BOUNDARY</p><p>{esc(lesson['boundary'])}</p></div></section>
        <div class="education-strip"><b>模擬優先</b><span>案例為假設，不是即時交易建議</span><span>停損不保證成交價</span><span>損失可能超過初始保證金</span></div>
        <div class="chapter-layout"><aside class="chapter-toc"><p>本章內容</p><ol>{toc}</ol><a href="#decision-lab">前往紙上決策 ↓</a></aside><div class="chapter-content">{parts}</div></div>
        <section class="decision-lab" id="decision-lab"><div class="decision-copy"><p class="section-index">DECISION REHEARSAL</p><h2>把第 {number} 章變成一次紙上決策</h2><p>先遮住事後價格，只使用當時可取得的規格、報價與帳戶資料。建立兩條路徑：第一條假設所有必要證據完整，寫出你會如何限制曝險；第二條故意放入一個資料缺漏、風險超限或操作異常，練習在真正損失出現前否決交易。</p><div class="scenario-pair"><article><span>PATH A / QUALIFY</span><b>條件通過也不能省略風控</b><p>以「{esc(meta['title'])}」為題，使用本章公式或流程做一次完整模擬。方向看對不是通過條件；規格、口數、委託、退出與紀錄全部可驗證，才算完成。</p></article><article><span>PATH B / VETO</span><b>練習主動取消</b><p>假設關鍵資料過時、合理口數為零、流動性突然下降，或人的狀態不合格。請明確寫出停止在哪一關、如何處理既有委託，以及何種新證據出現後才可重新評估。</p></article></div></div><ol>{decision_cards}</ol></section>
        <section class="optimization-workshop" id="workshop"><div><p class="section-index">IMPULSE / DISCIPLINE</p><h2>{esc(workshop['title'])}</h2></div><div class="workshop-grid"><article class="waste"><span>IMPULSIVE</span><p>{esc(workshop['before'])}</p></article><article class="optimized"><span>DISCIPLINED</span><p>{esc(workshop['after'])}</p></article><article class="result"><span>WHY IT MATTERS</span><p>{esc(workshop['result'])}</p></article></div></section>
        <section class="assignment" id="assignment"><div><p class="section-index">PAPER-TRADE ASSIGNMENT</p><h2>{esc(lesson['assignment']['title'])}</h2><p>{esc(lesson['assignment']['intro'])}</p></div><ol>{steps}</ol></section>
        <section class="self-check"><div><p class="section-index">CHECK YOUR MODEL</p><h2>先回答，再展開。</h2></div><div>{questions}</div></section>
        <section class="chapter-recap"><p class="section-index">CHAPTER {number:02d} / RECAP</p><h2>{esc(lesson['recap_title'])}</h2><div>{recap}</div></section>
        <section class="sources"><div><p class="section-index">OFFICIAL REFERENCES</p><h2>本章延伸閱讀</h2><p>制度、契約、保證金與時段會改變。交易前請回到交易所、監管機構與自己的期貨商，重新核對最新資訊。</p></div><ul>{source_cards(lesson['sources'])}</ul></section>
        <section class="final-disclaimer"><b>重要聲明</b><p>本頁僅供教育與模擬練習，不構成投資建議、招攬或任何獲利保證。期貨屬高風險槓桿商品，可能快速損失全部資金，甚至超過最初存入金額。請依所在地規範諮詢合格專業人士。</p></section>
        <nav class="chapter-nav">{previous_link}{next_link}</nav>
      </article>'''
    (ROOT / meta["href"]).write_text(shell(title=f'{number:02d}｜{meta["title"]}', description=meta["summary"], body=body, active=f"chapter-{number}", image=f'assets/{lesson["image"]}'), encoding="utf-8")


def main():
    if len(LESSONS) != 12:
        raise SystemExit(f"Expected 12 lessons, got {len(LESSONS)}")
    build_outline()
    for lesson in LESSONS:
        if len(lesson["sections"]) != 8:
            raise SystemExit(f"Chapter {lesson['number']} must have 8 sections")
        build_chapter(lesson)
    print("Built futures course: outline + 12 long chapters.")


if __name__ == "__main__":
    main()
