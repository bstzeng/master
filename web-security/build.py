#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the defensive web-security outline and completed large chapters."""

from __future__ import annotations

import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from data.course import CHAPTERS, PHASES, SOURCES  # noqa: E402
from data.chapter_02 import SOURCES as CHAPTER_02_SOURCES, body as chapter_02_body  # noqa: E402
from data.chapter_03 import SOURCES as CHAPTER_03_SOURCES, body as chapter_03_body  # noqa: E402


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def shell(*, title: str, description: str, body: str, prefix: str = "", active: str = "outline", image: str = "assets/og.png") -> str:
    image_url = f"https://bstzeng.github.io/master/web-security/{image}"
    return f'''<!doctype html>
<html lang="zh-Hant">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="{esc(description)}" />
    <meta name="theme-color" content="#0a1723" />
    <meta property="og:title" content="{esc(title)}｜網站攻擊與防禦" />
    <meta property="og:description" content="{esc(description)}" />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="{image_url}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{esc(title)}｜網站攻擊與防禦" />
    <meta name="twitter:description" content="{esc(description)}" />
    <meta name="twitter:image" content="{image_url}" />
    <title>{esc(title)}｜MASTER</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Noto+Sans+TC:wght@400;500;600;700&family=Noto+Serif+TC:wght@700;900&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="{prefix}styles.css" />
    <script src="{prefix}script.js" defer></script>
  </head>
  <body>
    <div class="reading-progress" aria-hidden="true"><span></span></div>
    <header class="site-header">
      <a class="brand" href="{prefix}../index.html" aria-label="回到 MASTER 首頁"><span class="brand-mark">M</span><span>MASTER</span></a>
      <nav aria-label="網站攻擊與防禦課程選單"><a class="{'is-active' if active == 'outline' else ''}" href="{prefix}index.html">完整大綱</a><a class="{'is-active' if active == 'chapter-1' else ''}" href="{prefix}chapter-01-attack-surface.html">01</a><a class="{'is-active' if active == 'chapter-2' else ''}" href="{prefix}chapter-02-http-request.html">02</a><a class="{'is-active' if active == 'chapter-3' else ''}" href="{prefix}chapter-03-information-exposure.html">03</a></nav>
      <span class="header-note">WEB SECURITY / DEFENDER'S VIEW</span>
    </header>
    <main>{body}</main>
    <footer><span>MASTER / TOPIC 06</span><p>Learn the attack. Build the defense.</p><span>© <b id="current-year"></b> PATRICK</span></footer>
    <dialog class="image-dialog" aria-label="放大圖片"><button type="button" aria-label="關閉圖片">×</button><img src="" alt="放大圖片預覽" /></dialog>
  </body>
</html>
'''


def chapter_card(chapter: dict) -> str:
    tags = "".join(f"<li>{esc(topic)}</li>" for topic in chapter["topics"])
    if chapter["ready"]:
        action = f'<a class="card-action" href="{chapter["href"]}">閱讀完整第 {chapter["number"]} 章 <span>→</span></a>'
        state = "is-ready"
        state_label = "AVAILABLE NOW"
    else:
        action = '<span class="card-action is-muted">依大綱順序製作</span>'
        state = ""
        state_label = "PLANNED"
    return f'''<article class="chapter-card {state}"><div class="chapter-card-head"><span>CHAPTER {chapter['number']:02d}</span><b>{state_label}</b></div><p>{esc(chapter['english'])}</p><h3>{esc(chapter['title'])}</h3><div class="chapter-summary">{esc(chapter['summary'])}</div><ul>{tags}</ul><div class="chapter-foot"><span>{esc(chapter['duration'])}</span>{action}</div></article>'''


