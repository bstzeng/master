const assert = require("node:assert/strict");

let clickHandler;
let lastAudio;
let speechCalls = 0;

const classNames = new Set();
const button = {
  dataset: {
    speak: "안녕하세요",
    audio: "../../audio/example.mp3",
    rate: "0.72",
  },
  classList: {
    add: (name) => classNames.add(name),
    remove: (name) => classNames.delete(name),
  },
};
const status = {
  textContent: "",
  classList: { add() {}, remove() {} },
};

global.window = {
  speechSynthesis: {
    getVoices: () => [],
    addEventListener() {},
    cancel() {},
    speak: () => { speechCalls += 1; },
  },
  clearTimeout,
  setTimeout,
};
global.document = {
  querySelector: () => status,
  querySelectorAll: () => [button],
  addEventListener: (name, handler) => {
    if (name === "click") clickHandler = handler;
  },
};
global.Audio = class {
  constructor(url) {
    this.url = url;
    this.currentTime = 0;
    lastAudio = this;
  }
  addEventListener() {}
  pause() {}
  play() {
    this.played = true;
    return Promise.resolve();
  }
};

require("./script.js");
clickHandler({ target: { closest: () => button } });

assert.equal(lastAudio.url, "../../audio/example.mp3");
assert.equal(lastAudio.playbackRate, 0.72);
assert.equal(lastAudio.preservesPitch, true);
assert.equal(lastAudio.played, true);
assert.equal(speechCalls, 0);
assert.equal(classNames.has("is-speaking"), true);
console.log("Bundled MP3 is used before the system voice fallback.");
