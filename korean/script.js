const speechStatus = document.querySelector("[data-speech-status]");
const speechButtons = document.querySelectorAll("[data-speak]");
const synth = window.speechSynthesis;
let voices = [];
let statusTimer;
let currentUtterance;
let currentAudio;

function refreshVoices() {
  if (synth) voices = synth.getVoices();
}

function koreanVoice() {
  return voices.find((voice) => voice.lang.toLowerCase() === "ko-kr")
    || voices.find((voice) => voice.lang.toLowerCase().startsWith("ko"));
}

function showStatus(message) {
  if (!speechStatus) return;
  window.clearTimeout(statusTimer);
  speechStatus.textContent = message;
  speechStatus.classList.add("is-visible");
  statusTimer = window.setTimeout(() => speechStatus.classList.remove("is-visible"), 2400);
}

function stopSpeakingState() {
  speechButtons.forEach((button) => button.classList.remove("is-speaking"));
}

function stopPlayback() {
  if (currentAudio) {
    currentAudio.pause();
    currentAudio = null;
  }
  if (synth) synth.cancel();
  stopSpeakingState();
}

function fallbackToSystemVoice(button, text, rate) {
  if (!synth || typeof window.SpeechSynthesisUtterance === "undefined") {
    stopSpeakingState();
    showStatus("音檔載入失敗，請確認網路後重新整理頁面。");
    return;
  }

  currentUtterance = new SpeechSynthesisUtterance(text);
  currentUtterance.lang = "ko-KR";
  currentUtterance.rate = rate < 0.9 ? 0.62 : 0.84;
  const voice = koreanVoice();
  if (voice) currentUtterance.voice = voice;
  button.classList.add("is-speaking");
  currentUtterance.onend = stopSpeakingState;
  currentUtterance.onerror = () => {
    stopSpeakingState();
    showStatus("音檔載入失敗，請確認網路後重新整理頁面。");
  };
  synth.speak(currentUtterance);
}

function playBundledAudio(button, text, rate) {
  const audioUrl = button.dataset.audio;
  if (!audioUrl) {
    fallbackToSystemVoice(button, text, rate);
    return;
  }

  const audio = new Audio(audioUrl);
  currentAudio = audio;
  audio.preload = "auto";
  audio.playbackRate = rate;
  audio.preservesPitch = true;
  audio.webkitPreservesPitch = true;
  let usedFallback = false;
  const fallback = () => {
    if (usedFallback || currentAudio !== audio) return;
    usedFallback = true;
    currentAudio = null;
    fallbackToSystemVoice(button, text, rate);
  };
  audio.addEventListener("ended", () => {
    if (currentAudio === audio) currentAudio = null;
    stopSpeakingState();
  }, { once: true });
  audio.addEventListener("error", fallback, { once: true });
  button.classList.add("is-speaking");
  audio.play().catch(fallback);
  showStatus(`${rate < 0.9 ? "慢速" : "播放"}：${text}`);
}

if (synth) {
  refreshVoices();
  if (typeof synth.addEventListener === "function") {
    synth.addEventListener("voiceschanged", refreshVoices);
  } else {
    synth.onvoiceschanged = refreshVoices;
  }
}

document.addEventListener("click", (event) => {
  const button = event.target.closest("[data-speak]");
  if (!button) return;
  const text = button.dataset.speak?.trim();
  if (!text) return;
  const rate = Number(button.dataset.rate || "1");
  stopPlayback();
  playBundledAudio(button, text, rate);
});
