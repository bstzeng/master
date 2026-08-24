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
  const closeButton = dialog.querySelector("button");

  document.querySelectorAll(".zoom-image").forEach((button) => {
    button.addEventListener("click", () => {
      dialogImage.src = button.dataset.image;
      dialogImage.alt = button.dataset.alt || "放大圖片";
      dialog.showModal();
    });
  });

  closeButton.addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) dialog.close();
  });
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
