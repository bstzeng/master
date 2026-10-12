// 在瀏覽器（開啟 https://translate.google.com 分頁）的 DevTools Console 執行。
// 依 script.json 的旁白逐句產生 zh-TW TTS，打包成 tide_tts_clips.json 下載。
// 之後執行： python build_audio.py --clips tide_tts_clips.json
// （本專案已附上解開後的 tts_raw/cXX.mp3，可直接跳過此步驟。）
(async () => {
  const script = await (await fetch(prompt('script.json 的網址（或先貼上內容到變數 SCRIPT）') || '')).json()
    .catch(() => window.SCRIPT);
  const lines = script.segments.flatMap(s => s.lines);
  const out = [];
  for (let i = 0; i < lines.length; i++) {
    const url = 'https://translate.google.com/translate_tts?ie=UTF-8&tl=zh-TW&client=tw-ob&q=' +
      encodeURIComponent(lines[i]);
    const r = await fetch(url);
    if (r.status !== 200) throw new Error(`clip ${i} failed: ${r.status}`);
    const b = new Uint8Array(await r.arrayBuffer());
    let s = '';
    for (let j = 0; j < b.length; j += 8192) s += String.fromCharCode.apply(null, b.subarray(j, j + 8192));
    out.push(btoa(s));
    await new Promise(z => setTimeout(z, 300));
  }
  const blob = new Blob([JSON.stringify(out)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'tide_tts_clips.json';
  a.click();
  console.log('done', out.length);
})();
