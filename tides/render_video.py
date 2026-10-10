"""Render the cute tide animation with pycairo and mux with narration via ffmpeg.

Usage:
  python build_audio.py          # -> build/audio.wav, build/timeline.json
  python render_video.py         # -> tide_for_kids.mp4
  python render_video.py --still 40.0   # render one frame to build/still.png (debug)
Needs: pycairo, ffmpeg, Noto Sans CJK TC font
"""
import json, math, os, subprocess, sys
import cairo

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
W, H, FPS = 1280, 720, 24
FONT = "Noto Sans CJK TC"

TL = json.load(open(os.path.join(BUILD, "timeline.json"), encoding="utf-8"))

# ---------------------------------------------------------------- palette
def hexc(h, a=1.0):
    h = h.lstrip("#")
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)

SKY1, SKY2 = hexc("8fd8ff"), hexc("e8f8ff")
SEA1, SEA2 = hexc("3aa7f0"), hexc("1f6fd1")
SAND = hexc("ffe2a1")
SAND2 = hexc("f7c873")
SPACE1, SPACE2 = hexc("1b1f5e"), hexc("3a2f8f")
WHITE, BLACK = (1, 1, 1, 1), hexc("2b2b40")
PINK = hexc("ff8fb1", 0.7)
YELLOW, ORANGE = hexc("ffe066"), hexc("ffa94d")
GREEN = hexc("63d471")
RED = hexc("ff6b6b")


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def pop(x):
    """overshoot pop-in 0..1"""
    x = max(0.0, min(1.0, x))
    return 1 + 2.2 * (x - 1) ** 3 + 1.2 * (x - 1) ** 2 if x < 1 else 1.0


def setc(c, col):
    c.set_source_rgba(*col)


def rrect(c, x, y, w, h, r):
    c.new_sub_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    c.close_path()


def circle(c, x, y, r, col, stroke=None, lw=4):
    c.arc(x, y, r, 0, 2 * math.pi)
    setc(c, col)
    if stroke:
        c.fill_preserve(); setc(c, stroke); c.set_line_width(lw); c.stroke()
    else:
        c.fill()


def text(c, s, x, y, size, col=BLACK, bold=True, align="center", outline=None, ow=6):
    c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL,
                       cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)
    ext = c.text_extents(s)
    if align == "center":
        x0 = x - ext.x_advance / 2
    elif align == "right":
        x0 = x - ext.x_advance
    else:
        x0 = x
    y0 = y + size * 0.35
    c.move_to(x0, y0)
    c.text_path(s)
    if outline:
        setc(c, outline); c.set_line_width(ow); c.set_line_join(cairo.LINE_JOIN_ROUND)
        c.stroke_preserve()
    setc(c, col); c.fill()
    return ext.x_advance


def text_w(c, s, size, bold=True):
    c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL,
                       cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)
    return c.text_extents(s).x_advance


def wrap(c, s, size, maxw):
    lines, cur = [], ""
    for ch in s:
        if text_w(c, cur + ch, size) > maxw and cur:
            lines.append(cur); cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    # avoid a line starting with punctuation
    for i in range(1, len(lines)):
        if lines[i] and lines[i][0] in "，。！？、：；」":
            lines[i - 1] += lines[i][0]; lines[i] = lines[i][1:]
    return [l for l in lines if l]


# ---------------------------------------------------------------- face & characters
def face(c, x, y, r, t, talk=False, blink_off=0.0, cheek=True, eye_col=BLACK):
    blink = (math.fmod(t + blink_off, 3.7) < 0.12)
    ex, ey, er = r * 0.36, r * 0.12, r * 0.13
    for sx in (-1, 1):
        if blink:
            c.set_line_width(max(2, r * 0.06)); setc(c, eye_col)
            c.move_to(x + sx * ex - er, y - ey); c.line_to(x + sx * ex + er, y - ey); c.stroke()
        else:
            circle(c, x + sx * ex, y - ey, er, eye_col)
            circle(c, x + sx * ex + er * 0.35, y - ey - er * 0.35, er * 0.38, WHITE)
    if cheek:
        for sx in (-1, 1):
            c.save(); c.translate(x + sx * r * 0.58, y + r * 0.18); c.scale(1, 0.6)
            circle(c, 0, 0, r * 0.15, PINK); c.restore()
    mo = (0.5 + 0.5 * math.sin(t * 22)) if talk else 0.0
    if mo > 0.15:
        c.save(); c.translate(x, y + r * 0.28); c.scale(1, 0.4 + mo * 0.9)
        circle(c, 0, 0, r * 0.16, hexc("c2185b")); c.restore()
    else:
        c.set_line_width(max(2, r * 0.06)); setc(c, eye_col); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.arc(x, y + r * 0.12, r * 0.2, 0.15 * math.pi, 0.85 * math.pi); c.stroke()


def wave_baby(c, x, y, s, t, talk=False, wave_hand=False, buoy=False):
    """浪浪: a chubby blue water drop/wave with a curl on top."""
    c.save(); c.translate(x, y + math.sin(t * 3) * 6 * s); c.scale(s, s)
    # body
    c.move_to(-70, 60)
    c.curve_to(-90, 0, -70, -60, -10, -75)
    c.curve_to(40, -88, 85, -55, 70, -15)   # curl top
    c.curve_to(62, 5, 30, 5, 30, -15)
    c.curve_to(30, -30, 48, -32, 48, -20)
    c.curve_to(80, 10, 85, 40, 70, 60)
    c.curve_to(30, 75, -30, 75, -70, 60)
    c.close_path()
    g = cairo.LinearGradient(0, -80, 0, 70)
    g.add_color_stop_rgba(0, *hexc("7fd4ff")); g.add_color_stop_rgba(1, *hexc("2f8ee8"))
    c.set_source(g); c.fill_preserve()
    c.set_line_width(5); setc(c, hexc("1c5fb8")); c.stroke()
    # foam bits
    for fx, fy, fr in ((-40, -50, 9), (-22, -62, 7), (60, -50, 6)):
        circle(c, fx, fy, fr, (1, 1, 1, 0.85))
    face(c, -5, 10, 60, t, talk)
    # little arms
    c.set_line_width(9); c.set_line_cap(cairo.LINE_CAP_ROUND); setc(c, hexc("2f8ee8"))
    c.move_to(-72, 25); c.line_to(-100, 5 + (math.sin(t * 8) * 18 if wave_hand else 18)); c.stroke()
    c.move_to(72, 25); c.line_to(100, 35); c.stroke()
    if buoy:
        c.set_line_width(22); setc(c, RED)
        c.save(); c.scale(1, 0.35); c.arc(0, 175, 85, 0, 2 * math.pi); c.stroke(); c.restore()
        c.set_line_width(22); setc(c, WHITE)
        for a in (0.3, 1.4, 2.5):
            c.save(); c.scale(1, 0.35); c.arc(0, 175, 85, a, a + 0.35); c.stroke(); c.restore()
    c.restore()


