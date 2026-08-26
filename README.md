# MASTER

Patrick 的個人學習知識庫，目前包含八個主題：

- 「Python 資料結構與經典演算法」：兩階段、16 個單元與 131 堂獨立課程。
- 「零基礎韓文」：五階段、26 個單元與 143 堂獨立課程，支援中文、RR 羅馬拼音與網站內建發音。
- 「零基礎日文」：五階段、26 個單元與 143 堂獨立課程，支援中文、Hepburn 羅馬拼音與網站內建發音。
- 「星座學習地圖」：五階段、36 個完整單元，涵蓋星座起源、十二星座人格、關係互動、基礎星盤與科學思考。
- 「魔戒深度解說」：十階段、60 個完整單元，從創世與三大紀元讀到人物主題、影視改編與完整閱讀路線。
- 「網站攻擊與防禦」：五階段、12 個完整大型章節；以防守者視角理解網站攻擊面、經典漏洞、部署、偵測與復原。
- 「Agentic AI 省 Token」：五階段、12 個完整大型章節；從成本量測、Context 與工具迴圈，到模型路由、多 Agent、快取與正式環境治理。
- 「期貨交易入門」：五階段、12 個完整長篇章節；從契約、保證金與下單，到多空策略、部位風控、日誌與紙上交易。

## 頁面

- `index.html`：主題總覽
- `python/index.html`：Python 課程總覽
- `python/phase-1.html`、`python/phase-2.html`：兩階段大綱
- `python/units/`：16 個單元首頁
- `python/lessons/`：各單元的獨立課程頁
- `korean/index.html`：零基礎韓文課程首頁
- `korean/outline.html`：五階段、26 單元完整大綱
- `korean/alphabet.html`：21 個母音、19 個子音與 RR 羅馬拼音系統課
- `korean/phase-1.html`～`korean/phase-5.html`：五階段課程頁
- `korean/units/`：26 個單元首頁
- `korean/lessons/`：143 堂獨立課程頁
- `japanese/index.html`：零基礎日文課程首頁
- `japanese/outline.html`：五階段、26 單元完整大綱
- `japanese/kana.html`：46 個平假名、46 個片假名與 Hepburn 系統課
- `japanese/phase-1.html`～`japanese/phase-5.html`：五階段課程頁
- `japanese/units/`：26 個單元首頁
- `japanese/lessons/`：143 堂獨立課程頁
- `astrology/index.html`：星座學習地圖首頁
- `astrology/outline.html`：五階段、36 單元完整大綱
- `astrology/phase-1.html`～`astrology/phase-5.html`：五階段課程頁
- `astrology/units/`：36 個完整教學單元頁
- `astrology/sources.html`：歷史、天文、心理學資料來源與使用界線
- `lotr/index.html`：魔戒深度解說首頁
- `lotr/outline.html`：十階段、60 單元完整大綱
- `lotr/phase-1.html`～`lotr/phase-10.html`：十階段課程頁
- `lotr/units/`：60 個完整教學單元頁
- `lotr/sources.html`：文本層級、資料來源與改編界線
- `web-security/index.html`：網站攻擊與防禦的五階段、12 章完整大綱
- `web-security/chapter-01-attack-surface.html`：第一章「網站到底會從哪裡被攻擊」完整教學
- `web-security/chapter-02-http-request.html`：第二章「網路與 HTTP 攻擊基礎」完整教學
- `web-security/chapter-03-information-exposure.html`：第三章「情報蒐集與資訊外洩」完整教學
- `web-security/chapter-04-identity.html`～`chapter-12-incident-response.html`：登入、授權、注入、瀏覽器、檔案、API、部署、可用性與事件應變完整教學
- `agentic-ai-token/index.html`：Agentic AI 省 Token 的五階段、12 章完整大綱
- `agentic-ai-token/chapter-01-token-cost-map.html`～`chapter-12-production-playbook.html`：完整大型章節
- `futures-trading/index.html`：期貨交易入門的五階段、12 章完整大綱與損益估算器
- `futures-trading/chapter-01-futures-foundations.html`～`chapter-12-trade-lifecycle.html`：契約、操作、策略、風控與完整紙上交易
- `futures-trading/templates/`：契約規格卡、風險計算表、交易計畫與交易日誌

## 內容維護

