const speechStatus = document.querySelector("[data-speech-status]");
const speechButtons = document.querySelectorAll("[data-speak]");
const synth = window.speechSynthesis;
let voices = [];
let statusTimer;
let currentUtterance;

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
  if (!synth || typeof window.SpeechSynthesisUtterance === "undefined") {
    showStatus("這個瀏覽器目前無法播放語音，請改用 Safari、Chrome 或 Edge。");
    return;
  }

  synth.cancel();
  stopSpeakingState();
  currentUtterance = new SpeechSynthesisUtterance(text);
  currentUtterance.lang = "ko-KR";
  currentUtterance.rate = Number(button.dataset.rate || "0.84");
  const voice = koreanVoice();
  if (voice) currentUtterance.voice = voice;

  button.classList.add("is-speaking");
  currentUtterance.onend = stopSpeakingState;
  currentUtterance.onerror = () => {
    stopSpeakingState();
    showStatus("語音播放失敗，請確認裝置已安裝韓文語音。");
  };
  synth.speak(currentUtterance);
  showStatus(`${Number(currentUtterance.rate) < 0.8 ? "慢速" : "播放"}：${text}`);
});