def moon(c, x, y, r, t, talk=False):
    c.save(); c.translate(x, y + math.sin(t * 2 + 1) * 5)
    glow = cairo.RadialGradient(0, 0, r * 0.8, 0, 0, r * 1.6)
    glow.add_color_stop_rgba(0, 1, 0.95, 0.6, 0.45); glow.add_color_stop_rgba(1, 1, 0.95, 0.6, 0)
    c.set_source(glow); c.arc(0, 0, r * 1.6, 0, 2 * math.pi); c.fill()
    circle(c, 0, 0, r, hexc("fff3a6"), hexc("e8c547"), max(3, r * 0.06))
    for cx, cy, cr in ((-0.45, -0.45, 0.14), (0.5, 0.45, 0.11), (0.55, -0.3, 0.08)):
        circle(c, cx * r, cy * r, cr * r, hexc("f3df7a"))
    # bow
    setc(c, hexc("ff7eb6"))
    bx, by = r * 0.45, -r * 0.82
    for sx in (-1, 1):
        c.move_to(bx, by); c.line_to(bx + sx * r * 0.32, by - r * 0.18); c.line_to(bx + sx * r * 0.32, by + r * 0.18)
        c.close_path(); c.fill()
    circle(c, bx, by, r * 0.09, hexc("e0559a"))
    face(c, 0, r * 0.05, r, t, talk, 1.1)
    c.restore()


def earth(c, x, y, r, t, rot=0.0, talk=False, show_face=True):
    c.save(); c.translate(x, y)
    circle(c, 0, 0, r, hexc("4da3ff"), hexc("2361b5"), max(3, r * 0.05))
    c.save(); c.arc(0, 0, r - 2, 0, 2 * math.pi); c.clip()
    c.rotate(rot)
    setc(c, GREEN)
    for ang, d, sz in ((0.3, 0.55, 0.38), (2.2, 0.5, 0.42), (4.0, 0.6, 0.3), (5.2, 0.2, 0.25)):
        px, py = math.cos(ang) * d * r, math.sin(ang) * d * r
        c.save(); c.translate(px, py); c.rotate(ang); c.scale(1.3, 0.8)
        c.arc(0, 0, sz * r, 0, 2 * math.pi); c.restore(); c.fill()
    c.restore()
    if show_face:
        face(c, 0, r * 0.05, r * 0.85, t, talk, 2.3)
    c.restore()


def sun(c, x, y, r, t):
    c.save(); c.translate(x, y); c.rotate(t * 0.4)
    setc(c, ORANGE)
    for i in range(12):
        a = i * math.pi / 6
        c.move_to(math.cos(a - 0.12) * r * 1.05, math.sin(a - 0.12) * r * 1.05)
        c.line_to(math.cos(a) * r * 1.45, math.sin(a) * r * 1.45)
        c.line_to(math.cos(a + 0.12) * r * 1.05, math.sin(a + 0.12) * r * 1.05)
        c.close_path(); c.fill()
    c.restore()
    c.save(); c.translate(x, y)
    circle(c, 0, 0, r, YELLOW, ORANGE, max(3, r * 0.06))
    face(c, 0, r * 0.05, r, t, False, 0.5)
    c.restore()


