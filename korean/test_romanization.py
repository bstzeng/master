#!/usr/bin/env python3
"""Regression checks for the RR labels shown in the Korean course."""

from romanization import romanize


EXPECTED = {
    "ㅏ": "ㅏ",
    "아": "a",
    "한국": "hanguk",
    "한국어": "hangugeo",
    "국물": "gungmul",
    "신라": "silla",
    "설날": "seollal",
    "연락": "yeollak",
    "좋다": "jota",
    "학교": "hakgyo",
    "감사합니다": "gamsahamnida",
    "안녕하세요": "annyeonghaseyo",
    "기역": "giyeok",
    "쌍지읒": "ssangjieut",
    "가, 카, 까": "ga, ka, kka",
}

for korean, expected in EXPECTED.items():
    actual = romanize(korean)
    assert actual == expected, f"{korean}: expected {expected}, got {actual}"

print(f"Validated {len(EXPECTED)} representative RR labels.")
