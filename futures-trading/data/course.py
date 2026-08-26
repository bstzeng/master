"""Shared outline metadata and official sources for the futures course."""

from .helpers import source

PHASES = [
    {"number": 1, "title": "先懂合約，再談交易", "english": "CONTRACT MECHANICS", "summary": "從期貨的用途、標準化合約與結算制度開始，建立名目價值、跳動點值、保證金與槓桿的正確模型。", "chapters": [1, 2, 3], "image": "phase-1-contract.jpg"},
    {"number": 2, "title": "把下單動作變成可驗證流程", "english": "ORDER & POSITION", "summary": "認識委託單、成交、持倉、平倉與交易成本，並比較做多與做空哪些相同、哪些絕不能鏡像套用。", "chapters": [4, 5, 6], "image": "phase-2-orders.jpg"},
    {"number": 3, "title": "依市場狀態建立策略", "english": "REGIME & STRATEGY", "summary": "讀懂趨勢、區間、基差、量與未平倉量，再把方向看法寫成有觸發、有失效點、有退出規則的策略。", "chapters": [7, 8, 9], "image": "phase-3-market.jpg"},
    {"number": 4, "title": "先控制生存，再追求報酬", "english": "RISK & PROCESS", "summary": "用每筆風險、部位大小、停損與帳戶熔斷把最壞情境寫進交易；再用計畫與日誌檢驗執行品質。", "chapters": [10, 11], "image": "phase-4-risk.jpg"},
    {"number": 5, "title": "完成一次全生命週期演練", "english": "PAPER-TRADE LIFECYCLE", "summary": "把選市場、查規格、判斷狀態、計算部位、模擬下單、管理、退出與復盤串成一套可重複流程。", "chapters": [12], "image": "phase-5-practice.jpg"},
]

CHAPTER_META = [
    (1, "futures-foundations", "期貨的起源、用途與核心特性", "WHY FUTURES EXIST", "理解標準化合約、避險、價格發現、到期與結算，不把期貨誤當成可無限持有的股票。", ["標準化合約", "避險與投機", "結算所", "到期收斂", "期貨與其他商品"], "70–90 分鐘", 1),
    (2, "contract-specifications", "讀懂一張期貨合約規格", "READ THE CONTRACT", "逐欄拆解標的、乘數、最小跳動、月份、交易時段、最後交易日與結算方式。", ["名目價值", "跳動點值", "契約月份", "交易時段", "TX 官方範例"], "75–95 分鐘", 1),
    (3, "margin-leverage", "保證金、槓桿與每日結算", "MARGIN IS A BOND", "看懂保證金不是買價、每日損益如何入帳，以及槓桿、追繳與強制平倉如何連動。", ["原始／維持保證金", "每日結算", "有效槓桿", "追繳", "壓力測試"], "85–110 分鐘", 1),
    (4, "order-workflow", "期貨交易介面與完整訂單流程", "FROM TICKET TO FILL", "以平台無關的方式認識報價、委託、成交、持倉、停損、平倉與到期管理。", ["開倉／平倉", "委託種類", "部分成交", "盤別", "模擬單"], "80–105 分鐘", 2),
    (5, "pnl-costs", "多空損益與交易成本計算", "KNOW THE P&L", "精確計算多空毛損益、跳動價值、未實現與已實現損益，以及費用、稅與滑價。", ["多空公式", "跳動點值", "交易成本", "平均價", "期望值"], "90–115 分鐘", 2),
    (6, "long-vs-short", "做多與做空的完整比較", "MIRROR MECHANICS, DIFFERENT RISKS", "分清楚多空對稱的損益公式與不對稱的行情速度、跳空、擠壓、心理與退出條件。", ["共同流程", "風險不對稱", "觸發與失效", "避險", "雙情境演練"], "85–110 分鐘", 2),
    (7, "market-structure", "期貨價格結構與市場資訊", "READ THE REGIME", "用趨勢、區間、波動、成交量、未平倉量、基差與期限結構建立市場狀態儀表板。", ["市場狀態", "量與未平倉量", "基差", "正逆價差", "轉倉"], "95–120 分鐘", 3),
    (8, "long-strategies", "做多策略的建立方式", "BUILD A LONG PLAN", "從突破、拉回、區間收復三種邏輯，寫出進場觸發、失效點、部位與退出規則。", ["突破", "拉回", "收復", "失效點", "模擬驗證"], "95–120 分鐘", 3),
    (9, "short-strategies", "做空策略的建立方式", "BUILD A SHORT PLAN", "建立跌破、反彈失敗與假突破反轉策略，並處理空頭擠壓、跳空與快速波動。", ["跌破", "反彈失敗", "假突破", "擠壓風險", "避險空單"], "95–120 分鐘", 3),
    (10, "risk-position-sizing", "停損、部位大小與帳戶風險", "SURVIVE THE DISTRIBUTION", "把可承受損失換算成口數，設計停損、現金緩衝、單日熔斷與組合暴露上限。", ["每筆風險", "口數公式", "停損種類", "熔斷", "壓力情境"], "105–135 分鐘", 4),
    (11, "plan-journal", "建立交易計畫與交易日誌", "TURN TRADING INTO DATA", "用盤前計畫、檢查表、交易日誌與統計把結果拆成策略品質、執行品質與隨機波動。", ["交易計畫", "盤前檢查", "日誌欄位", "期望值", "30 筆模擬"], "90–120 分鐘", 4),
    (12, "trade-lifecycle", "完成一筆期貨交易的全生命週期", "PAPER TRADE END TO END", "從合約選擇到復盤完整演練一次，並用清楚的畢業門檻決定是否繼續模擬。", ["選合約", "規格核對", "下單管理", "退出復盤", "實盤門檻"], "120–150 分鐘", 5),
]

