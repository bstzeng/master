"""星座課程主資料與組裝函式。"""

from .foundations import FOUNDATION_UNITS
from .relationships import RELATIONSHIP_UNITS
from .signs import SIGNS
from .synthesis import SYNTHESIS_UNITS


PHASES = [
    {
        "number": 1,
        "title": "星座的起源與歷史",
        "range": "UNIT 01–06",
        "summary": "從人類觀星、黃道、古代文明與神話開始，最後清楚分辨天文學與占星學。",
        "goal": "能說明星座如何從天空辨識工具，演變成跨文化的占星象徵系統。",
        "units": list(range(1, 7)),
    },
    {
        "number": 2,
        "title": "理解個性的基礎框架",
        "range": "UNIT 07–11",
        "summary": "建立太陽、月亮、上升、元素、模式、陰影與行星功能的完整閱讀語法。",
        "goal": "不再用單一太陽星座替一個人下定論，能從多層次提出觀察問題。",
        "units": list(range(7, 12)),
    },
    {
        "number": 3,
        "title": "十二星座個性詳解",
        "range": "UNIT 12–23",
        "summary": "十二星座各一頁，固定學習神話、核心動機、優勢、陰影、關係、職場與成長方向。",
        "goal": "能用相同框架比較十二星座，同時避開刻板印象與人格宿命。",
        "units": list(range(12, 24)),
    },
    {
        "number": 4,
        "title": "星座與相互關係",
        "range": "UNIT 24–30",
        "summary": "從多層關係閱讀、元素模式互動，到感情、家庭、職場、衝突與十二對十二關係地圖。",
        "goal": "把『合不合』改成需求、溝通、界線、權力與修復能力的具體分析。",
        "units": list(range(24, 31)),
    },
    {
        "number": 5,
        "title": "星盤與綜合應用",
        "range": "UNIT 31–36",
        "summary": "認識出生星盤、相位、閱讀順序、關係合盤、自我觀察與科學思考。",
        "goal": "能閱讀基礎星盤，也能辨識巴納姆效應、確認偏誤與證據界線。",
        "units": list(range(31, 37)),
    },
]


SOURCES = {
    "iau": {
        "title": "國際天文聯合會｜The Constellations",
        "url": "https://www.iau.org/Iau/Science/What-we-do/The-Constellations.aspx",
        "note": "現代 88 星座、正式邊界，以及星座作為文化與導航工具的說明。",
    },
    "iau_faq": {
        "title": "國際天文聯合會｜Constellation FAQ",
        "url": "https://www.iau.org/Iau/Iau/Science/What-we-do/FAQs.aspx",
        "note": "黃道星座數量、蛇夫座與十二等分制度的常見問題。",
    },
    "astroedu": {
        "title": "IAU astroEDU｜What is a Constellation?",
        "url": "https://astroedu.iau.org/activities/what-is-a-constellation/",
        "note": "適合初學者的星座、距離與觀察活動。",
    },
    "british_museum": {
        "title": "大英博物館｜巴比倫十二宮泥板",
        "url": "https://www.britishmuseum.org/collection/object/W_1885-0430-15",
        "note": "約公元前 500 年、月份與黃道符號對應的實物資料。",
    },
    "met": {
        "title": "大都會藝術博物館｜Mesopotamian Magic",
        "url": "https://www.metmuseum.org/essays/mesopotamian-magic-in-the-first-millennium-bc",
        "note": "理解美索不達米亞知識、徵兆、醫療與宗教並存的歷史環境。",
    },
    "loc": {
        "title": "美國國會圖書館｜Zodiac Craze",
        "url": "https://guides.loc.gov/chronicling-america-zodiac-craze",
        "note": "十九、二十世紀報紙與大眾占星流行的原始資料入口。",
    },
    "getty": {
        "title": "Getty｜The Leiden Aratea",
        "url": "https://www.getty.edu/publications/resources/virtuallibrary/0892361425.pdf",
        "note": "古典星座如何透過中世紀手稿保存與再詮釋。",
    },
    "nature": {
        "title": "Nature｜A double-blind test of astrology",
        "url": "https://www.nature.com/articles/318419a0",
        "note": "1985 年以雙盲方法檢驗出生星盤與人格配對的經典研究。",
    },
    "apa_astrology": {
        "title": "APA Dictionary of Psychology｜Astrology",
        "url": "https://dictionary.apa.org/astrology",
        "note": "心理學對占星、人格類型與現有證據的簡明定義。",
    },
    "apa_barnum": {
        "title": "APA Dictionary of Psychology｜Barnum effect",
        "url": "https://dictionary.apa.org/barnum-effect",
        "note": "為何普遍而模糊的人格敘述容易讓人覺得特別準。",
    },
    "forer": {
        "title": "PubMed｜The fallacy of personal validation",
        "url": "https://pubmed.ncbi.nlm.nih.gov/18110193/",
        "note": "Forer 1949 年個人驗證謬誤的經典研究紀錄。",
    },
}