- `python/data/unit-XX.json`：課程內容來源
- `python/validate.py`：驗證 16 個單元的資料結構
- `python/build.py`：產生主題、階段、單元與課程頁
- `python/check_site.py`：檢查頁面結構與站內連結
- `korean/data/curriculum.json`：韓文完整大綱與第一階段課程內容
- `korean/data/phase-2.json`～`korean/data/phase-5.json`：第二至第五階段課程內容
- `korean/data/alphabet.json`：韓文字母的系統分組、名稱與 RR 資料
- `korean/validate.py`：驗證大綱、單元、課程與發音資料
- `korean/build.py`：產生韓文主題的所有靜態頁面
- `korean/generate_audio.py`：一次產生網站內建的韓文 MP3 發音
- `korean/audio/`：網站內建韓文 MP3 發音，不依賴裝置語音套件
- `korean/check_site.py`：檢查韓文頁面結構、發音按鈕與站內連結
- `japanese/data/phase-X.json`：日文五階段課程內容
- `japanese/data/kana.json`：平假名、片假名與例詞資料
- `japanese/validate.py`：驗證假名、單元、課程與讀音資料
- `japanese/build.py`：產生日文主題的所有靜態頁面
- `japanese/generate_audio.py`：產生網站內建的日文 MP3
- `japanese/check_site.py`：檢查日文頁面、羅馬拼音、音檔與連結
- `astrology/data/`：星座課程的歷史、人格、關係與星盤內容
- `astrology/validate.py`：驗證五階段、36 單元與完整教學結構
- `astrology/build.py`：產生星座主題的所有靜態頁面
- `astrology/check_site.py`：檢查星座頁面結構與站內連結
- `lotr/data/`：魔戒課程的年代、人物、主題與改編內容
- `lotr/validate.py`：驗證十階段、60 單元與完整教學結構
- `lotr/build.py`：產生魔戒主題的所有靜態頁面
- `lotr/check_site.py`：檢查魔戒頁面結構與站內連結
- `web-security/data/course.py`：五階段、12 個大型章節與官方參考來源
- `web-security/data/chapter_02.py`、`chapter_03.py`：第二、三章完整內容與官方來源
- `web-security/data/chapters_04_06.py`～`chapters_10_12.py`：第四至十二章完整內容與官方來源
- `web-security/data/chapter_factory.py`：第四至十二章共用的大型章節頁面產生器
- `web-security/validate.py`：驗證課程大綱與章節狀態
- `web-security/build.py`：產生完整大綱與全部 12 章教學頁
- `web-security/check_site.py`：檢查章節密度、圖片、來源、metadata 與站內連結
- `agentic-ai-token/data/`：Agentic AI 省 Token 的完整章節內容與官方來源
- `agentic-ai-token/build.py`、`validate.py`、`check_site.py`：產生並檢查 12 個大型章節
- `futures-trading/data/`：期貨課程五階段、12 章內容與官方來源
- `futures-trading/build.py`：產生完整大綱與全部 12 個長篇章節
- `futures-trading/validate.py`：檢查每章 8 段、5 題與至少 5,000 可見字元
- `futures-trading/check_site.py`：檢查 13 個頁面的站內連結與圖片資產

修改內容後執行：

```bash
python3 python/validate.py
python3 python/build.py
python3 python/check_site.py
python3 korean/validate.py
python3 korean/build.py
python3 korean/check_site.py
python3 japanese/validate.py
python3 japanese/build.py
python3 japanese/check_site.py
python3 astrology/validate.py
python3 astrology/build.py
python3 astrology/check_site.py
python3 lotr/validate.py
python3 lotr/build.py
python3 lotr/check_site.py
python3 web-security/validate.py
python3 web-security/build.py
python3 web-security/check_site.py
python3 agentic-ai-token/build.py
python3 agentic-ai-token/validate.py
python3 agentic-ai-token/check_site.py
python3 futures-trading/build.py
python3 futures-trading/validate.py
python3 futures-trading/check_site.py
```

需要重建語言課程音檔時，先安裝該主題的 `requirements-audio.txt`，再執行：

```bash
python3 korean/generate_audio.py
python3 japanese/generate_audio.py
```

## 本機預覽

```bash
python3 -m http.server 8000
```

前往 <http://localhost:8000/master-site/>。
