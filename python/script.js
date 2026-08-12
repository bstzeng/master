document.querySelectorAll("[data-copy-code]").forEach((button) => {
  button.addEventListener("click", async () => {
    const code = button.closest("figure")?.querySelector("code")?.textContent;
    if (!code) return;
    try {
      await navigator.clipboard.writeText(code);
      button.textContent = "已複製";
      window.setTimeout(() => { button.textContent = "複製"; }, 1500);
    } catch {
      button.textContent = "請手動選取";
    }
  });
});