CHAPTERS = [
    {"number": n, "slug": slug, "title": title, "english": english, "summary": summary, "topics": topics, "duration": duration, "phase": phase, "href": f"chapter-{n:02d}-{slug}.html"}
    for n, slug, title, english, summary, topics, duration, phase in CHAPTER_META
]

OFFICIAL = {
    "cftc_basics": source("CFTC｜Futures Market Basics", "https://www.cftc.gov/LearnAndProtect/EducationCenter/FuturesMarketBasics/index2.htm", "期貨合約、避險者、投機者、結算與市場功能的官方入門。"),
    "cftc_purpose": source("CFTC｜The Economic Purpose of Futures Markets", "https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/economicpurpose.html", "價格發現、風險移轉、保證金與每日結算的官方說明。"),
    "taifex_tx": source("臺灣期貨交易所｜臺股期貨 TX 契約規格", "https://www.taifex.com.tw/cht/2/tX?menuid1=12", "TX 乘數、最小升降單位、月份、時段、到期與結算規格；交易前應重新查閱。"),
    "taifex_qa": source("臺灣期貨交易所｜期貨交易問答", "https://www.taifex.com.tw/cht/9/futuresQA", "交易制度、保證金、結算與風險的官方問答。"),
    "taifex_margin": source("臺灣期貨交易所｜保證金計收方式", "https://www.taifex.com.tw/cht/5/margingReqSSF", "保證金計算與調整方式；實際金額須查交易所與期貨商最新公告。"),
    "taifex_news": source("臺灣期貨交易所｜公告", "https://www.taifex.com.tw/cht/11/announcement", "契約、保證金、交易制度與風險措施的最新公告入口。"),
    "nfa_best": source("NFA｜Investor Best Practices", "https://www.nfa.futures.org/investors/investor-resources/files/investor-best-practices.html", "查核業者、理解費用與只使用風險資本等投資人保護原則。"),
    "nfa_fundamentals": source("NFA｜Futures Fundamentals", "https://www.nfa.futures.org/investors/investor-resources/files/futuresFundamentals.html", "期貨市場、帳戶、下單、風險與監管的完整官方教材。"),
}