def build_outline() -> None:
    phase_sections = []
    for phase in PHASES:
        cards = "".join(chapter_card(chapter) for chapter in CHAPTERS if chapter["number"] in phase["chapters"])
        phase_sections.append(f'''<section class="phase" id="phase-{phase['number']}"><div class="phase-head"><div><p class="section-index">PHASE {phase['number']:02d} / {esc(phase['english'])}</p><h2>{esc(phase['title'])}</h2></div><p>{esc(phase['summary'])}</p></div><div class="chapter-grid">{cards}</div></section>''')
    body = f'''
      <section class="outline-hero">
        <div class="outline-copy"><a class="breadcrumb" href="../index.html">MASTER / TOPIC 06</a><p class="eyebrow">WEB ATTACK & DEFENSE · DEFENDER-LED COURSE</p><h1>看懂攻擊路徑，<br /><em>才能守住自己的站。</em></h1><p class="hero-intro">從攻擊者視角理解網站，但所有操作只用在自己的系統或刻意建立的本機練習環境。這次不拆成大量短頁：全課程只有 12 個大型章節，每頁完成一個可以實際拿去保護網站的能力。</p><div class="course-stats"><div><strong>12</strong><span>大型章節</span></div><div><strong>50–120</strong><span>分鐘／章</span></div><div><strong>3</strong><span>章目前完成</span></div></div><a class="primary-button" href="chapter-01-attack-surface.html">從第一章開始 <span>→</span></a></div>
        <figure class="hero-image"><button class="zoom-image" type="button" data-image="assets/og.png" data-alt="網站攻擊與防禦的分層伺服器主視覺"><img src="assets/og.png" alt="網站攻擊與防禦的分層伺服器主視覺" /><span>點擊放大 ↗</span></button><figcaption>GPT 原創主視覺｜精確技術標示由網頁元件另外呈現</figcaption></figure>
      </section>
      <section class="course-contract"><p class="section-index">00 / COURSE CONTRACT</p><div><h2>學攻擊，是為了把防禦做對。</h2><p>課程會解釋攻擊成立條件、資料流與可觀察跡象；示範限制在本機練習程式，不提供對外部目標的掃描、入侵、繞過偵測或維持存取步驟。</p></div><ol><li><span>01</span><b>先畫系統</b><p>不知道資產與信任邊界，就不知道該守哪裡。</p></li><li><span>02</span><b>再理解失敗</b><p>追蹤輸入在哪一層失去控制，而不是只背漏洞名稱。</p></li><li><span>03</span><b>最後驗證防禦</b><p>以測試、日誌和檢查表確認修正真的生效。</p></li></ol></section>
      <nav class="phase-nav" aria-label="快速前往課程階段">{''.join(f'<a href="#phase-{phase["number"]}"><span>{phase["number"]:02d}</span>{esc(phase["title"])}</a>' for phase in PHASES)}</nav>
      <div class="full-outline">{''.join(phase_sections)}</div>
      <section class="density-promise"><div><p class="section-index">01 / NEW CONTENT STANDARD</p><h2>這次每一頁，<br />就是一整章。</h2></div><div class="density-list"><p>目前完成的三章都包含 8 個連續段落、大字程式化技術圖、1 張 GPT 原創插畫、實際範本、5 題測驗與可直接執行的自家網站作業。</p><ul><li>不再為每個小名詞拆頁</li><li>圖像服務理解，不只是裝飾</li><li>每個觀念都回到自家網站</li><li>來源、界線與可驗證結果並列</li></ul><a href="chapter-01-attack-surface.html">從第一章開始 →</a></div></section>'''
    (ROOT / "index.html").write_text(shell(title="網站攻擊與防禦｜完整大綱", description="12 個大型章節，從攻擊面、登入與經典網站漏洞學到部署、偵測與事件復原。", body=body), encoding="utf-8")


