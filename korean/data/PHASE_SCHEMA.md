# Korean phase data contract

Create exactly one JSON file containing an array of unit objects. Do not edit any other file.

## Unit shape

```json
{
  "number": 7,
  "slug": "numbers-floors-prices",
  "title": "數字、樓層與價格",
  "korean_title": "숫자·층·가격",
  "summary": "Traditional Chinese summary.",
  "goal": "Observable learner goal.",
  "prerequisites": ["...", "...", "..."],
  "outcomes": ["...", "...", "...", "..."],
  "lessons": []
}
```

## Lesson shape

Every lesson is a self-contained 15-minute page. Lesson numbers start at 1 in every unit and are consecutive.

```json
{
  "number": 1,
  "slug": "sino-korean-numbers",
  "title": "漢字數字 0–10",
  "subtitle": "Short Traditional Chinese deck.",
  "summary": "Why this lesson matters.",
  "objectives": ["...", "...", "..."],
  "sections": [
    {
      "heading": "...",
      "paragraphs": ["One concise Traditional Chinese teaching paragraph."],
      "bullets": ["...", "...", "..."],
      "audio": [
        {"text": "일", "meaning": "一"},
        {"text": "이", "meaning": "二", "note": "Optional note"}
      ],
      "callout": "Optional key idea"
    }
  ],
  "takeaways": ["...", "...", "..."],
  "quiz": [
    {"question": "...", "answer": "..."},
    {"question": "...", "answer": "..."}
  ],
  "practice": ["...", "..."]
}
```

## Exact requirements

- Exactly 3 sections per lesson.
- Each section has exactly 1 paragraph, 3 useful bullets, and 2–4 audio items.
- Exactly 3 takeaways, 2 quiz items, and 2 practice items per lesson.
- `text` is the Korean shown on the card. `speak` is optional and only differs when a symbol or abbreviated display needs a natural TTS target.
- `meaning` is concise Traditional Chinese. `note` is optional.
- Do not add romanization manually unless the official Revised Romanization cannot be inferred from the written Korean. The generator adds RR beside every Chinese meaning.
- Use natural, polite contemporary Korean. Prefer 해요체 for learner-facing conversation and include formal signs where the real context requires them.
- Explain literal structure before idiomatic Chinese when it prevents confusion.
- Keep lessons progressive and systematic. Each unit should begin with recognition/core pattern, then controlled examples, then a real-life reading or listening task.
- Avoid Roman-letter-only audio targets, bracketed pronunciation spellings, slang, and keyboard instruction.
- Slugs are lowercase ASCII kebab-case and unique within the unit.
- JSON must pass `jq empty`.

## Phase allocations

- Phase 2: units 7–11, lesson counts `6, 6, 5, 5, 5` (27 total).
- Phase 3: units 12–17, lesson counts `5, 6, 5, 6, 5, 5` (32 total).
- Phase 4: units 18–23, lesson counts `5, 6, 5, 6, 5, 6` (33 total).
- Phase 5: units 24–26, lesson counts `7, 7, 8` (22 total).

Use the matching entries in `curriculum.json` → `outline_units` as the authoritative unit topics and scope.
