"""Build narration + background music and a timeline for the tide video.

Input : script.json, tts_raw/cXX.mp3 (one clip per narration line, in order)
Output: build/audio.wav, build/timeline.json
Needs : ffmpeg, numpy
"""
import json, os, subprocess, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
SR = 44100

# kid-friendly voice: raise pitch slightly (asetrate) + speed up (atempo)
PITCH = 1.08
TEMPO = 1.34
LINE_GAP = 0.35      # seconds between lines
SEG_GAP = 0.9        # extra seconds between segments
HEAD = 1.2           # silence before first line
TAIL = 2.5           # after last line


def decode(path):
    af = f"asetrate={int(24000 * PITCH)},aresample={SR},atempo={TEMPO},loudnorm=I=-16:TP=-1.5"
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-af", af, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
        check=True, capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).copy()
    # trim leading/trailing near-silence
    idx = np.where(np.abs(x) > 0.01)[0]
    if len(idx):
        x = x[max(0, idx[0] - 800): idx[-1] + 2000]
    return x


def music(n):
    """Gentle pentatonic 'ukulele-ish' pluck loop + soft bass, very quiet."""
    t_beat = 0.42
    notes = [0, 4, 7, 9, 7, 4, 2, 4, 0, 4, 7, 12, 9, 7, 4, 2]   # semitones above C5
    bass = [0, 0, -5, -5, -3, -3, -7, -5]
    out = np.zeros(n, dtype=np.float32)
    total_beats = int(n / SR / t_beat) + 1

    def pluck(freq, dur, amp):
        m = int(dur * SR)
        tt = np.arange(m) / SR
        env = np.exp(-tt * 5.0) * np.minimum(1, tt * 200)
        s = (np.sin(2 * np.pi * freq * tt) + 0.35 * np.sin(4 * np.pi * freq * tt)
             + 0.15 * np.sin(6 * np.pi * freq * tt))
        return (amp * env * s).astype(np.float32)

    for b in range(total_beats):
        st = int(b * t_beat * SR)
        f = 523.25 * 2 ** (notes[b % len(notes)] / 12)
        p = pluck(f, 0.9, 0.05)
        e = min(n, st + len(p)); out[st:e] += p[: e - st]
        if b % 2 == 0:
            fb = 130.81 * 2 ** (bass[(b // 2) % len(bass)] / 12)
            p = pluck(fb, 1.2, 0.07)
            e = min(n, st + len(p)); out[st:e] += p[: e - st]
    # fade in/out
    fade = int(2 * SR)
    out[:fade] *= np.linspace(0, 1, fade)
    out[-fade:] *= np.linspace(1, 0, fade)
    return out


def main():
    os.makedirs(BUILD, exist_ok=True)
    script = json.load(open(os.path.join(HERE, "script.json"), encoding="utf-8"))
    clips, timeline = [], {"title": script["title"], "segments": []}
    t = HEAD
    k = 0
    for si, seg in enumerate(script["segments"]):
        if si > 0:
            t += SEG_GAP
        seg_start = max(0.0, t - (SEG_GAP / 2 if si > 0 else HEAD))
        pauses = seg.get("pause_after", [0] * len(seg["lines"]))
        lines = []
        for li, text in enumerate(seg["lines"]):
            x = decode(os.path.join(HERE, "tts_raw", f"c{k:02d}.mp3"))
            k += 1
            clips.append((t, x))
            d = len(x) / SR
            lines.append({"text": text, "start": round(t, 3), "end": round(t + d, 3),
                          "pause": pauses[li]})
            t += d + LINE_GAP + pauses[li]
        timeline["segments"].append({"id": seg["id"], "title": seg["title"],
                                     "start": round(seg_start, 3), "lines": lines})
    total = t + TAIL
    for i, s in enumerate(timeline["segments"]):
        s["end"] = timeline["segments"][i + 1]["start"] if i + 1 < len(timeline["segments"]) else round(total, 3)
    timeline["duration"] = round(total, 3)

    n = int(total * SR) + SR
    voice = np.zeros(n, dtype=np.float32)
    for st, x in clips:
        a = int(st * SR); voice[a:a + len(x)] += x
    # duck music under the voice
    env = np.convolve((np.abs(voice) > 0.02).astype(np.float32), np.ones(int(0.3 * SR)) / (0.3 * SR), "same")
    duck = 1.0 - 0.55 * np.clip(env * 3, 0, 1)
    mix = voice * 0.95 + music(n) * duck
    mix = np.clip(mix, -1, 1)
    pcm = (mix * 32767).astype(np.int16)
    with wave.open(os.path.join(BUILD, "audio.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    json.dump(timeline, open(os.path.join(BUILD, "timeline.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"duration {total:.1f}s, lines {k}")


if __name__ == "__main__":
    main()
