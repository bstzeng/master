# 潮汐大冒險（tides/）

給小朋友看的潮汐教學動畫影片，繁體中文旁白＋字幕，約 3 分 40 秒，1280×720、24fps MP4。
主持角色是海浪寶寶「浪浪」，配角有月亮姐姐、地球哥哥、太陽公公。

- `index.html`：影片播放頁（段落跳轉、海邊安全守則、旁白全文；網址加 `?t=秒數` 可直接跳到某個畫面）
- `tide_for_kids.mp4`：成品影片
- `outline.md`：分段大綱（每段畫面描述＋旁白）
- `script.json`：腳本來源（段落、畫面描述、每句旁白、問答停頓秒數）
- `tts_raw/cXX.mp3`：每句一個的原始 TTS 旁白（Google 翻譯 zh-TW 語音）
- `fetch_tts.js`：在瀏覽器 Console 產生 `tts_raw` 的腳本
- `build_audio.py`：旁白調速（×1.34）與微升音調（×1.08）、排時間軸、合成輕柔背景音樂 → `build/audio.wav`、`build/timeline.json`
- `render_video.py`：用 pycairo 逐格畫出所有角色與場景，再用 ffmpeg 與音軌合成 MP4
- `build/timeline.json`：每段、每句旁白的起訖秒數（字幕與動畫同步用）

## 段落

1. 開場（浪浪、月亮姐姐、地球哥哥登場）
2. 什麼是潮汐？（沙灘水位上升＝漲潮、下降＝退潮）
3. 月亮怎麼拉海水？（引力讓靠近月亮那側與對面各鼓起一個水包）
4. 為什麼一天兩次？（地球自轉經過兩個水包；每天晚約 50 分鐘）
5. 大潮與小潮（日月地一直線＝大潮，新月/滿月；直角＝小潮，上/下弦月）
6. 潮間帶的小生物（螃蟹、寄居蟹、海葵、海螺、藤壺；輕輕看、不帶走）
7. 海邊安全小守則（5 條）
8. 小問答複習（4 題，每題倒數 3 秒）
9. 結尾

## 重新產生

```bash
pip install pycairo numpy      # 另需 ffmpeg 與 Noto Sans CJK TC 字型
python build_audio.py          # tts_raw/*.mp3 + script.json -> build/audio.wav, build/timeline.json
python render_video.py         # -> tide_for_kids.mp4（約 2 分鐘）
python render_video.py --still 30 98   # 只輸出某幾秒的畫面到 build/still_XX.png 方便檢查
```

改旁白文字時，要先用 `fetch_tts.js` 重新產生 `tts_raw/`（每句一檔、順序與 `script.json` 相同）。
