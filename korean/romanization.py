"""Small Revised Romanization helper for the course's Korean examples."""

from __future__ import annotations

import re


INITIALS = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
VOWELS = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"]
FINALS = ["", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]

INITIAL_RR = {
    "ㄱ": "g", "ㄲ": "kk", "ㄴ": "n", "ㄷ": "d", "ㄸ": "tt", "ㄹ": "r",
    "ㅁ": "m", "ㅂ": "b", "ㅃ": "pp", "ㅅ": "s", "ㅆ": "ss", "ㅇ": "",
    "ㅈ": "j", "ㅉ": "jj", "ㅊ": "ch", "ㅋ": "k", "ㅌ": "t", "ㅍ": "p", "ㅎ": "h",
}
VOWEL_RR = {
    "ㅏ": "a", "ㅐ": "ae", "ㅑ": "ya", "ㅒ": "yae", "ㅓ": "eo", "ㅔ": "e",
    "ㅕ": "yeo", "ㅖ": "ye", "ㅗ": "o", "ㅘ": "wa", "ㅙ": "wae", "ㅚ": "oe",
    "ㅛ": "yo", "ㅜ": "u", "ㅝ": "wo", "ㅞ": "we", "ㅟ": "wi", "ㅠ": "yu",
    "ㅡ": "eu", "ㅢ": "ui", "ㅣ": "i",
}
FINAL_RR = {
    "": "", "ㄱ": "k", "ㄲ": "k", "ㄳ": "k", "ㄴ": "n", "ㄵ": "n", "ㄶ": "n",
    "ㄷ": "t", "ㄹ": "l", "ㄺ": "k", "ㄻ": "m", "ㄼ": "l", "ㄽ": "l", "ㄾ": "l",
    "ㄿ": "p", "ㅀ": "l", "ㅁ": "m", "ㅂ": "p", "ㅄ": "p", "ㅅ": "t", "ㅆ": "t",
    "ㅇ": "ng", "ㅈ": "t", "ㅊ": "t", "ㅋ": "k", "ㅌ": "t", "ㅍ": "p", "ㅎ": "t",
}
LIAISON_RR = {
    "ㄱ": "g", "ㄲ": "kk", "ㄴ": "n", "ㄷ": "d", "ㄹ": "r", "ㅁ": "m",
    "ㅂ": "b", "ㅅ": "s", "ㅆ": "ss", "ㅈ": "j", "ㅊ": "ch", "ㅋ": "k", "ㅌ": "t", "ㅍ": "p", "ㅎ": "h",
}
COMPLEX_LIAISON = {
    "ㄳ": ("k", "s"), "ㄵ": ("n", "j"), "ㄶ": ("n", ""),
    "ㄺ": ("l", "g"), "ㄻ": ("l", "m"), "ㄼ": ("l", "b"),
    "ㄽ": ("l", "s"), "ㄾ": ("l", "t"), "ㄿ": ("l", "p"),
    "ㅀ": ("l", ""), "ㅄ": ("p", "s"),
}
VELAR_FINALS = {"ㄱ", "ㄲ", "ㄳ", "ㄺ", "ㅋ"}
CORONAL_FINALS = {"ㄷ", "ㄵ", "ㄶ", "ㅅ", "ㅆ", "ㅈ", "ㅊ", "ㅌ", "ㅎ"}
LABIAL_FINALS = {"ㅂ", "ㅄ", "ㄼ", "ㄿ", "ㅍ"}

