const year = document.querySelector("#current-year");
if (year) year.textContent = new Date().getFullYear();

const progress = document.querySelector(".reading-progress span");
const updateProgress = () => {
  if (!progress) return;
  const scrollable = document.documentElement.scrollHeight - window.innerHeight;
  const ratio = scrollable > 0 ? Math.min(1, window.scrollY / scrollable) : 0;
  progress.style.width = `${ratio * 100}%`;
};

updateProgress();
window.addEventListener("scroll", updateProgress, { passive: true });
