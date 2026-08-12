# MASTER

Patrick 的個人學習知識庫。第一個完整主題是「Python 資料結構與經典演算法」，包含兩階段、16 個單元與 131 堂獨立課程。

## 頁面

- `index.html`：主題總覽
- `python/index.html`：Python 課程總覽
- `python/phase-1.html`、`python/phase-2.html`：兩階段大綱
- `python/units/`：16 個單元首頁
- `python/lessons/`：各單元的獨立課程頁

## 內容維護

- `python/data/unit-XX.json`：課程內容來源
- `python/validate.py`：驗證 16 個單元的資料結構
- `python/build.py`：產生主題、階段、單元與課程頁
- `python/check_site.py`：檢查頁面結構與站內連結

修改內容後執行：

```bash
python3 python/validate.py
python3 python/build.py
python3 python/check_site.py
```

## 本機預覽

```bash
python3 -m http.server 8000
```

前往 <http://localhost:8000/master-site/>。
