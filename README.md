# MASTER

Patrick 的個人學習知識庫，目前包含三個主題：

- 「Python 資料結構與經典演算法」：兩階段、16 個單元與 131 堂獨立課程。
- 「零基礎韓文」：五階段、26 個單元與 143 堂獨立課程，支援中文、RR 羅馬拼音與網站內建發音。
- 「零基礎日文」：五階段、26 個單元與 143 堂獨立課程，支援中文、Hepburn 羅馬拼音與網站內建發音。

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
