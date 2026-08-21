"""Assemble the sixty-unit Tolkien legendarium course."""

from .part_1 import UNITS as PART_1
from .part_2 import UNITS as PART_2
from .part_3 import UNITS as PART_3
from .part_4 import UNITS as PART_4


PHASES = [
    {
        "number": 1,
        "title": "托爾金與傳說體系",
        "english": "THE LEGENDARIUM",
        "range": "UNIT 01–04",
        "era": "現實世界／創作史",
        "summary": "先理解作者、文本層級、版本差異與敘事框架，建立不混淆原著、遺稿和改編的閱讀方法。",
        "goal": "能辨識主要作品的關係，並在遇到矛盾時先問來源、版本與敘事者。",
        "units": list(range(1, 5)),
    },
    {
        "number": 2,
        "title": "創世與雙聖樹紀元",
        "english": "BEFORE THE SUN",
        "range": "UNIT 05–10",
        "era": "創世至諾多流亡",
        "summary": "從埃努的大樂章、阿爾達受損到精靈寶鑽與費諾誓言，追蹤美、自由與佔有如何開啟漫長悲劇。",
        "goal": "理解中土世界的宇宙觀，以及第一紀元衝突為何早在太陽升起前已經成形。",
        "units": list(range(5, 11)),
    },
    {
        "number": 3,
        "title": "第一紀元：珠寶與悲劇",
        "english": "THE FIRST AGE",
        "range": "UNIT 11–18",
        "era": "貝爾蘭戰爭",
        "summary": "諾多王國、英雄愛情、家族誓言與毀滅一路走到埃蘭迪爾航行和憤怒之戰。",
        "goal": "能以誓言、血脈、選擇和後果串起第一紀元，而不是只記戰役與名字。",
        "units": list(range(11, 19)),
    },
    {
        "number": 4,
        "title": "第二紀元：戒指與帝國",
        "english": "THE SECOND AGE",
        "range": "UNIT 19–24",
        "era": "努曼諾爾至最後同盟",
        "summary": "從海上王國與精靈工藝，到索倫的戒指計畫、努曼諾爾覆亡與最後同盟。",
        "goal": "理解力量之戒、死亡恐懼與帝國擴張如何共同塑造《魔戒》的歷史背景。",
        "units": list(range(19, 25)),
    },
    {
        "number": 5,
        "title": "第三紀元前史",
        "english": "THE LONG WATCH",
        "range": "UNIT 25–29",
        "era": "魔戒失落至孤山流亡",
        "summary": "魔戒失落後，北方王國、剛鐸、洛汗、巫師與孤山的多條歷史慢慢匯向同一場危機。",
        "goal": "看懂《哈比人》和《魔戒》開始以前，數百年政治、族群與索倫回歸的因果。",
        "units": list(range(25, 30)),
    },
    {
        "number": 6,
        "title": "《哈比人》：意外旅程",
        "english": "THERE AND BACK AGAIN",
        "range": "UNIT 30–34",
        "era": "第三紀元 2941 年",
        "summary": "跟著比爾博離開袋底洞，穿越巨怪、謎語、森林、巨龍與五軍之戰。",
        "goal": "理解比爾博如何以機智和道德判斷改變遠征，以及一枚戒指如何進入大歷史。",
        "units": list(range(30, 35)),
    },
    {
        "number": 7,
        "title": "《魔戒》：魔戒戰爭",
        "english": "THE WAR OF THE RING",
        "range": "UNIT 35–44",
        "era": "第三紀元 3001–3021 年",
        "summary": "從夏爾、遠征隊分裂到洛汗、剛鐸、末日火山、返鄉與灰港岸，完整拆解主線。",
        "goal": "能同時追蹤持戒任務、戰爭政治、人物創傷與結局代價。",
        "units": list(range(35, 45)),
    },
    {
        "number": 8,
        "title": "第四紀元與人物終局",
        "english": "AFTER THE VICTORY",
        "range": "UNIT 45–48",
        "era": "第四紀元初期",
        "summary": "勝利之後仍有治理、告別、死亡與記憶；中土進入人類時代，舊世界慢慢離去。",
        "goal": "理解大結局不是停在加冕，而是每位人物如何承擔和平與時間的後果。",
        "units": list(range(45, 49)),
    },
    {
        "number": 9,
        "title": "人物、權力與核心主題",
        "english": "DEEP READING",
        "range": "UNIT 49–56",
        "era": "跨紀元主題閱讀",
        "summary": "比較反派、巫師、持戒者、王權、女性角色，以及死亡、自然、憐憫與自由意志。",
        "goal": "從劇情整理進入文本分析，能用證據說明跨作品的主題回聲。",
        "units": list(range(49, 57)),
    },
    {
        "number": 10,
        "title": "影視改編與完整學習路線",
        "english": "ADAPTATION & RETURN",
        "range": "UNIT 57–60",
        "era": "電影、影集與重讀",
        "summary": "分開分析《魔戒》《哈比人》電影與《力量之戒》影集，最後建立自己的閱讀觀看順序。",
        "goal": "能欣賞改編又保持版本界線，並把六十單元轉成可持續更新的個人知識系統。",
        "units": list(range(57, 61)),
    },
]


def all_units():
    """Return all units in canonical course order."""
    return sorted([*PART_1, *PART_2, *PART_3, *PART_4], key=lambda item: item["number"])


def all_sources():
    """Deduplicate sources while preserving first appearance."""
    sources = []
    seen = set()
    for current in all_units():
        for source in current["sources"]:
            key = source["url"]
            if key not in seen:
                seen.add(key)
                sources.append(source)
    return sources
