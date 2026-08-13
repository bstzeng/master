# MASTER

Patrick 的個人學習知識庫，目前包含兩個主題：

- 「Python 資料結構與經典演算法」：兩階段、16 個單元與 131 堂獨立課程。
- 「零基礎韓文」：五階段完整大綱；第一階段 6 個單元與 29 堂獨立課程已完成，支援點擊韓文發音。

## 頁面

- `index.html`：主題總覽
- `python/index.html`：Python 課程總覽
- `python/phase-1.html`、`python/phase-2.html`：兩階段大綱
- `python/units/`：16 個單元首頁
- `python/lessons/`：各單元的獨立課程頁
- `korean/index.html`：零基礎韓文課程首頁
- `korean/outline.html`：五階段、26 單元完整大綱
- `korean/phase-1.html`：第一階段大綱
- `korean/units/`：第一階段 6 個單元首頁
- `korean/lessons/`：第一階段 29 堂獨立課程頁

## 內容維護

- `python/data/unit-XX.json`：課程內容來源
- `python/validate.py`：驗證 16 個單元的資料結構
- `python/build.py`：產生主題、階段、單元與課程頁
- `python/check_site.py`：檢查頁面結構與站內連結
- `korean/data/curriculum.json`：韓文完整大綱與第一階段課程內容
- `korean/validate.py`：驗證大綱、單元、課程與發音資料
- `korean/build.py`：產生韓文主題的所有靜態頁面
- `korean/generate_audio.py`：一次產生網站內建的韓文 MP3 發音
- `korean/audio/`：186 組內建韓文發音，不依賴裝置語音套件
- `korean/check_site.py`：檢查韓文頁面結構、發音按鈕與站內連結

修改內容後執行：

```bash
python3 python/validate.py
python3 python/build.py
python3 python/check_site.py
python3 korean/validate.py
python3 korean/build.py
python3 korean/check_site.py
```

需要重建韓文音檔時，先安裝 `korean/requirements-audio.txt`，再執行：

```bash
python3 korean/generate_audio.py
```

## 本機預覽

```bash
python3 -m http.server 8000
```

前往 <http://localhost:8000/master-site/>。
