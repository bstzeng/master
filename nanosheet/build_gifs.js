// 用 Playwright 逐格繪製 anim.html 的場景，存成 PNG，再交給 encode_gif.py 合成 GIF
// 用法：node nanosheet/build_gifs.js [場景名稱...]
const path = require("path"), fs = require("fs"), { execFileSync } = require("child_process");
let chromium;
try { ({ chromium } = require("playwright")); } catch { ({ chromium } = require(path.join(execFileSync("npm", ["root", "-g"]).toString().trim(), "playwright"))); }
const FPS = 15;
(async () => {
  const dir = __dirname, out = path.join(dir, "gifs"), tmp = fs.mkdtempSync(path.join(require("os").tmpdir(), "nsgif-"));
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 800, height: 450 } });
  await page.goto("file://" + path.join(dir, "anim.html"));
  await page.evaluate(() => document.fonts.ready);
  const all = await page.evaluate(() => Object.keys(window.SCENES).map((k) => [k, window.SCENES[k].dur]));
  const wanted = process.argv.slice(2);
  for (const [name, dur] of all.filter(([n]) => !wanted.length || wanted.includes(n))) {
    const frames = Math.round(dur * FPS), fdir = path.join(tmp, name);
    fs.mkdirSync(fdir);
    for (let i = 0; i < frames; i++) {
      const url = await page.evaluate(([n, t]) => window.renderAt(n, t), [name, i / FPS]);
      fs.writeFileSync(path.join(fdir, String(i).padStart(4, "0") + ".png"), Buffer.from(url.split(",")[1], "base64"));
    }
    execFileSync("python3", [path.join(dir, "encode_gif.py"), fdir, path.join(out, name + ".gif"), String(FPS)], { stdio: "inherit" });
  }
  await browser.close();
  fs.rmSync(tmp, { recursive: true, force: true });
})();
