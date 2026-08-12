# Python 課程單元資料格式

每位協作者只新增自己被分配的 `unit-XX.json`，不要修改共用檔案或其他單元。

## 必填結構

```json
{
  "number": 1,
  "phase": 1,
  "slug": "algorithm-foundations",
  "title": "演算法基礎",
  "english": "Algorithm Foundations",
  "summary": "單元摘要。",
  "goal": "完成單元後的核心能力。",
  "prerequisites": ["先備知識"],
  "outcomes": ["可觀察的學習成果"],
  "lessons": [
    {
      "number": 1,
      "slug": "what-is-an-algorithm",
      "title": "資料結構與演算法是什麼",
      "subtitle": "一句話說明本課重點",
      "duration": "15 分鐘",
      "difficulty": "入門",
      "summary": "本課摘要。",
      "objectives": ["本課學習目標"],
      "sections": [
        {
          "heading": "段落標題",
          "paragraphs": ["完整教學段落。"],
          "bullets": ["補充重點"],
          "code": "可省略的 Python 程式碼",
          "code_caption": "可省略的程式碼說明",
          "table": {
            "headers": ["欄位一", "欄位二"],
            "rows": [["內容一", "內容二"]]
          },
          "callout": "可省略的提醒或觀念澄清"
        }
      ],
      "takeaways": ["本課重點整理"],
      "quiz": [
        {"question": "理解題", "answer": "答案與原因"}
      ],
      "practice": ["不要求立即作答的延伸練習"]
    }
  ]
}
```

`code`、`code_caption`、`table`、`callout` 可以省略，其餘欄位必填。每課至少 3 個 sections、3 個 takeaways、2 題 quiz、2 個 practice。演算法課應包含能閱讀的 Python 範例與複雜度說明；概念課可用表格或生活例子代替程式碼。

## 單元對照

| 編號 | phase | slug | 單元 |
|---|---:|---|---|
| 01 | 1 | `algorithm-foundations` | 演算法基礎 |
| 02 | 1 | `python-builtins` | Python 內建資料結構 |
| 03 | 1 | `arrays-and-strings` | 陣列與字串技巧 |
| 04 | 1 | `searching` | 搜尋演算法 |
| 05 | 1 | `sorting` | 排序演算法 |
| 06 | 1 | `linked-lists` | 鏈結串列 |
| 07 | 1 | `stack-queue-heap` | Stack、Queue 與 Heap |
| 08 | 1 | `recursion-divide-backtracking` | 遞迴、分治與回溯 |
| 09 | 1 | `trees` | 樹狀資料結構 |
| 10 | 1 | `graph-basics` | 圖論基礎 |
| 11 | 2 | `classic-graph-algorithms` | 經典圖論演算法 |
| 12 | 2 | `greedy` | Greedy 貪心演算法 |
| 13 | 2 | `dynamic-programming` | Dynamic Programming 動態規劃 |
| 14 | 2 | `string-algorithms` | 經典字串演算法 |
| 15 | 2 | `advanced-data-structures` | 進階資料結構 |
| 16 | 2 | `problem-solving` | 綜合解題與演算法設計 |

## 寫作原則

- 使用台灣繁體中文，第一次出現專有名詞時附英文。
- 先講直覺，再講規則，最後才給程式碼與複雜度。
- 不假設讀者有資工背景，但不把內容寫成兒童教材。
- 程式碼使用 Python 3，變數命名清楚，不依賴第三方套件。
- 不使用外部圖片或需要授權的內容。
- 各課之間避免重複大段文字，必要時以前置課程概念帶過。