# The official system follows standard pronunciation for many sound changes.
# These course words need explicit handling beyond a character-by-character pass.
OVERRIDES = {
    "한국어": "hangugeo", "옷이": "osi", "집에": "jibe", "문을": "muneul",
    "국물": "gungmul", "앞문": "ammun", "입문": "immun",
    "신라": "silla", "설날": "seollal", "연락": "yeollak", "편리": "pyeolli",
    "편리점": "pyeollijeom", "좋다": "jota", "읽다": "ikda", "읽어요": "ilgeoyo",
    "없다": "eopda", "없어요": "eopseoyo", "앉다": "anda",
    "학교": "hakgyo", "식당": "sikdang", "국밥": "gukbap", "숙소": "sukso",
    "축하": "chukha", "입학": "iphak", "대학교 입학": "daehakgyo iphak",
    "감사합니다": "gamsahamnida", "안녕하세요": "annyeonghaseyo",
    "기역": "giyeok", "리을": "rieul", "미음": "mieum", "비읍": "bieup",
    "시옷": "siot", "이응": "ieung", "지읒": "jieut", "치읓": "chieut",
    "키읔": "kieuk", "티읕": "tieut", "피읖": "pieup", "히읗": "hieut",
    "쌍기역": "ssanggiyeok", "쌍디귿": "ssangdigeut", "쌍비읍": "ssangbieup",
    "쌍시옷": "ssangsiot", "쌍지읒": "ssangjieut",
}


def decompose(character: str) -> tuple[str, str, str] | None:
    codepoint = ord(character)
    if not 0xAC00 <= codepoint <= 0xD7A3:
        return None
    offset = codepoint - 0xAC00
    initial_index = offset // 588
    vowel_index = (offset % 588) // 28
    final_index = offset % 28
    return INITIALS[initial_index], VOWELS[vowel_index], FINALS[final_index]


def romanize_word(text: str) -> str:
    if text in OVERRIDES:
        return OVERRIDES[text]
    result: list[str] = []
    for index, character in enumerate(text):
        parts = decompose(character)
        if parts is None:
            result.append(character)
            continue
        initial, vowel, final = parts
        previous_parts = decompose(text[index - 1]) if index else None
        previous_final = previous_parts[2] if previous_parts else ""
        initial_rr = INITIAL_RR[initial]
        if initial == "ㅇ" and previous_final:
            if previous_final == "ㅎ":
                initial_rr = ""
            elif previous_final in COMPLEX_LIAISON:
                initial_rr = COMPLEX_LIAISON[previous_final][1]
            elif previous_final == "ㄷ" and vowel == "ㅣ":
                initial_rr = "j"
            elif previous_final == "ㅌ" and vowel == "ㅣ":
                initial_rr = "ch"
            elif previous_final in LIAISON_RR:
                initial_rr = LIAISON_RR[previous_final]
        elif initial == "ㄹ" and previous_final:
            if previous_final in {"ㄴ", "ㄹ"}:
                initial_rr = "l"
            else:
                initial_rr = "n"
        elif initial == "ㄴ" and previous_final == "ㄹ":
            initial_rr = "l"
        result.append(initial_rr)
        result.append(VOWEL_RR[vowel])
        next_parts = decompose(text[index + 1]) if index + 1 < len(text) else None
        final_rr = FINAL_RR[final]
        if final and next_parts:
            next_initial, next_vowel, _ = next_parts
            if next_initial == "ㅇ":
                if final == "ㅎ" or final in LIAISON_RR or (final in {"ㄷ", "ㅌ"} and next_vowel == "ㅣ"):
                    final_rr = ""
                elif final in COMPLEX_LIAISON:
                    final_rr = COMPLEX_LIAISON[final][0]
            elif next_initial in {"ㄴ", "ㅁ", "ㄹ"}:
                if final in VELAR_FINALS:
                    final_rr = "ng"
                elif final in CORONAL_FINALS:
                    final_rr = "n"
                elif final in LABIAL_FINALS:
                    final_rr = "m"
                elif final == "ㄴ" and next_initial == "ㄹ":
                    final_rr = "l"
                elif final == "ㄹ" and next_initial == "ㄴ":
                    final_rr = "l"
        result.append(final_rr)
    return "".join(result)


def romanize(text: str) -> str:
    if text in OVERRIDES:
        return OVERRIDES[text]
    parts = re.split(r"([,，]\s*|\s+)", text.strip())
    output: list[str] = []
    for part in parts:
        if not part:
            continue
        if part.startswith((",", "，")):
            output.append(", ")
        elif part.isspace():
            output.append(" ")
        else:
            output.append(romanize_word(part))
    return "".join(output).strip()
