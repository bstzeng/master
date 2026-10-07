// 等向性蝕刻種類課：用 Playwright 逐格繪製 isotropic-etch/anim3d.html（three.js，共用 nanosheet/vendor）的場景，存成 PNG，再交給 encode_gif.py 合成 GIF
// 用法：node isotropic-etch/build_gifs.js [--preview] [場景名稱...]
//   預設輸出 1080P（1920×1080）到 gifs/，給下載與簡報用
//   --preview 輸出 800×450 到 gifs/preview/，給網頁顯示用（檔案小、載入快）
const path = require("path"), fs = require("fs"), http = require("http"), os = require("os");
const { execFileSync } = require("child_process");
let chromium;
try { ({ chromium } = require("playwright")); } catch { ({ chromium } = require(path.join(execFileSync("npm", ["root", "-g"]).toString().trim(), "playwright"))); }
const PAGES = ["isotropic-etch/anim3d.html"];
const TYPES = { ".html": "text/html", ".js": "text/javascript", ".json": "application/json" };

(async () => {
  const args = process.argv.slice(2), preview = args.includes("--preview"), scale = preview ? 1 : 2.4;
  const dir = path.dirname(__dirname), out = path.join(__dirname, "gifs", preview ? "preview" : ""), tmp = fs.mkdtempSync(path.join(os.tmpdir(), "nsgif-"));
  fs.mkdirSync(out, { recursive: true });
  // ES module 不能從 file:// 載入，所以起一個只服務 repo 根目錄的本機伺服器（要讀到 ../nanosheet/vendor）
  const server = http.createServer((req, res) => {
    const file = path.join(dir, decodeURIComponent(req.url.split(/[?#]/)[0]));
    if (!file.startsWith(dir) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { "Content-Type": TYPES[path.extname(file)] || "application/octet-stream" });
    fs.createReadStream(file).pipe(res);
  }).listen(0, "127.0.0.1");
  await new Promise((r) => server.once("listening", r));
  const base = `http://127.0.0.1:${server.address().port}/`;

  const browser = await chromium.launch({ args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"] });
  const page = await browser.newPage({ viewport: { width: 800, height: 450 } });
  const wanted = args.filter((a) => !a.startsWith("--"));
  for (const p of PAGES) {
    await page.goto(`${base}${p}?scale=${scale}`);
    await page.waitForFunction(() => window.SCENES && window.renderAt);
    await page.evaluate(() => document.fonts.ready);
    const scenes = await page.evaluate(() => Object.keys(window.SCENES).map((k) => [k, window.SCENES[k].dur, window.SCENES[k].fps]));
    for (const [name, dur, fps] of scenes.filter(([n]) => !wanted.length || wanted.includes(n))) {
      const frames = Math.round(dur * fps), fdir = path.join(tmp, name);
      fs.mkdirSync(fdir);
      for (let i = 0; i < frames; i++) {
        const url = await page.evaluate(([n, t]) => window.renderAt(n, t), [name, i / fps]);
        fs.writeFileSync(path.join(fdir, String(i).padStart(4, "0") + ".png"), Buffer.from(url.split(",")[1], "base64"));
      }
      execFileSync("python3", [path.join(dir, "nanosheet", "encode_gif.py"), fdir, path.join(out, name + ".gif"), String(fps)], { stdio: "inherit" });
    }
  }
  await browser.close();
  server.close();
  fs.rmSync(tmp, { recursive: true, force: true });
})();