def build_chapter_one() -> None:
    source_cards = "".join(f'<li><a href="{esc(source["url"])}" target="_blank" rel="noreferrer"><b>{esc(source["title"])}</b><span>{esc(source["note"])}</span></a></li>' for source in SOURCES)
    body = f'''
      <article class="chapter-page">
        <header class="chapter-hero"><div class="chapter-hero-copy"><a class="breadcrumb" href="index.html">COURSE OUTLINE / CHAPTER 01</a><p class="eyebrow">MAP THE ATTACK SURFACE</p><h1>網站到底會從哪裡被攻擊</h1><p class="chapter-deck">先別急著學漏洞。第一步是把自己的網站畫完整：什麼東西有價值、外部能碰到哪裡、資料穿過哪些信任邊界，以及哪一個入口失守後會造成最大的連鎖影響。</p><div class="chapter-meta"><span>50–70 分鐘</span><span>8 個完整段落</span><span>防守者視角</span><span>無外部掃描</span></div></div><figure class="chapter-cover"><button class="zoom-image" type="button" data-image="assets/chapter-01-attack-surface.png" data-alt="網站攻擊面分層主視覺"><img src="assets/chapter-01-attack-surface.png" alt="網站攻擊面分層主視覺" /><span>點擊放大 ↗</span></button><figcaption>GPT 原創概念圖：攻擊路徑不只指向網頁，也會繞向控制面與資料層。</figcaption></figure></header>

        <section class="chapter-opening"><div><p class="section-index">LEARNING OUTCOME</p><p>完成本章後，你不只是知道「網站可能被駭」，而是能產出一張自己的攻擊面地圖、一份資產清單和一份優先改善順序。這三份成果會成為後續 11 章的共同底圖。</p></div><div><p class="section-index">SAFE PRACTICE BOUNDARY</p><p>本章只盤點你擁有或獲得明確授權的系統。不要對不屬於你的網域、IP 或服務進行掃描；公開可見不代表獲得測試授權。</p></div></section>

        <div class="chapter-layout">
          <aside class="chapter-toc"><p>本章內容</p><ol><li><a href="#part-1"><span>01</span>攻擊不是從漏洞名稱開始</a></li><li><a href="#part-2"><span>02</span>網站其實是一整條供應鏈</a></li><li><a href="#part-3"><span>03</span>攻擊面的精確定義</a></li><li><a href="#part-4"><span>04</span>攻擊者如何選擇路徑</a></li><li><a href="#part-5"><span>05</span>資料流與信任邊界</a></li><li><a href="#part-6"><span>06</span>建立第一份資產清單</a></li><li><a href="#part-7"><span>07</span>風險排序，不平均用力</a></li><li><a href="#part-8"><span>08</span>完成自己的攻擊面地圖</a></li></ol><a href="#assignment">前往本章作業 ↓</a></aside>

          <div class="chapter-content">
            <section class="lesson-part" id="part-1"><div class="part-label"><span>01</span><p>START WITH VALUE</p></div><h2>攻擊不是從漏洞名稱開始</h2><p>防守者很容易從「我要不要裝防火牆」開始，攻擊者卻通常先問另一組問題：這個系統有什麼值得取得？哪些入口從網際網路就能接觸？哪個帳號或服務一旦失守，可以接近更多資產？因此，資安的第一步不是背 SQL Injection、XSS 或 DDoS，而是理解價值、入口與權限之間的關係。</p><p>一個只有公開文章的靜態網站，可能沒有會員資料庫，卻仍有網域註冊商帳號、GitHub 帳號、部署 Token、DNS 設定與內容完整性需要保護。相反地，一個看似只有登入頁的內部工具，背後可能連著客戶資料、雲端儲存與寄信權限。畫面看起來簡單，不代表攻擊面很小。</p><div class="definition"><b>本章的工作定義</b><p><strong>資產</strong>是你不希望被看見、被改動、被中斷或被濫用的東西；<strong>入口</strong>是資料或命令進出系統的地方；<strong>信任邊界</strong>是資料跨過後必須重新驗證身分、權限或完整性的界線。</p></div><ul class="four-points"><li><b>機密性</b><span>哪些資料不能被未授權的人看到？</span></li><li><b>完整性</b><span>哪些內容、設定或紀錄不能被偷偷修改？</span></li><li><b>可用性</b><span>哪些服務中斷會讓網站失去主要功能？</span></li><li><b>濫用成本</b><span>哪些寄信、運算或儲存資源可能被拿去消耗？</span></li></ul></section>

            <section class="lesson-part" id="part-2"><div class="part-label"><span>02</span><p>SEE THE STACK</p></div><h2>網站不是一頁 HTML，而是一整條供應鏈</h2><p>使用者看到的是網頁，真正提供服務的卻是一串彼此依賴的元件：網域註冊商決定誰控制名稱；DNS 把名稱指向服務；CDN 或反向代理接收外部流量；應用程式處理登入與商業邏輯；資料庫、物件儲存和第三方 API 保存或傳遞價值；Git 平台和 CI/CD 則能直接改變正式環境。</p><p>攻擊者不需要從首頁突破。若部署 Token 外洩，他可能繞過應用程式直接發布內容；若網域帳號失守，他可能把流量導向另一台主機；若備份儲存桶公開，資料甚至不必經過網站程式就會外洩。攻擊面分析的目的，就是防止團隊只盯著最顯眼的前端。</p><div class="surface-map" role="img" aria-label="網站從網際網路、DNS、邊緣層、應用層、資料層到控制面的攻擊面示意圖"><div class="surface-source"><b>INTERNET</b><span>匿名訪客</span><span>已登入使用者</span><span>第三方服務</span></div><div class="surface-arrow">→</div><div class="surface-layers"><article><span>01</span><b>NAME</b><p>網域註冊商<br />DNS 記錄</p></article><article><span>02</span><b>EDGE</b><p>CDN／WAF<br />Reverse Proxy</p></article><article><span>03</span><b>APP</b><p>網站／API<br />登入與權限</p></article><article><span>04</span><b>DATA</b><p>資料庫<br />檔案／備份</p></article><article class="control"><span>05</span><b>CONTROL PLANE</b><p>Git／CI/CD／Cloud IAM／Secret</p></article></div></div><p class="diagram-caption"><b>圖 1｜網站攻擊面分層</b> 橘色代表外部可接觸面，綠色代表必須設計驗證與隔離的防禦控制。控制面雖不一定對一般訪客公開，失守後的影響通常更大。</p></section>

            <section class="lesson-part" id="part-3"><div class="part-label"><span>03</span><p>DEFINE THE SURFACE</p></div><h2>攻擊面不只是公開網址</h2><p>OWASP 將應用程式攻擊面描述為所有資料與命令進出路徑、保護這些路徑的程式、系統使用的高價值資料，以及保護這些資料的控制。這個定義很重要，因為它把「入口」和「防守入口的程式」一起納入：登入頁本身是入口，驗證密碼、限制嘗試與記錄異常的程式也是攻擊面的一部分。</p><p>盤點時應同時看外部與內部。外部面包含公開網站、API、Webhook、寄信入口與檔案上傳；內部面可能包含管理後台、資料庫管理工具、監控介面、CI/CD、備份與員工帳號。內部不等於安全，只代表攻擊者通常需要先跨過另一個邊界。</p><div class="surface-formula"><div><span>DATA & COMMAND PATHS</span><b>所有進出路徑</b></div><i>＋</i><div><span>PROTECTIVE CODE</span><b>驗證與授權</b></div><i>＋</i><div><span>VALUABLE ASSETS</span><b>資料、金鑰、功能</b></div><i>＋</i><div><span>PROTECTIVE CONTROLS</span><b>加密、日誌、隔離</b></div></div><aside class="chapter-callout"><b>常見誤解</b><p>「沒有會員系統，所以沒什麼可被攻擊」並不成立。內容被竄改、網域被接管、部署金鑰外洩、網站被拿去散播惡意內容或服務被耗盡，都屬於實際安全風險。</p></aside></section>

            <section class="lesson-part" id="part-4"><div class="part-label"><span>04</span><p>FOLLOW THE PATH</p></div><h2>攻擊者會選阻力最小、價值足夠的路</h2><p>真實攻擊不一定沿著最戲劇化的路線發生。攻擊者會先利用公開資訊建立假設，再挑選成本低、可重複或影響大的入口。也許是沒有保護的管理頁，也許是重複使用的密碼，也可能是早已忘記的測試子網域。當第一個入口成功後，下一步通常是確認取得了什麼權限、能接近哪些其他資產，以及防守方是否會察覺。</p><p>防守課程學習這條路徑的目的，不是教你隱藏攻擊，而是把控制放到正確位置：減少不必要暴露、在每個信任邊界重新授權、限制單一帳號能造成的影響，並留下足以辨識異常的紀錄。只在入口擋一次，等於假設第一道門永遠不會失效。</p><div class="attack-chain" role="img" aria-label="攻擊假設到防守驗證的五階段流程"><article><span>01</span><b>DISCOVER</b><p>看見網域、功能、技術與外露入口</p><em>防守：減少不必要暴露</em></article><article><span>02</span><b>CHOOSE</b><p>比較價值、阻力、權限與可達性</p><em>防守：修補高影響路徑</em></article><article><span>03</span><b>TOUCH</b><p>讓輸入進入功能或身分流程</p><em>防守：驗證、限速、隔離</em></article><article><span>04</span><b>EXPAND</b><p>嘗試接近更多資料或控制面</p><em>防守：最小權限、分段</em></article><article><span>05</span><b>IMPACT</b><p>讀取、改動、中斷或濫用資源</p><em>防守：告警、復原、追蹤</em></article></div><p class="diagram-caption"><b>圖 2｜攻擊路徑與防守對位</b> 這是高階威脅模型，不是外部測試操作指南。你的任務是在每一步安排至少一個預防或偵測控制。</p></section>

            <section class="lesson-part" id="part-5"><div class="part-label"><span>05</span><p>DRAW THE TRUST BOUNDARIES</p></div><h2>資料每跨過一條界線，就重新問一次「憑什麼相信」</h2><p>信任邊界不是一面實體牆，而是不同信任程度相遇的位置。瀏覽器送來的欄位、Cookie 和 Header 都可被使用者控制；CDN 轉送的請求不能因來自內部 IP 就自動取得管理權限；應用程式讀寫資料庫時，也不應擁有建立新管理員或刪除所有備份的能力。</p><p>畫資料流圖時，至少標出外部實體、處理程序、資料儲存、資料流和信任邊界。OWASP 建議用這類模型回答四個問題：我們在做什麼、可能出什麼錯、要怎麼處理，以及是否做得夠好。圖不用漂亮，但必須能被更新和驗證。</p><div class="data-flow" role="img" aria-label="瀏覽器到網站資料庫和第三方服務的資料流與信任邊界"><div class="flow-node external"><span>UNTRUSTED</span><b>Browser</b><p>表單、Cookie、檔案、Header</p></div><div class="flow-line"><span>HTTPS REQUEST</span>→</div><div class="trust-zone"><span class="zone-label">TRUST BOUNDARY A</span><div class="flow-node edge"><b>Edge</b><p>TLS、限速、基礎過濾</p></div><div class="flow-line">→</div><div class="flow-node app"><b>Application</b><p>驗證、身分、授權、商業規則</p></div></div><div class="flow-line boundary"><span>LEAST PRIVILEGE</span>→</div><div class="trust-zone data-zone"><span class="zone-label">TRUST BOUNDARY B</span><div class="flow-node data"><b>Database</b><p>受限帳號與資料範圍</p></div><div class="flow-node third"><b>Third-party API</b><p>Webhook、寄信、付款</p></div></div></div><p class="diagram-caption"><b>圖 3｜資料流與信任邊界</b> 每個箭頭都要回答：誰能送、接收者如何驗證、允許做什麼、失敗如何記錄，以及權限最壞能擴張到哪裡。</p></section>

            <section class="lesson-part" id="part-6"><div class="part-label"><span>06</span><p>BUILD THE INVENTORY</p></div><h2>建立第一份資產清單：先求可用，再求完整</h2><p>資產清單不是採購表。除了伺服器與資料庫，還要記錄能改變系統的身分、金鑰、部署流程和第三方依賴。每項資產至少需要擁有者、用途、所在位置、外部可達性、保存資料、最高權限、備份方式和日誌位置。若沒有人知道誰負責，實務上就很難在異常時快速停用或復原。</p><p>第一次盤點不必找出數千個 Endpoint。先按功能分類：公開內容、登入、管理、資料輸入、檔案、API、營運介面、第三方連線和控制面。之後每增加新子網域、新服務、新 Webhook 或新部署金鑰，都把它視為攻擊面變更，觸發一次小型威脅檢查。</p><div class="inventory-wrap"><table><thead><tr><th>資產</th><th>價值／最壞影響</th><th>入口與角色</th><th>現有控制</th><th>缺口</th></tr></thead><tbody><tr><td><b>網域與 DNS</b><span>註冊商帳號</span></td><td>流量被導走、郵件冒用</td><td>管理後台<br />網域管理者</td><td>MFA、異動通知</td><td>復原聯絡人未確認</td></tr><tr><td><b>正式網站</b><span>Web／API</span></td><td>內容竄改、服務中斷</td><td>公開路由<br />匿名／會員</td><td>HTTPS、部署審核</td><td>安全 Header 未盤點</td></tr><tr><td><b>部署控制面</b><span>Git／CI/CD</span></td><td>直接改變正式環境</td><td>Git 帳號、Token<br />維護者</td><td>MFA、分支保護</td><td>Token 權限過大</td></tr><tr><td><b>資料與備份</b><span>DB／Object Storage</span></td><td>個資外洩、無法復原</td><td>應用帳號、管理員</td><td>私有網路、加密</td><td>未做還原演練</td></tr></tbody></table></div><p class="diagram-caption"><b>表 1｜最小可用資產清單</b> 範例內容只是提示，請以自己的架構替換；不要把真實密鑰、密碼或完整連線字串寫進課程筆記。</p></section>

            <section class="lesson-part" id="part-7"><div class="part-label"><span>07</span><p>PRIORITIZE THE RISK</p></div><h2>不要平均用力：先處理可達、權限大、影響高的路徑</h2><p>列出風險後，最常見的失敗是把每一項都標成「高」。排序不是假裝能精確預測攻擊機率，而是讓有限時間先處理最可能形成重大後果的路徑。對個人網站而言，可以先問四件事：外部是否直接可達？是否不需要身分或只需低權限？成功後能否碰到高價值資產？發生時你能否快速看見並復原？</p><p>NIST CSF 2.0 強調治理、識別、保護、偵測、回應與復原是同一套風險管理結果。這提醒我們：修補不是唯一答案。暫時關閉不需要的功能、縮小權限、增加告警、準備還原和接受某項低影響風險，都可能是合理回應，但必須由真正承擔後果的人知情決定。</p><div class="risk-board"><div class="risk-axis"><span>影響 ↑</span><span>可達性 →</span></div><article class="risk-low"><b>低優先</b><p>難以接觸、資料價值低，而且能快速復原。</p></article><article class="risk-watch"><b>需要監控</b><p>容易接觸但影響有限；用限速、日誌與資源上限控制。</p></article><article class="risk-fix"><b>優先修正</b><p>公開可達，且能直接接近資料、管理權或部署控制面。</p></article><article class="risk-plan"><b>復原計畫</b><p>不一定能完全避免，但中斷或外洩影響很高，必須演練應變。</p></article></div><aside class="chapter-callout"><b>實用決策</b><p>如果一個沒人使用的測試後台公開在網路上，最快的控制可能不是替它加十項防護，而是先關閉或限制來源。消除攻擊面通常比永久維護更多控制更可靠。</p></aside></section>

            <section class="lesson-part" id="part-8"><div class="part-label"><span>08</span><p>TURN THE MAP INTO ACTION</p></div><h2>完成自己的攻擊面地圖</h2><p>現在把前面的概念合在一起。選擇一個你確實擁有的網站，從使用者能看見的入口往後畫：網域由誰管理、DNS 指向哪裡、外部流量先到哪個服務、應用程式部署在哪裡、資料存放在哪裡、Git 和部署由哪些帳號控制、第三方服務能做什麼，以及日誌與備份放在哪裡。</p><p>每畫一個箭頭，就補上驗證方式與最壞權限；每畫一個資料儲存，就補上資料類型、擁有者與復原方式。最後圈出三條最需要先處理的路徑。這份圖不會一次完成，之後每章都會回來更新：登入章補身分風險、注入章補資料流、部署章補控制面，事件章則補告警與復原。</p><div class="completion-grid"><article><span>DELIVERABLE 01</span><h3>一張系統圖</h3><p>至少包含網域、Edge、應用、資料、第三方與控制面。</p></article><article><span>DELIVERABLE 02</span><h3>一份資產表</h3><p>記錄擁有者、價值、入口、角色、控制、日誌與備份。</p></article><article><span>DELIVERABLE 03</span><h3>三條優先路徑</h3><p>說明可達性、需要權限、最壞影響、偵測與復原能力。</p></article><article><span>DELIVERABLE 04</span><h3>一項今天能做的修正</h3><p>例如關閉廢棄入口、開啟 MFA、縮小 Token 或確認備份。</p></article></div></section>
          </div>
        </div>

        <section class="assignment" id="assignment"><div><p class="section-index">FIELD ASSIGNMENT</p><h2>用 30 分鐘盤點自己的網站</h2><p>這不是滲透測試，也不需要安全工具。只使用你自己的管理後台、架構設定和部署文件完成。</p></div><ol><li><span>00–05</span><p><b>列出資產</b>網域、Git、主機、資料、第三方服務、備份與擁有者。</p></li><li><span>05–15</span><p><b>畫資料流</b>從瀏覽器開始，用箭頭連到 Edge、App、Data 與第三方。</p></li><li><span>15–25</span><p><b>標信任邊界</b>每個箭頭寫下身分、授權、輸入驗證與最高權限。</p></li><li><span>25–30</span><p><b>選前三項</b>依外部可達性和最壞影響，挑出下一步改善順序。</p></li></ol></section>

        <section class="self-check"><div><p class="section-index">CHECK YOUR MODEL</p><h2>先回答，再展開。</h2></div><div><details><summary>沒有資料庫的靜態網站，還有攻擊面嗎？</summary><p>有。網域註冊商、DNS、Git 帳號、部署 Token、託管平台、內容完整性與服務可用性都是資產。攻擊者不一定需要突破應用程式。</p></details><details><summary>為什麼管理後台在內網仍要做權限控制？</summary><p>內網只是其中一道邊界。帳號遭冒用、代理設定錯誤或其他服務失守時，攻擊者可能已在內部；管理功能仍應驗證身分、授權並記錄操作。</p></details><details><summary>攻擊面越小，就一定完全安全嗎？</summary><p>不是。縮小攻擊面能減少需要防守與測試的路徑，但留下的入口仍可能有高影響漏洞；還需要安全設計、測試、偵測與復原。</p></details><details><summary>資產清單為什麼要包含 Git 與 CI/CD？</summary><p>因為控制程式碼和部署流程的帳號或 Token，可能繞過網站功能直接改變正式環境，屬於高影響控制面。</p></details><details><summary>什麼情況應先移除功能，而不是加更多防護？</summary><p>當功能沒有實際需求、很少維護或暴露的風險高時，關閉入口能直接消除一部分攻擊面，通常比長期維護多層控制可靠。</p></details></div></section>

        <section class="chapter-recap"><p class="section-index">CHAPTER 01 / RECAP</p><h2>真正的第一道防線，<br />是知道自己正在保護什麼。</h2><div><article><span>01</span><p>攻擊面包含所有進出路徑、保護路徑的程式、高價值資產與保護資產的控制。</p></article><article><span>02</span><p>網站攻擊面跨越網域、Edge、應用、資料、第三方與部署控制面。</p></article><article><span>03</span><p>資料每跨過信任邊界，都必須重新驗證身分、權限、完整性與最壞影響。</p></article><article><span>04</span><p>排序時先處理公開可達、權限需求低、後果大且難偵測復原的路徑。</p></article></div></section>

        <section class="sources"><div><p class="section-index">PRIMARY REFERENCES</p><h2>本章依據</h2><p>課程將官方框架轉成個人架站可執行的語言；來源用來支持攻擊面、威脅建模與風險管理方法。</p></div><ul>{source_cards}</ul></section>

        <nav class="chapter-nav"><a href="index.html"><span>← 回到</span><b>12 章完整大綱</b></a><a class="next" href="chapter-02-http-request.html"><small>NEXT CHAPTER →</small><b>網路與 HTTP 攻擊基礎</b><i>繼續閱讀</i></a></nav>
      </article>'''
    (ROOT / "chapter-01-attack-surface.html").write_text(shell(title="第一章｜網站到底會從哪裡被攻擊", description="從資產、入口、資料流、信任邊界與風險排序，完成自己的網站攻擊面地圖。", body=body, active="chapter-1", image="assets/chapter-01-attack-surface.png"), encoding="utf-8")


