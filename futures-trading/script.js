const year = document.querySelector("#current-year");
if (year) year.textContent = new Date().getFullYear();

const progressBar = document.querySelector(".reading-progress span");
const updateProgress = () => {
  if (!progressBar) return;
  const distance = document.documentElement.scrollHeight - window.innerHeight;
  const progress = distance > 0 ? (window.scrollY / distance) * 100 : 0;
  progressBar.style.width = `${Math.min(100, Math.max(0, progress))}%`;
};
window.addEventListener("scroll", updateProgress, { passive: true });
updateProgress();

const dialog = document.querySelector(".image-dialog");
if (dialog) {
  const dialogImage = dialog.querySelector("img");
  document.querySelectorAll(".zoom-image").forEach((button) => {
    button.addEventListener("click", () => {
      dialogImage.src = button.dataset.image;
      dialogImage.alt = button.dataset.alt || "放大圖片";
      dialog.showModal();
    });
  });
  dialog.querySelector("button").addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", (event) => { if (event.target === dialog) dialog.close(); });
}

const sections = [...document.querySelectorAll(".lesson-part[id]")];
const tocLinks = [...document.querySelectorAll(".chapter-toc a[href^='#part-']")];
if (sections.length && tocLinks.length && "IntersectionObserver" in window) {
  const linkById = new Map(tocLinks.map((link) => [link.hash.slice(1), link]));
  const observer = new IntersectionObserver((entries) => {
    const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
    if (!visible.length) return;
    tocLinks.forEach((link) => link.classList.remove("is-current"));
    linkById.get(visible[0].target.id)?.classList.add("is-current");
  }, { rootMargin: "-10% 0px -68%", threshold: 0 });
  sections.forEach((section) => observer.observe(section));
}

const calc = {
  direction: document.querySelector("#calc-direction"),
  entry: document.querySelector("#calc-entry"),
  exit: document.querySelector("#calc-exit"),
  multiplier: document.querySelector("#calc-multiplier"),
  contracts: document.querySelector("#calc-contracts"),
  cost: document.querySelector("#calc-cost"),
  result: document.querySelector("#calc-result"),
  detail: document.querySelector("#calc-detail"),
};

const updateCalculator = () => {
  if (!calc.result) return;
  const entry = Number(calc.entry.value) || 0;
  const exit = Number(calc.exit.value) || 0;
  const multiplier = Math.max(0, Number(calc.multiplier.value) || 0);
  const contracts = Math.max(1, Math.floor(Number(calc.contracts.value) || 1));
  const cost = Math.max(0, Number(calc.cost.value) || 0);
  const difference = calc.direction.value === "long" ? exit - entry : entry - exit;
  const gross = difference * multiplier * contracts;
  const net = gross - cost;
  calc.result.textContent = `${net < 0 ? "−" : "+"}NT$${new Intl.NumberFormat("zh-TW", { maximumFractionDigits: 2 }).format(Math.abs(net))}`;
  calc.detail.textContent = `毛損益 NT$${new Intl.NumberFormat("zh-TW", { maximumFractionDigits: 2 }).format(gross)}，扣除輸入成本 NT$${new Intl.NumberFormat("zh-TW").format(cost)}`;
  calc.result.closest("output").classList.toggle("is-loss", net < 0);
};

[calc.direction, calc.entry, calc.exit, calc.multiplier, calc.contracts, calc.cost].forEach((input) => {
  input?.addEventListener("input", updateCalculator);
  input?.addEventListener("change", updateCalculator);
});
updateCalculator();
