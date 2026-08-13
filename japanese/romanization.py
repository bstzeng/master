"""Hepburn-style romanization for kana readings used by the course."""

from __future__ import annotations

import re


BASIC = {
    "あ": "a", "い": "i", "う": "u", "え": "e", "お": "o",
    "か": "ka", "き": "ki", "く": "ku", "け": "ke", "こ": "ko",
    "さ": "sa", "し": "shi", "す": "su", "せ": "se", "そ": "so",
    "た": "ta", "ち": "chi", "つ": "tsu", "て": "te", "と": "to",
    "な": "na", "に": "ni", "ぬ": "nu", "ね": "ne", "の": "no",
    "は": "ha", "ひ": "hi", "ふ": "fu", "へ": "he", "ほ": "ho",
    "ま": "ma", "み": "mi", "む": "mu", "め": "me", "も": "mo",
    "や": "ya", "ゆ": "yu", "よ": "yo",
    "ら": "ra", "り": "ri", "る": "ru", "れ": "re", "ろ": "ro",
    "わ": "wa", "ゐ": "i", "ゑ": "e", "を": "o", "ん": "n",
    "が": "ga", "ぎ": "gi", "ぐ": "gu", "げ": "ge", "ご": "go",
    "ざ": "za", "じ": "ji", "ず": "zu", "ぜ": "ze", "ぞ": "zo",
    "だ": "da", "ぢ": "ji", "づ": "zu", "で": "de", "ど": "do",
    "ば": "ba", "び": "bi", "ぶ": "bu", "べ": "be", "ぼ": "bo",
    "ぱ": "pa", "ぴ": "pi", "ぷ": "pu", "ぺ": "pe", "ぽ": "po",
    "ゔ": "vu", "ぁ": "a", "ぃ": "i", "ぅ": "u", "ぇ": "e", "ぉ": "o",
}

COMBOS = {
    "きゃ": "kya", "きゅ": "kyu", "きょ": "kyo",
    "しゃ": "sha", "しゅ": "shu", "しょ": "sho",
    "ちゃ": "cha", "ちゅ": "chu", "ちょ": "cho",
    "にゃ": "nya", "にゅ": "nyu", "にょ": "nyo",
    "ひゃ": "hya", "ひゅ": "hyu", "ひょ": "hyo",
    "みゃ": "mya", "みゅ": "myu", "みょ": "myo",
    "りゃ": "rya", "りゅ": "ryu", "りょ": "ryo",
    "ぎゃ": "gya", "ぎゅ": "gyu", "ぎょ": "gyo",
    "じゃ": "ja", "じゅ": "ju", "じょ": "jo",
    "びゃ": "bya", "びゅ": "byu", "びょ": "byo",
    "ぴゃ": "pya", "ぴゅ": "pyu", "ぴょ": "pyo",
    "ふぁ": "fa", "ふぃ": "fi", "ふぇ": "fe", "ふぉ": "fo",
    "うぃ": "wi", "うぇ": "we", "うぉ": "wo",
    "ゔぁ": "va", "ゔぃ": "vi", "ゔぇ": "ve", "ゔぉ": "vo",
    "しぇ": "she", "じぇ": "je", "ちぇ": "che",
    "てぃ": "ti", "でぃ": "di", "とぅ": "tu", "どぅ": "du",
    "つぁ": "tsa", "つぃ": "tsi", "つぇ": "tse", "つぉ": "tso",
}


def to_hiragana(text: str) -> str:
    output = []
    for character in text:
        codepoint = ord(character)
        if 0x30A1 <= codepoint <= 0x30F6:
            output.append(chr(codepoint - 0x60))
        else:
            output.append(character)
    return "".join(output)


def _last_vowel(output: list[str]) -> str:
    match = re.search(r"[aeiou](?!.*[aeiou])", "".join(output))
    return match.group(0) if match else ""


def _macronize(text: str) -> str:
    replacements = {"aa": "ā", "ii": "ī", "uu": "ū", "ee": "ē", "oo": "ō", "ou": "ō"}
    for source, target in replacements.items():
        text = re.sub(source, target, text)
    return text


def romanize(reading: str) -> str:
    text = to_hiragana(reading.strip())
    if text in {"こんにちは", "こんばんは"}:
        text = text[:-1] + "わ"
    output: list[str] = []
    index = 0
    geminate = False
    while index < len(text):
        character = text[index]
        if character == "っ":
            geminate = True
            index += 1
            continue
        if character == "ー":
            vowel = _last_vowel(output)
            if vowel:
                output.append(vowel)
            index += 1
            continue
        pair = text[index:index + 2]
        syllable = COMBOS.get(pair)
        width = 2 if syllable else 1
        if not syllable:
            syllable = BASIC.get(character)
        if syllable is None:
            output.append(character)
            index += 1
            continue
        if character == "ん":
            following = text[index + 1:index + 3]
            next_roman = COMBOS.get(following) or BASIC.get(text[index + 1:index + 2], "")
            if next_roman.startswith(("b", "m", "p")):
                syllable = "m"
            elif next_roman.startswith(("a", "i", "u", "e", "o", "y")):
                syllable = "n'"
        if geminate:
            if syllable.startswith("ch"):
                output.append("t")
            elif syllable and syllable[0] not in "aeioun":
                output.append(syllable[0])
            geminate = False
        output.append(syllable)
        index += width
    return _macronize("".join(output))