def render_source_cards(sources: list[dict]) -> str:
    return "".join(f'<li><a href="{esc(source["url"])}" target="_blank" rel="noreferrer"><b>{esc(source["title"])}</b><span>{esc(source["note"])}</span></a></li>' for source in sources)


def build_chapter_two() -> None:
    body = chapter_02_body(render_source_cards(CHAPTER_02_SOURCES))
    page = shell(title="第二章｜網路與 HTTP 攻擊基礎", description="沿著一次網站請求理解 DNS、TLS、HTTP、Proxy、Cookie 與 Session 的安全責任。", body=body, active="chapter-2", image="assets/chapter-02-http-request.png")
    (ROOT / "chapter-02-http-request.html").write_text(page, encoding="utf-8")


def build_chapter_three() -> None:
    body = chapter_03_body(render_source_cards(CHAPTER_03_SOURCES))
    page = shell(title="第三章｜情報蒐集與資訊外洩", description="從網域、前端程式、錯誤訊息、備份檔與 Git 歷史建立自己網站的公開暴露清單。", body=body, active="chapter-3", image="assets/chapter-03-information-exposure.png")
    (ROOT / "chapter-03-information-exposure.html").write_text(page, encoding="utf-8")


def main() -> None:
    build_outline()
    build_chapter_one()
    build_chapter_two()
    build_chapter_three()
    print("Built web-security outline and complete chapters 01–03.")


if __name__ == "__main__":
    main()
