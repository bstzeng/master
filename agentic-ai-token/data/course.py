"""Outline and shared references for Token-Efficient Agentic AI."""

PHASES = [
    {"number": 1, "title": "看懂成本，建立基準", "english": "MEASURE BEFORE YOU CUT", "summary": "先追蹤一次任務中輸入、輸出、推理、工具與重試如何累積，再用成功任務成本建立基準。", "chapters": [1, 2], "image": "phase-1-cost-map.png"},
    {"number": 2, "title": "提示詞與上下文瘦身", "english": "DESIGN THE CONTEXT", "summary": "把目標說清楚、只載入必要資訊，並用摘要、記憶與壓縮控制長對話的成本。", "chapters": [3, 4, 5], "image": "phase-2-context.png"},
    {"number": 3, "title": "工具與執行迴圈最佳化", "english": "CONTROL THE LOOP", "summary": "縮小工具面與工具輸出，定義停止、重試與權限邊界，避免 Agent 在迴圈中空轉。", "chapters": [6, 7, 8], "image": "phase-3-tools.png"},
    {"number": 4, "title": "模型、快取與多 Agent", "english": "ROUTE THE WORK", "summary": "依任務價值分流模型與推理強度，正確計算多 Agent 經濟性，並提高可重複前綴的快取命中。", "chapters": [9, 10, 11], "image": "phase-4-routing.png"},
    {"number": 5, "title": "正式環境與持續改善", "english": "OPERATE THE SYSTEM", "summary": "把預算、品質、延遲與告警接進正式流程，建立可持續改善的 Token-Efficient Agent Playbook。", "chapters": [12], "image": "phase-5-production.png"},
]

CHAPTER_META = [
    (1, "token-cost-map", "Agentic AI 的 Token 成本地圖", "TRACE EVERY TOKEN", "看懂一次任務為何會把同一份內容重送很多次。", ["輸入／輸出", "推理 Token", "工具與歷史", "成本公式", "浪費熱點"], "65–85 分鐘", 1),
    (2, "measure-baseline", "先量測，再開始節省", "COST PER SUCCESSFUL TASK", "用成功率、總 Token、呼叫、重試與延遲建立可比較基準。", ["Usage", "基準任務", "成本／成功", "品質閘門", "回歸比較"], "70–90 分鐘", 1),
    (3, "lean-prompts", "高效率提示詞設計", "SAY THE RIGHT THING ONCE", "刪掉儀式與重複，保留真正決定品質的目標、限制與證據。", ["任務契約", "精簡提示", "輸出預算", "結構化輸出", "漸進刪減"], "75–95 分鐘", 2),
    (4, "context-engineering", "Context Engineering 上下文工程", "LOAD ONLY WHAT MATTERS", "讓 Agent 先定位再讀取，避免整個專案與文件每一步都進入上下文。", ["相關性", "選擇性載入", "RAG", "Context Budget", "重新定位"], "85–110 分鐘", 2),
    (5, "memory-compaction", "對話記憶、摘要與壓縮", "REMEMBER WITHOUT REPLAYING", "把歷史轉成可驗證狀態，保留決策與未完成事項而不是逐字重播。", ["短期記憶", "長期記憶", "Checkpoint", "Compaction", "重新開局"], "80–105 分鐘", 2),
    (6, "tool-surface", "只給 Agent 真正需要的工具", "EXPOSE THE SMALLEST TOOLSET", "縮小工具定義與選擇空間，讓路由更快、更準、更便宜。", ["工具面", "動態載入", "描述與 Schema", "權限", "路由測試"], "70–90 分鐘", 3),
    (7, "tool-output", "縮小工具輸出再交給模型", "REDUCE BEFORE REASONING", "先搜尋、過濾、聚合與結構化，再讓模型對少量高訊號內容判斷。", ["欄位投影", "Top-K", "去重與聚合", "Artifact", "程式化工具"], "80–105 分鐘", 3),
    (8, "loops-retries", "減少重試、空轉與無效確認", "MAKE THE LOOP TERMINATE", "用完成條件、錯誤契約、重試上限與權限邊界停止無效循環。", ["停止條件", "冪等", "Retry Budget", "核准邊界", "失敗輸出"], "80–100 分鐘", 3),
    (9, "model-routing", "模型與推理強度分流", "SPEND INTELLIGENCE WHERE IT PAYS", "用任務風險與可驗證性選模型、推理強度及輸出詳細度。", ["任務分級", "推理強度", "升級閘門", "輸出長度", "路由評測"], "85–110 分鐘", 4),
    (10, "multi-agent-economics", "多 Agent 到底省不省 Token", "PARALLEL IS NOT FREE", "分清楚省時間與省 Token，避免重複上下文、研究與統整成本。", ["可分割性", "共享上下文", "交接格式", "協調成本", "損益門檻"], "90–115 分鐘", 4),
    (11, "prompt-cache", "Prompt Cache 與可重複內容", "MAKE REPETITION CHEAPER", "排列穩定前綴與動態尾端，量測快取讀寫而不是假設有命中。", ["穩定前綴", "動態尾端", "命中率", "失效", "淨節省"], "70–95 分鐘", 4),
    (12, "production-playbook", "Token-Efficient Agent 完整架構", "OPERATE FOR QUALITY AND COST", "把預算、Evals、降級、告警與改善循環組成正式環境 Playbook。", ["階段預算", "Evals", "降級", "成本告警", "30 天計畫"], "100–130 分鐘", 5),
]

CHAPTERS = [
    {"number": n, "slug": slug, "title": title, "english": english, "summary": summary, "topics": topics, "duration": duration, "phase": phase, "href": f"chapter-{n:02d}-{slug}.html", "ready": True}
    for n, slug, title, english, summary, topics, duration, phase in CHAPTER_META
]

OFFICIAL = {
    "guidance": {"title": "OpenAI Docs｜Model guidance", "url": "https://developers.openai.com/api/docs/guides/latest-model", "note": "精簡提示、相關工具、推理強度、快取與工作流評測的現行官方指引。"},
    "counting": {"title": "OpenAI Docs｜Counting tokens", "url": "https://developers.openai.com/api/docs/guides/token-counting", "note": "輸入與使用量估算、Token 計數的官方概念。"},
    "state": {"title": "OpenAI Docs｜Conversation state", "url": "https://developers.openai.com/api/docs/guides/conversation-state", "note": "多輪狀態、續接回應與歷史管理。"},
    "compaction": {"title": "OpenAI Docs｜Compaction", "url": "https://developers.openai.com/api/docs/guides/compaction", "note": "長工作流的狀態壓縮與上下文控制。"},
    "caching": {"title": "OpenAI Docs｜Prompt caching", "url": "https://developers.openai.com/api/docs/guides/prompt-caching", "note": "快取前綴、命中與使用量觀測。"},
    "multi": {"title": "OpenAI Docs｜Multi-agent", "url": "https://developers.openai.com/api/docs/guides/multi-agent", "note": "多 Agent 協調、平行工作與適用條件。"},
}
