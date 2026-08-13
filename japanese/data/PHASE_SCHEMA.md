# Japanese phase data contract

Create exactly one JSON file containing an array of unit objects. Do not edit any other file.

## Unit shape

```json
{
  "number": 1,
  "slug": "japanese-writing-system",
  "title": "日文文字系統",
  "japanese_title": "日本語の文字",
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
  "slug": "three-writing-systems",
  "title": "三種文字的分工",
  "subtitle": "Short Traditional Chinese deck.",
  "summary": "Why this lesson matters.",
  "objectives": ["...", "...", "..."],
  "sections": [
    {
      "heading": "...",
      "paragraphs": ["One concise Traditional Chinese teaching paragraph."],
      "bullets": ["...", "...", "..."],
      "audio": [
        {"text": "ひらがな", "reading": "ひらがな", "meaning": "平假名"},
        {"text": "入口", "reading": "いりぐち", "meaning": "入口", "note": "Optional note"}
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
- Exactly 3 objectives, 3 takeaways, 2 quiz items, and 2 practice items per lesson.
- Every audio item requires `text`, `reading`, and concise Traditional Chinese `meaning`.
- `text` is authentic Japanese as shown to a learner. `reading` is the full standard pronunciation in kana and is used to generate Hepburn romanization.
- `speak` is optional and only differs when digits, symbols, abbreviations, counters, or an isolated character need a natural Japanese TTS target.
- Do not add romanization manually. The generator converts `reading` to Hepburn and displays it beside the Chinese meaning.
- Use natural, polite contemporary Japanese. Prefer です／ます style for learner-facing conversation and authentic formal wording for signs.
- Use standard Japanese orthography: show realistic kanji/kana on cards, while `reading` supplies the pronunciation.
- Explain literal structure before idiomatic Chinese when it prevents confusion.
- Keep lessons progressive and systematic: recognition/core pattern, controlled examples, then a real-life reading or listening task.
- Avoid Roman-letter-only TTS targets, bracketed pronunciation spellings, slang, keyboard instruction, and invented signage.
- Slugs are lowercase ASCII kebab-case and unique within the unit.
- Output valid UTF-8 JSON.

## Phase allocations

- Phase 1: units 1–6, lesson counts `4, 5, 5, 5, 5, 5` (29 total).
- Phase 2: units 7–11, lesson counts `6, 6, 5, 5, 5` (27 total).
- Phase 3: units 12–17, lesson counts `5, 6, 5, 6, 5, 5` (32 total).
- Phase 4: units 18–23, lesson counts `5, 6, 5, 6, 5, 6` (33 total).
- Phase 5: units 24–26, lesson counts `7, 7, 8` (22 total).

Use the matching entries in `curriculum.json` → `outline_units` as the authoritative unit topics and scope.