def sign_to_unit(sign):
    """將十二星座的固定欄位展開成和其他單元相同的完整頁面結構。"""
    return {
        "number": sign["number"],
        "slug": sign["slug"],
        "title": sign["title"],
        "english": sign["english"],
        "subtitle": f"{sign['element']}象 × {sign['mode']}宮｜{sign['ruler']}守護的核心動機、關係與成長。",
        "opening": f"{sign['title']}不是一張固定性格清單。這一頁以神話、元素、模式與核心動機建立完整框架，再把每個描述當成可觀察、可修正的假設。",
        "objectives": [f"理解{sign['title']}的象徵與核心動機", "辨認優勢如何在壓力下形成陰影", "把關係與成長描述轉成具體行為"],
        "profile": {
            "glyph": sign["glyph"],
            "dates": sign["dates"],
            "element": sign["element"],
            "mode": sign["mode"],
            "ruler": sign["ruler"],
            "polarity": sign["polarity"],
        },
        "sections": [
            {
                "heading": "起源、神話與基本座標",
                "body": sign["myth"],
                "points": [f"日期：{sign['dates']}（近似太陽宮日期）", f"元素：{sign['element']}象", f"模式：{sign['mode']}宮", f"守護星：{sign['ruler']}", f"極性：{sign['polarity']}"],
                "note": sign["myth_lens"],
            },
            {
                "heading": "核心動機與可發展的優勢",
                "body": sign["core"],
                "points": sign["strengths"],
                "note": "優勢不是自動擁有的獎品，而是核心動機經過練習、情境與責任後的成熟表現。",
            },
            {
                "heading": "壓力陰影與真正需要",
                "body": f"同一股動機若失去彈性，可能出現下列陰影。{sign['stress']}",
                "points": [*sign["shadows"], "需要：" + "、".join(sign["needs"])],
                "note": "陰影用來提早辨識反應，不是替任何傷害行為免責。",
            },
            {
                "heading": "溝通、感情、友情與家庭",
                "body": sign["communication"],
                "points": [f"感情｜{sign['love']}", f"友情｜{sign['friendship']}", f"家庭｜{sign['family']}"],
                "note": "關係描述只能當作對話起點；安全、同意、誠信與實際修復能力永遠優先。",
            },
            {
                "heading": "職場表現、成長方向與常見誤解",
                "body": sign["work"],
                "points": sign["growth"],
                "note": sign["misconception"],
            },
        ],
        "takeaways": [sign["core"], f"成熟優勢：{'、'.join(sign['strengths'][:2])}", f"壓力時需留意：{'、'.join(sign['shadows'][:2])}", sign["misconception"]],
        "quiz": [
            (f"{sign['title']}屬於什麼元素與模式？", f"{sign['element']}象、{sign['mode']}宮。"),
            (f"{sign['title']}的核心動機是什麼？", sign["core"]),
            ("為什麼不能把本頁描述直接套在每個人身上？", "因為太陽星座只是完整星盤與真實人格的一小部分，而且占星人格主張沒有足夠科學證據；描述應視為可修正假設。"),
        ],
        "practice": sign["observation"],
        "glyph": sign["glyph"],
    }


def unit_sources(number):
    if number == 1:
        keys = ["iau", "astroedu"]
    elif number == 2:
        keys = ["iau", "iau_faq"]
    elif number == 3:
        keys = ["british_museum", "met"]
    elif number == 4:
        keys = ["getty", "iau"]
    elif number == 5:
        keys = ["loc", "british_museum"]
    elif number == 6:
        keys = ["iau", "nature", "apa_astrology"]
    elif 7 <= number <= 34:
        keys = ["apa_astrology", "nature"]
    elif number == 35:
        keys = ["apa_barnum", "forer", "nature"]
    else:
        keys = ["apa_barnum", "forer", "nature", "iau"]
    return [SOURCES[key] for key in keys]


def all_units():
    units = [*FOUNDATION_UNITS, *(sign_to_unit(sign) for sign in SIGNS), *RELATIONSHIP_UNITS, *SYNTHESIS_UNITS]
    for unit in units:
        unit["phase"] = next(phase["number"] for phase in PHASES if unit["number"] in phase["units"])
        unit["sources"] = unit_sources(unit["number"])
    return units