def cloud(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    for cx, cy, cr in ((0, 0, 30), (30, -14, 34), (62, 0, 28), (32, 10, 28)):
        circle(c, cx, cy, cr, (1, 1, 1, 0.95))
    c.restore()


def stars(c, t, seed=7, n=60):
    import random
    rnd = random.Random(seed)
    for i in range(n):
        x, y = rnd.random() * W, rnd.random() * H
        tw = 0.5 + 0.5 * math.sin(t * 2 + i)
        circle(c, x, y, 1.5 + rnd.random() * 2, (1, 1, 0.85, 0.4 + 0.6 * tw))


def sky_bg(c, top=SKY1, bot=SKY2):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgba(0, *top); g.add_color_stop_rgba(1, *bot)
    c.set_source(g); c.paint()


def space_bg(c, t):
    g = cairo.LinearGradient(0, 0, W, H)
    g.add_color_stop_rgba(0, *SPACE1); g.add_color_stop_rgba(1, *SPACE2)
    c.set_source(g); c.paint()
    stars(c, t)


def sea(c, y, t, amp=10, col1=SEA1, col2=SEA2, x0=0, x1=W, foam=True):
    c.move_to(x0, H)
    for x in range(int(x0), int(x1) + 10, 10):
        c.line_to(x, y + math.sin(x / 60 + t * 2.2) * amp + math.sin(x / 23 - t * 3) * amp * 0.3)
    c.line_to(x1, H); c.close_path()
    g = cairo.LinearGradient(0, y - amp, 0, H)
    g.add_color_stop_rgba(0, *col1); g.add_color_stop_rgba(1, *col2)
    c.set_source(g); c.fill()
    if foam:
        c.set_line_width(5); setc(c, (1, 1, 1, 0.8)); c.set_line_cap(cairo.LINE_CAP_ROUND)
        first = True
        for x in range(int(x0), int(x1) + 10, 10):
            yy = y + math.sin(x / 60 + t * 2.2) * amp + math.sin(x / 23 - t * 3) * amp * 0.3
            (c.move_to if first else c.line_to)(x, yy); first = False
        c.stroke()


def arrow(c, x0, y0, x1, y1, col, lw=8, head=22, dash=None, t=0):
    setc(c, col); c.set_line_width(lw); c.set_line_cap(cairo.LINE_CAP_ROUND)
    ang = math.atan2(y1 - y0, x1 - x0)
    ex, ey = x1 - math.cos(ang) * head * 0.8, y1 - math.sin(ang) * head * 0.8
    if dash:
        c.set_dash(dash, -t * 60)
    c.move_to(x0, y0); c.line_to(ex, ey); c.stroke(); c.set_dash([])
    c.move_to(x1, y1)
    c.line_to(x1 - math.cos(ang - 0.45) * head, y1 - math.sin(ang - 0.45) * head)
    c.line_to(x1 - math.cos(ang + 0.45) * head, y1 - math.sin(ang + 0.45) * head)
    c.close_path(); c.fill()


def label(c, s, x, y, size=34, bg=WHITE, fg=BLACK, scale=1.0, alpha=1.0):
    if scale <= 0.01 or alpha <= 0.01:
        return
    c.save(); c.translate(x, y); c.scale(scale, scale)
    w = text_w(c, s, size) + size * 0.9
    h = size * 1.5
    rrect(c, -w / 2, -h / 2, w, h, h / 2)
    setc(c, (bg[0], bg[1], bg[2], bg[3] * alpha)); c.fill_preserve()
    setc(c, (BLACK[0], BLACK[1], BLACK[2], 0.15 * alpha)); c.set_line_width(3); c.stroke()
    text(c, s, 0, 0, size, (fg[0], fg[1], fg[2], alpha))
    c.restore()


# ---------------------------------------------------------------- tide ocean shell (space view)
def ocean_shell(c, x, y, r, a_near, a_far, dir_ang, t):
    pts = []
    for i in range(121):
        th = i / 120 * 2 * math.pi
        rel = th - dir_ang
        cs = math.cos(rel)
        rr = r + 6 + a_near * max(0, cs) ** 2 + a_far * max(0, -cs) ** 2 + math.sin(th * 9 + t * 3) * 2.5
        pts.append((x + math.cos(th) * rr, y + math.sin(th) * rr))
    c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.close_path()
    setc(c, hexc("6fd0ff", 0.65)); c.fill_preserve()
    setc(c, hexc("ffffff", 0.8)); c.set_line_width(4); c.stroke()


# ---------------------------------------------------------------- scene helpers
def cur_line(seg, t):
    """index of line being spoken (or last spoken) and whether speaking now"""
    idx, speaking = -1, False
    for i, ln in enumerate(seg["lines"]):
        if t >= ln["start"]:
            idx = i
            speaking = t <= ln["end"]
    return idx, speaking


def line_t(seg, i, t):
    ln = seg["lines"][i]
    return t - ln["start"], ln["end"] - ln["start"]


# ---------------------------------------------------------------- scenes  (t = global time)
def s1_intro(c, seg, t):
    lt = t - seg["start"]
    sky_bg(c)
    sun(c, 1150, 110, 55, t)
    cloud(c, 120 + math.fmod(t * 15, 1400) - 100, 110, 1.0)
    cloud(c, 700 - math.fmod(t * 10, 900), 70, 0.8)
    sea(c, 520, t, 12)
    # title
    sc = pop(lt / 0.8)
    c.save(); c.translate(W / 2, 170 + math.sin(t * 2) * 6); c.scale(sc, sc)
    text(c, "潮汐大冒險", 0, 0, 96, hexc("ff7a59"), outline=WHITE, ow=16)
    c.restore()
    label(c, "月亮姐姐拉海水", W / 2, 268, 36, bg=YELLOW, scale=pop((lt - 0.6) / 0.6))
    idx, speaking = cur_line(seg, t)
    wb = pop((lt - 0.3) / 0.7)
    if wb > 0:
        wave_baby(c, 330, 480 + (1 - wb) * 200, 1.15, t, talk=speaking, wave_hand=True)
    # moon & earth fly in during line 2
    p = ease((t - seg["lines"][1]["start"]) / 1.5)
    if p > 0:
        moon(c, 1300 - 280 * p, 380, 62, t)
        earth(c, 1300 - 480 * p, 420, 72, t, rot=t * 0.3)
        if p > 0.9:
            label(c, "月亮姐姐", 1020, 470, 24, scale=p)
            label(c, "地球哥哥", 820, 520, 24, scale=p)
    if idx == 2:
        label(c, "出發囉！", 330, 300, 40, bg=hexc("ffd6e7"), scale=pop(line_t(seg, 2, t)[0] / 0.5))


def beach_scene(c, t, level_y, show_items):
    sky_bg(c)
    sun(c, 700, 95, 48, t)
    cloud(c, 200, 90, 0.9); cloud(c, 650, 140, 0.7)

    def sand_y(x):
        return 600 - max(0, x - 120) * 0.30

    # water first (full width); the sand slope drawn on top forms the shoreline
    xi = 120 + (600 - level_y) / 0.30
    sea(c, level_y, t, 8)
    # sand
    c.move_to(0, H); c.line_to(0, sand_y(0))
    for x in range(0, W + 20, 20):
        c.line_to(x, sand_y(x))
    c.line_to(W, H); c.close_path()
    setc(c, SAND); c.fill()
    # rocks & shells on beach
    for (x, kind) in ((520, "rock"), (640, "shell"), (760, "rock"), (880, "star"), (980, "shell")):
        y = sand_y(x)
        vis = y < level_y + 5 or show_items
        if not vis:
            continue
        if kind == "rock":
            c.save(); c.translate(x, y - 8); c.scale(1.6, 0.9)
            circle(c, 0, 0, 22, hexc("9aa5b1"), hexc("6b7785"), 3); c.restore()
        elif kind == "shell":
            c.save(); c.translate(x, y - 10)
            c.move_to(-18, 6); c.curve_to(-18, -22, 18, -22, 18, 6); c.close_path()
            setc(c, hexc("ffb3c7")); c.fill_preserve(); setc(c, hexc("e07a98")); c.set_line_width(3); c.stroke()
            c.restore()
        else:
            c.save(); c.translate(x, y - 12); c.rotate(0.3)
            for i in range(5):
                a = i * 2 * math.pi / 5 - math.pi / 2
                c.line_to(math.cos(a) * 20, math.sin(a) * 20)
                a2 = a + math.pi / 5
                c.line_to(math.cos(a2) * 9, math.sin(a2) * 9)
            c.close_path(); setc(c, ORANGE); c.fill(); c.restore()
    # foam at the shoreline
    for k in range(3):
        circle(c, xi - 14 + k * 14, level_y + 2 + math.sin(t * 4 + k) * 2, 7, (1, 1, 1, 0.85))
    return sand_y, xi


def s2_what(c, seg, t):
    L = seg["lines"]
    # water level: low -> rising during line1 -> high -> falling during line2 -> gently oscillate
    LOW, HIGH = 540, 380
    r0, r1 = L[1]["start"], L[1]["end"]
    f0, f1 = L[2]["start"], L[2]["end"]
    if t < r0:
        lv = LOW
    elif t < r1:
        lv = LOW + (HIGH - LOW) * ease((t - r0) / (r1 - r0))
    elif t < f0:
        lv = HIGH
    elif t < f1:
        lv = HIGH + (LOW - HIGH) * ease((t - f0) / (f1 - f0))
    else:
        ph = (t - f1) / 3.0
        lv = (LOW + HIGH) / 2 + (LOW - HIGH) / 2 * math.cos(ph * math.pi)
    sand_y, xi = beach_scene(c, t, lv, False)
    idx, speaking = cur_line(seg, t)
    wave_baby(c, min(xi - 110, 380), lv - 70, 0.8, t, talk=speaking)
    # level gauge
    gx = 1180
    c.set_line_width(6); setc(c, hexc("ffffff", 0.9)); rrect(c, gx - 22, 160, 44, 260, 22); c.fill()
    frac = (LOW - lv) / (LOW - HIGH)
    rrect(c, gx - 16, 414 - 248 * frac, 32, 248 * frac + 0.1, 16); setc(c, SEA1); c.fill()
    text(c, "水位", gx, 135, 26)
    if r0 <= t < f0:
        label(c, "漲潮 ↑", 950, 200, 48, bg=hexc("c7f0ff"), fg=hexc("1f6fd1"), scale=pop((t - r0) / 0.5))
    elif f0 <= t < f1 + 0.6:
        label(c, "退潮 ↓", 950, 200, 48, bg=hexc("fff1c7"), fg=hexc("d9480f"), scale=pop((t - f0) / 0.5))
    elif t >= f1 + 0.6:
        label(c, "一漲一退 = 潮汐", 860, 200, 46, bg=YELLOW, scale=pop((t - f1 - 0.6) / 0.5))


def space_moon_scene(c, seg, t, a_near, a_far, show_arrows, rot=0.0, earth_x=500):
    space_bg(c, t)
    ex, ey, er = earth_x, 380, 120
    ocean_shell(c, ex, ey, er, a_near, a_far, 0.0, t)
    earth(c, ex, ey, er, t, rot=rot, show_face=True)
    moon(c, 1080, 380, 75, t)
    if show_arrows > 0:
        for dy in (-60, 0, 60):
            arrow(c, 990, 380 + dy * 0.5, ex + er + 60 + a_near * 0.6, 380 + dy, hexc("ffe066", show_arrows),
                  lw=7, head=24, dash=[18, 14], t=t)
    return ex, ey, er


def s3_moon(c, seg, t):
    L = seg["lines"]
    idx, speaking = cur_line(seg, t)
    near = 70 * ease((t - L[2]["start"]) / 2.0)
    far = 55 * ease((t - L[3]["start"]) / 2.0)
    arrows = ease((t - L[1]["start"]) / 1.0)
    ex, ey, er = space_moon_scene(c, seg, t, near, far, arrows)
    if idx >= 1:
        label(c, "引力：看不見的拉力", 1040, 230, 34, bg=YELLOW, scale=pop(line_t(seg, 1, t)[0] / 0.5))
        # magnet icon
        c.save(); c.translate(1080, 520); c.scale(0.9, 0.9)
        c.set_line_width(26); setc(c, RED); c.arc(0, 0, 40, 0, math.pi); c.stroke()
        setc(c, (0.85, 0.85, 0.9, 1)); c.rectangle(-53, -30, 26, 30); c.fill(); c.rectangle(27, -30, 26, 30); c.fill()
        c.restore()
    if idx >= 2:
        label(c, "漲潮！", ex + er + 110, 250, 38, bg=hexc("c7f0ff"), fg=hexc("1f6fd1"),
              scale=pop(line_t(seg, 2, t)[0] / 0.5))
    if idx >= 3:
        label(c, "第二個大水包", ex - er - 60, 250, 34, bg=hexc("c7f0ff"), fg=hexc("1f6fd1"),
              scale=pop(line_t(seg, 3, t)[0] / 0.5))
    wave_baby(c, 140, 610, 0.55, t, talk=speaking)


def house_on_earth(c, ex, ey, er, ang):
    hx, hy = ex + math.cos(ang) * (er + 4), ey + math.sin(ang) * (er + 4)
    c.save(); c.translate(hx, hy); c.rotate(ang + math.pi / 2)
    setc(c, hexc("fff4e0")); c.rectangle(-14, -22, 28, 22); c.fill()
    setc(c, RED); c.move_to(-19, -20); c.line_to(0, -38); c.line_to(19, -20); c.close_path(); c.fill()
    setc(c, hexc("8d5524")); c.rectangle(-4, -12, 8, 12); c.fill()
    c.restore()


def s4_twice(c, seg, t):
    L = seg["lines"]
    idx, speaking = cur_line(seg, t)
    lt = t - seg["start"]
    period = 9.0
    rot = (lt / period) * 2 * math.pi if lt > 0 else 0
    ex, ey, er = space_moon_scene(c, seg, t, 70, 55, 0.0, rot=rot)
    ang = math.pi * 0.5 + rot
    house_on_earth(c, ex, ey, er + 2, ang)
    # count tides: each time house angle passes 0 or pi
    passes = int((rot - (-math.pi / 2) + 0) // math.pi)  # house starts at +pi/2 (bottom)
    passes = max(0, int((rot + math.pi / 2) // math.pi))
    if idx >= 1:
        txt = f"漲潮次數：{passes}"
        label(c, txt, 1040, 200, 36, bg=YELLOW)
        cosv = math.cos(ang)
        if abs(cosv) > 0.93:
            label(c, "漲潮囉！", ex + math.cos(ang) * (er + 120), ey + math.sin(ang) * (er + 90) - 30, 30,
                  bg=hexc("c7f0ff"), fg=hexc("1f6fd1"))
    if idx >= 2:
        label(c, "一天：2 次漲潮、2 次退潮", W / 2, 70, 40, bg=hexc("ffd6e7"), scale=pop(line_t(seg, 2, t)[0] / 0.5))
    if idx >= 3:
        p = pop(line_t(seg, 3, t)[0] / 0.5)
        c.save(); c.translate(1060, 560); c.scale(p, p)
        circle(c, 0, 0, 62, WHITE, BLACK, 6)
        c.set_line_width(7); setc(c, BLACK); c.set_line_cap(cairo.LINE_CAP_ROUND)
        a = -math.pi / 2 + t * 0.8
        c.move_to(0, 0); c.line_to(math.cos(a) * 45, math.sin(a) * 45); c.stroke()
        c.move_to(0, 0); c.line_to(0, -30); c.stroke()
        c.restore()
        label(c, "每天晚約 50 分鐘", 1060, 660, 30, bg=YELLOW, scale=p)
    wave_baby(c, 140, 610, 0.55, t, talk=speaking)


def s5_spring_neap(c, seg, t):
    L = seg["lines"]
    idx, speaking = cur_line(seg, t)
    space_bg(c, t)
    neap = t >= L[3]["start"]
    sw = ease((t - L[3]["start"]) / 1.2) if neap else 0.0
    ex, ey, er = 640, 420, 95
    # sun on the left
    sun(c, 150, 420, 70, t)
    # moon position: right (spring) -> top (neap)
    ma = -math.pi / 2 * sw
    mx, my = ex + math.cos(ma) * 330, ey + math.sin(ma) * 225
    spring_p = ease((t - L[1]["start"]) / 1.5)
    if not neap:
        a_near = 45 + 55 * spring_p
        ocean_shell(c, ex, ey, er, a_near, a_near * 0.85, 0.0, t)
    else:
        a = 100 - 60 * sw
        ocean_shell(c, ex, ey, er, a, a * 0.85, ma, t)
    earth(c, ex, ey, er, t, rot=t * 0.2)
    moon(c, mx, my, 55, t)
    if idx >= 0:
        arrow(c, 240, 420, ex - er - 40, 420, hexc("ffa94d", 0.9), lw=6, head=20, dash=[16, 12], t=t)
        label(c, "太陽的引力（比較小）", 280, 250, 26, bg=hexc("fff1c7"), scale=pop(line_t(seg, 0, t)[0] / 0.5))
    if 1 <= idx < 3 or (idx == 2):
        arrow(c, mx - 70, my, ex + er + 110, ey, hexc("ffe066", 0.9), lw=6, head=20, dash=[16, 12], t=t)
    if 1 <= idx <= 2:
        label(c, "排成一直線 → 大潮", W / 2, 75, 46, bg=hexc("ff8fa3"), fg=WHITE, scale=pop(line_t(seg, 1, t)[0] / 0.5))
        c.set_line_width(4); c.set_dash([8, 10]); setc(c, (1, 1, 1, 0.6))
        c.move_to(150, 420); c.line_to(mx, my); c.stroke(); c.set_dash([])
    if idx == 2:
        p = pop(line_t(seg, 2, t)[0] / 0.5)
        # new moon / full moon icons
        for k, (nm, full) in enumerate((("新月", False), ("滿月", True))):
            x = 960 + k * 140
            c.save(); c.translate(x, 250); c.scale(p, p)
            circle(c, 0, 0, 38, hexc("fff3a6") if full else hexc("3d3d6b"), hexc("e8c547"), 4)
            c.restore()
            label(c, nm, x, 315, 26, scale=p)
    if idx >= 3:
        if idx == 3:
            arrow(c, mx, my + 60, ex, ey - er - 80, hexc("ffe066", 0.9), lw=6, head=20, dash=[16, 12], t=t)
        label(c, "站成直角 → 小潮", 960, 75, 46, bg=hexc("74c0fc"), fg=WHITE, scale=pop(line_t(seg, 3, t)[0] / 0.5))
        p = pop((t - L[3]["start"] - 3.0) / 0.5)
        for k, (nm, side) in enumerate((("上弦月", 1), ("下弦月", -1))):
            x = 1000 + k * 150
            c.save(); c.translate(x, 250); c.scale(p, p)
            circle(c, 0, 0, 38, hexc("3d3d6b"), hexc("e8c547"), 4)
            c.arc(0, 0, 36, -math.pi / 2, math.pi / 2) if side > 0 else c.arc(0, 0, 36, math.pi / 2, 1.5 * math.pi)
            c.close_path(); setc(c, hexc("fff3a6")); c.fill()
            c.restore()
            label(c, nm, x, 315, 26, scale=p)
    wave_baby(c, 110, 620, 0.5, t, talk=speaking)


def crab(c, x, y, s, t):
    c.save(); c.translate(x + math.sin(t * 3) * 25, y); c.scale(s, s)
    c.set_line_width(6); setc(c, hexc("e8590c")); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for sx in (-1, 1):
        for k in range(3):
            c.move_to(sx * 30, 5 + k * 8); c.line_to(sx * (55 + k * 4), 22 + k * 10 + math.sin(t * 12 + k) * 4); c.stroke()
        c.move_to(sx * 25, -15); c.line_to(sx * 48, -40); c.stroke()
        circle(c, sx * 52, -48, 14, hexc("ff6b35"))
    c.save(); c.scale(1.3, 0.85); circle(c, 0, 0, 34, hexc("ff6b35"), hexc("e8590c"), 4); c.restore()
    face(c, 0, -2, 30, t, False, 0.7)
    c.restore()


def hermit(c, x, y, s, t):
    c.save(); c.translate(x - math.sin(t * 1.5) * 15, y); c.scale(s, s)
    # shell spiral
    c.save(); c.translate(15, -10)
    circle(c, 0, 0, 40, hexc("c08552"), hexc("8d5524"), 4)
    c.set_line_width(4); setc(c, hexc("8d5524"))
    for i in range(40):
        a = i * 0.35; r = 3 + i * 0.85
        (c.move_to if i == 0 else c.line_to)(math.cos(a) * r, math.sin(a) * r)
    c.stroke(); c.restore()
    circle(c, -32, 10, 20, hexc("ff8787"))
    circle(c, -38, 2, 5, BLACK)
    c.set_line_width(5); setc(c, hexc("ff8787"))
    for k in range(3):
        c.move_to(-30 + k * 10, 25); c.line_to(-42 + k * 10, 42 + math.sin(t * 10 + k) * 3); c.stroke()
    c.restore()


def anemone(c, x, y, s, t):
    c.save(); c.translate(x, y); c.scale(s, s)
    setc(c, hexc("da77f2")); c.set_line_width(10); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(9):
        a = -math.pi + i * math.pi / 8
        sw = math.sin(t * 2 + i) * 0.15
        c.move_to(0, -10)
        c.curve_to(math.cos(a + sw) * 25, -10 + math.sin(a) * 25, math.cos(a + sw) * 40,
                   -10 + math.sin(a) * 40 - 10, math.cos(a + sw * 2) * 50, -10 + math.sin(a) * 50)
        c.stroke()
    rrect(c, -28, -15, 56, 40, 14); setc(c, hexc("be4bdb")); c.fill()
    face(c, 0, 5, 22, t, False, 1.7)
    c.restore()


def snail(c, x, y, s, t):
    c.save(); c.translate(x + math.sin(t * 0.8) * 20, y); c.scale(s, s)
    c.move_to(-50, 20); c.curve_to(-40, 0, 40, 0, 60, 20); c.close_path()
    setc(c, hexc("94d82d")); c.fill()
    c.move_to(-25, 15); c.line_to(0, -45); c.line_to(25, 15); c.close_path()
    setc(c, hexc("e9c46a")); c.fill_preserve(); setc(c, hexc("b5838d")); c.set_line_width(3); c.stroke()
    for k in range(3):
        c.move_to(-18 + k * 6, 5 - k * 14); c.line_to(18 - k * 6, 5 - k * 14); c.stroke()
    circle(c, 55, 8, 4, BLACK)
    c.restore()


def barnacle(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    for dx in (-30, 0, 30):
        c.move_to(dx - 16, 10); c.line_to(dx - 8, -14); c.line_to(dx + 8, -14); c.line_to(dx + 16, 10); c.close_path()
        setc(c, hexc("f1f3f5")); c.fill_preserve(); setc(c, hexc("868e96")); c.set_line_width(3); c.stroke()
    c.restore()


def s6_creatures(c, seg, t):
    L = seg["lines"]
    idx, speaking = cur_line(seg, t)
    sky_bg(c)
    sun(c, 1160, 90, 45, t)
    # zone bands
    setc(c, hexc("ffe8b0")); c.rectangle(0, 330, W, H - 330); c.fill()
    sea(c, 600, t, 8)
    # rocks
    for x, y, rx, ry in ((200, 520, 110, 55), (620, 560, 140, 60), (1050, 520, 120, 55), (420, 420, 90, 40), (880, 420, 90, 40)):
        c.save(); c.translate(x, y); c.scale(rx / 50, ry / 50)
        circle(c, 0, 0, 50, hexc("a5aeb8"), hexc("6b7785"), 3); c.restore()
    # tide markers
    c.set_line_width(4); c.set_dash([14, 10]); setc(c, hexc("1f6fd1", 0.8))
    c.move_to(0, 345); c.line_to(W, 345); c.stroke(); c.set_dash([])
    text(c, "漲潮線", 70, 320, 24, hexc("1f6fd1"))
    text(c, "退潮線", 70, 580, 24, hexc("1f6fd1"))
    if idx >= 0:
        label(c, "潮間帶", W / 2, 285, 46, bg=hexc("c7f0ff"), fg=hexc("1f6fd1"), scale=pop(line_t(seg, 0, t)[0] / 0.6))
    if idx >= 1:
        lt, ld = line_t(seg, 1, t)
        names = [("螃蟹", crab, 200, 470, 0.9), ("寄居蟹", hermit, 430, 380, 0.8),
                 ("海葵", anemone, 640, 500, 0.9), ("海螺", snail, 860, 380, 0.75), ("藤壺", barnacle, 1060, 480, 0.9)]
        for k, (nm, fn, x, y, s) in enumerate(names):
            st = ld * (0.22 + k * 0.155)
            p = pop((lt - st) / 0.5) if idx == 1 else 1.0
            if p <= 0.01:
                continue
            c.save(); c.translate(x, y); c.scale(p, p); c.translate(-x, -y)
            if fn is barnacle:
                fn(c, x, y, s)
            else:
                fn(c, x, y, s, t)
            c.restore()
            label(c, nm, x, y + 75, 26, scale=p)
    if idx >= 2:
        p = pop(line_t(seg, 2, t)[0] / 0.5)
        label(c, "輕輕看 不帶走 ♥", W / 2, 170, 44, bg=hexc("ffd6e7"), fg=hexc("c2185b"), scale=p)
    wave_baby(c, 1180, 640, 0.5, t, talk=speaking)


def icon(c, k, x, y, s, t):
    c.save(); c.translate(x, y); c.scale(s, s)
    if k == 0:  # adult + kid holding hands
        for dx, r, h, col in ((-22, 14, 60, hexc("4dabf7")), (22, 10, 38, hexc("ff8787"))):
            circle(c, dx, -h + 5, r, hexc("ffd8a8"))
            rrect(c, dx - r, -h + 5 + r, 2 * r, h - r - 5, 6); setc(c, col); c.fill()
        c.set_line_width(5); setc(c, hexc("ffd8a8")); c.move_to(-10, -25); c.line_to(12, -18); c.stroke()
    elif k == 1:  # clock
        circle(c, 0, -25, 32, WHITE, BLACK, 5)
        c.set_line_width(5); setc(c, BLACK); c.move_to(0, -25); c.line_to(0, -47); c.stroke()
        c.move_to(0, -25); c.line_to(15, -18); c.stroke()
    elif k == 2:  # go back to shore
        sea(c, 0, t, 0, x0=-45, x1=45, foam=False) if False else None
        setc(c, SEA1); rrect(c, -45, -10, 90, 20, 8); c.fill()
        arrow(c, -20, -5, 30, -50, GREEN, lw=9, head=22)
    elif k == 3:  # shoe
        c.move_to(-40, 0); c.line_to(-40, -35); c.line_to(-10, -35); c.curve_to(0, -15, 30, -15, 40, -8)
        c.line_to(40, 0); c.close_path(); setc(c, hexc("845ef7")); c.fill()
        setc(c, BLACK); c.rectangle(-40, 0, 80, 7); c.fill()
    else:  # no swimming alone
        circle(c, 0, -25, 34, WHITE, RED, 7)
        setc(c, SEA1); c.set_line_width(6)
        c.move_to(-22, -20)
        for xx in range(-22, 24, 4):
            c.line_to(xx, -20 + math.sin(xx / 5) * 4)
        c.stroke()
        setc(c, RED); c.set_line_width(7); c.move_to(-24, -49); c.line_to(24, -1); c.stroke()
    c.restore()


def s7_safety(c, seg, t):
    L = seg["lines"]
    idx, speaking = cur_line(seg, t)
    sky_bg(c, hexc("b2f2bb"), hexc("f4fce3"))
    sea(c, 650, t, 6)
    label(c, "海邊安全小守則", W / 2, 70, 50, bg=hexc("ff8787"), fg=WHITE, scale=pop((t - seg["start"]) / 0.6))
    rules = ["有大人陪伴", "先查漲退潮時間", "漲潮就回岸上", "穿防滑鞋", "不自己下水"]
    for k, r in enumerate(rules):
        li = k + 1
        if idx < li:
            continue
        p = pop(line_t(seg, li, t)[0] / 0.5) if idx == li else 1.0
        row, col = divmod(k, 3)
        x = 270 + col * 330 + (165 if row == 1 else 0)
        y = 250 + row * 230
        c.save(); c.translate(x, y); c.scale(p, p)
        rrect(c, -145, -95, 290, 190, 28)
        setc(c, WHITE); c.fill_preserve()
        setc(c, hexc("ffd43b") if idx == li else hexc("dee2e6")); c.set_line_width(8); c.stroke()
        circle(c, -115, -70, 24, hexc("ff8787"))
        text(c, str(k + 1), -115, -72, 30, WHITE)
        icon(c, k, 0, 15, 1.0, t)
        text(c, r, 0, 60, 32)
        c.restore()
    wave_baby(c, 1170, 590, 0.6, t, talk=speaking, buoy=True)


def s8_quiz(c, seg, t):
    L = seg["lines"]
    idx, speaking = cur_line(seg, t)
    sky_bg(c, hexc("ffe8cc"), hexc("fff9db"))
    # confetti dots
    import random
    rnd = random.Random(3)
    for i in range(40):
        x = rnd.random() * W; y = math.fmod(rnd.random() * H + t * 40 * (0.5 + rnd.random()), H)
        circle(c, x, y, 5, hexc(rnd.choice(["ff8787", "74c0fc", "ffd43b", "8ce99a", "da77f2"]), 0.7))
    if idx <= 0:
        p = pop((t - seg["start"]) / 0.7)
        c.save(); c.translate(W / 2, 300); c.scale(p, p)
        text(c, "小問答時間！", 0, 0, 90, hexc("ff7a59"), outline=WHITE, ow=16)
        c.restore()
        wave_baby(c, W / 2, 520, 1.0, t, talk=speaking, wave_hand=True)
        return
    q = (idx - 1) // 2
    qs = ["海水慢慢上升，叫做什麼？", "主要是誰在拉海水？", "一天大約有幾次漲潮？", "排成一直線時是大潮還是小潮？"]
    ans = ["漲潮！", "月亮的引力！", "兩次！", "大潮！"]
    label(c, f"第 {q + 1} 題", W / 2, 90, 40, bg=hexc("845ef7"), fg=WHITE)
    rrect(c, 140, 150, W - 280, 170, 30); setc(c, WHITE); c.fill_preserve()
    setc(c, hexc("845ef7")); c.set_line_width(8); c.stroke()
    text(c, qs[q], W / 2, 235, 50)
    qline = L[1 + q * 2]
    if idx == 1 + q * 2:
        # countdown during the pause
        cd = t - qline["end"] - 0.2
        if cd >= 0:
            n = 3 - int(cd)
            if n >= 1:
                p = pop(math.fmod(cd, 1.0) / 0.4)
                c.save(); c.translate(W / 2, 450); c.scale(p, p)
                circle(c, 0, 0, 80, hexc("ffd43b"), hexc("f08c00"), 8)
                text(c, str(n), 0, -4, 90, WHITE, outline=hexc("f08c00"), ow=8)
                c.restore()
        else:
            text(c, "想一想…", W / 2, 450, 46, hexc("845ef7"))
    else:
        lt = t - L[2 + q * 2]["start"]
        p = pop(lt / 0.5)
        c.save(); c.translate(W / 2, 450); c.scale(p, p)
        rrect(c, -260, -70, 520, 140, 70); setc(c, hexc("8ce99a")); c.fill()
        text(c, ans[q], 0, -4, 64, hexc("2b8a3e"), outline=WHITE, ow=10)
        c.restore()
        for k in range(5):
            a = k * 2 * math.pi / 5 + t
            rr = 300 * min(1, lt * 2)
            sx, sy = W / 2 + math.cos(a) * rr, 450 + math.sin(a) * rr * 0.4
            c.save(); c.translate(sx, sy); c.rotate(t * 2)
            for i in range(5):
                aa = i * 2 * math.pi / 5 - math.pi / 2
                c.line_to(math.cos(aa) * 20, math.sin(aa) * 20)
                aa2 = aa + math.pi / 5
                c.line_to(math.cos(aa2) * 9, math.sin(aa2) * 9)
            c.close_path(); setc(c, hexc("ffd43b")); c.fill(); c.restore()
    wave_baby(c, 150, 600, 0.6, t, talk=speaking)


def s9_outro(c, seg, t):
    idx, speaking = cur_line(seg, t)
    sky_bg(c, hexc("ffa8a8"), hexc("ffe066"))
    lt = t - seg["start"]
    c.save(); c.arc(W / 2, 520, 120, 0, 2 * math.pi); setc(c, hexc("ff922b", 0.9)); c.fill(); c.restore()
    sea(c, 520, t, 10, col1=hexc("748ffc"), col2=hexc("4263eb"))
    moon(c, 980, 300, 65, t)
    earth(c, 760, 330, 70, t, rot=t * 0.3)
    wave_baby(c, 380, 470, 1.0, t, talk=speaking, wave_hand=True)
    p = pop((t - seg["lines"][-1]["start"]) / 0.6)
    if p > 0:
        c.save(); c.translate(W / 2, 140); c.scale(p, p)
        text(c, "下次見！掰掰～", 0, 0, 84, hexc("ff6b6b"), outline=WHITE, ow=16)
        c.restore()
    else:
        label(c, "今天學會了：潮汐的祕密 ★", W / 2, 120, 44, bg=WHITE, scale=pop(lt / 0.6))


SCENES = {"s1_intro": s1_intro, "s2_what": s2_what, "s3_moon": s3_moon, "s4_twice": s4_twice,
          "s5_spring_neap": s5_spring_neap, "s6_creatures": s6_creatures, "s7_safety": s7_safety,
          "s8_quiz": s8_quiz, "s9_outro": s9_outro}


def subtitle(c, seg, t):
    for ln in seg["lines"]:
        if ln["start"] - 0.1 <= t <= ln["end"] + 0.25:
            lines = wrap(c, ln["text"], 34, W - 260)
            h = 20 + 48 * len(lines)
            y0 = H - 30 - h
            rrect(c, 110, y0, W - 220, h, 22); setc(c, (0.1, 0.1, 0.25, 0.62)); c.fill()
            for i, s in enumerate(lines):
                text(c, s, W / 2, y0 + 34 + i * 48, 34, WHITE)
            return


def badge(c, seg, t):
    if seg["id"] in ("s1_intro", "s9_outro"):
        return
    s = seg["title"]
    w = text_w(c, s, 26) + 40
    rrect(c, 20, 18, w, 46, 23); setc(c, (1, 1, 1, 0.85)); c.fill()
    text(c, s, 40, 41, 26, hexc("1f6fd1"), align="left")


def render_frame(c, t):
    seg = TL["segments"][-1]
    for s in TL["segments"]:
        if s["start"] <= t < s["end"]:
            seg = s; break
    c.save()
    SCENES[seg["id"]](c, seg, t)
    c.restore()
    badge(c, seg, t)
    subtitle(c, seg, t)
    # transitions
    a = 0.0
    a = max(a, 1 - (t - seg["start"]) / 0.35)
    a = max(a, 1 - (seg["end"] - t) / 0.25) if seg is not TL["segments"][-1] else max(a, 1 - (seg["end"] - t) / 1.0)
    if a > 0:
        c.set_source_rgba(1, 1, 1, min(1, a) * (0.85 if seg is not TL["segments"][-1] or t < seg["end"] - 1 else 1))
        c.paint()


def main():
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(surf)
    c.set_antialias(cairo.ANTIALIAS_GOOD)
    if "--still" in sys.argv:
        for i, a in enumerate(sys.argv[sys.argv.index("--still") + 1:]):
            c.set_source_rgb(1, 1, 1); c.paint()
            render_frame(c, float(a))
            surf.write_to_png(os.path.join(BUILD, f"still_{i:02d}.png"))
        return
    dur = TL["duration"]
    nframes = int(dur * FPS)
    out = os.path.join(HERE, "tide_for_kids.mp4")
    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
         "-i", "-", "-i", os.path.join(BUILD, "audio.wav"),
         "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", out],
        stdin=subprocess.PIPE)
    for f in range(nframes):
        c.set_source_rgb(1, 1, 1); c.paint()
        render_frame(c, f / FPS)
        surf.flush()
        ff.stdin.write(surf.get_data())
        if f % (FPS * 20) == 0:
            print(f"{f / FPS:.0f}s / {dur:.0f}s", flush=True)
    ff.stdin.close(); ff.wait()
    print("wrote", out)


if __name__ == "__main__":
    main()
