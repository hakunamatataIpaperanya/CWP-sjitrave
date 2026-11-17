#!/usr/bin/env python3
"""Generate the animated pixel-art SVGs used by README.md (42 Bangkok · Discovery Piscine).

Run:  python3 assets/make_assets.py   (writes the .svg files next to this script)
"""
import math
import os
import random
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)


def n(v):
    if isinstance(v, float):
        if v.is_integer():
            return str(int(v))
        return f"{v:.2f}".rstrip("0").rstrip(".")
    return str(v)


# ------------------------------------------------------------------ pixel font
_U = {
    'A': ".###. #...# #...# ##### #...# #...# #...#",
    'B': "####. #...# #...# ####. #...# #...# ####.",
    'C': ".###. #...# #.... #.... #.... #...# .###.",
    'D': "####. #...# #...# #...# #...# #...# ####.",
    'E': "##### #.... #.... ####. #.... #.... #####",
    'F': "##### #.... #.... ####. #.... #.... #....",
    'G': ".###. #...# #.... #.### #...# #...# .####",
    'H': "#...# #...# #...# ##### #...# #...# #...#",
    'I': ".###. ..#.. ..#.. ..#.. ..#.. ..#.. .###.",
    'J': "..### ...#. ...#. ...#. #..#. #..#. .##..",
    'K': "#...# #..#. #.#.. ##... #.#.. #..#. #...#",
    'L': "#.... #.... #.... #.... #.... #.... #####",
    'M': "#...# ##.## #.#.# #.#.# #...# #...# #...#",
    'N': "#...# #...# ##..# #.#.# #..## #...# #...#",
    'O': ".###. #...# #...# #...# #...# #...# .###.",
    'P': "####. #...# #...# ####. #.... #.... #....",
    'Q': ".###. #...# #...# #...# #.#.# #..#. .##.#",
    'R': "####. #...# #...# ####. #.#.. #..#. #...#",
    'S': ".#### #.... #.... .###. ....# ....# ####.",
    'T': "##### ..#.. ..#.. ..#.. ..#.. ..#.. ..#..",
    'U': "#...# #...# #...# #...# #...# #...# .###.",
    'V': "#...# #...# #...# #...# #...# .#.#. ..#..",
    'W': "#...# #...# #...# #.#.# #.#.# #.#.# .#.#.",
    'X': "#...# #...# .#.#. ..#.. .#.#. #...# #...#",
    'Y': "#...# #...# .#.#. ..#.. ..#.. ..#.. ..#..",
    'Z': "##### ....# ...#. ..#.. .#... #.... #####",
    '0': ".###. #...# #..## #.#.# ##..# #...# .###.",
    '1': "..#.. .##.. ..#.. ..#.. ..#.. ..#.. .###.",
    '2': ".###. #...# ....# ...#. ..#.. .#... #####",
    '3': "##### ...#. ..#.. ...#. ....# #...# .###.",
    '4': "...#. ..##. .#.#. #..#. ##### ...#. ...#.",
    '5': "##### #.... ####. ....# ....# #...# .###.",
    '6': "..##. .#... #.... ####. #...# #...# .###.",
    '7': "##### ....# ...#. ..#.. .#... .#... .#...",
    '8': ".###. #...# #...# .###. #...# #...# .###.",
    '9': ".###. #...# #...# .#### ....# ...#. .##..",
    ' ': "..... ..... ..... ..... ..... ..... .....",
    '.': "..... ..... ..... ..... ..... .##.. .##..",
    ',': "..... ..... ..... ..... .##.. .##.. .#...",
    '!': "..#.. ..#.. ..#.. ..#.. ..#.. ..... ..#..",
    '?': ".###. #...# ....# ...#. ..#.. ..... ..#..",
    '-': "..... ..... ..... .###. ..... ..... .....",
    '+': "..... ..#.. ..#.. ##### ..#.. ..#.. .....",
    '=': "..... ..... ##### ..... ##### ..... .....",
    ':': "..... .##.. .##.. ..... .##.. .##.. .....",
    '/': "....# ....# ...#. ..#.. .#... #.... #....",
    '_': "..... ..... ..... ..... ..... ..... #####",
    '$': "..#.. .#### #.#.. .###. ..#.# ####. ..#..",
    '>': ".#... ..#.. ...#. ....# ...#. ..#.. .#...",
    '<': "...#. ..#.. .#... #.... .#... ..#.. ...#.",
    '(': "...#. ..#.. .#... .#... .#... ..#.. ...#.",
    ')': ".#... ..#.. ...#. ...#. ...#. ..#.. .#...",
    '~': "..... ..... .#... #.#.# ...#. ..... .....",
    '*': "..... #.#.# .###. ##### .###. #.#.# .....",
    '#': ".#.#. .#.#. ##### .#.#. ##### .#.#. .#.#.",
    "'": "..#.. ..#.. .#... ..... ..... ..... .....",
    '"': ".#.#. .#.#. ..... ..... ..... ..... .....",
    '·': "..... ..... ..#.. .###. ..#.. ..... .....",
    '♥': "..... .#.#. ##### ##### .###. ..#.. .....",
    '▶': "#.... ##... ###.. ####. ###.. ##... #....",
    '▼': "..... ..... ##### .###. ..#.. ..... .....",
    '[': ".###. .#... .#... .#... .#... .#... .###.",
    ']': ".###. ...#. ...#. ...#. ...#. ...#. .###.",
    '|': "..#.. ..#.. ..#.. ..#.. ..#.. ..#.. ..#..",
}
_L = {
    'a': "..... ..... .###. ....# .#### #...# .#### .....",
    'b': "#.... #.... ####. #...# #...# #...# ####. .....",
    'c': "..... ..... .###. #.... #.... #.... .###. .....",
    'd': "....# ....# .#### #...# #...# #...# .#### .....",
    'e': "..... ..... .###. #...# ##### #.... .###. .....",
    'f': "..##. .#... ####. .#... .#... .#... .#... .....",
    'g': "..... ..... .#### #...# #...# .#### ....# .###.",
    'h': "#.... #.... ####. #...# #...# #...# #...# .....",
    'i': "..#.. ..... .##.. ..#.. ..#.. ..#.. .###. .....",
    'j': "...#. ..... ..##. ...#. ...#. ...#. #..#. .##..",
    'k': "#.... #.... #..#. #.#.. ##... #.#.. #..#. .....",
    'l': ".##.. ..#.. ..#.. ..#.. ..#.. ..#.. .###. .....",
    'm': "..... ..... ##.#. #.#.# #.#.# #.#.# #...# .....",
    'n': "..... ..... ####. #...# #...# #...# #...# .....",
    'o': "..... ..... .###. #...# #...# #...# .###. .....",
    'p': "..... ..... ####. #...# #...# ####. #.... #....",
    'q': "..... ..... .#### #...# #...# .#### ....# ....#",
    'r': "..... ..... #.##. ##..# #.... #.... #.... .....",
    's': "..... ..... .#### #.... .###. ....# ####. .....",
    't': ".#... .#... ####. .#... .#... .#..# ..##. .....",
    'u': "..... ..... #...# #...# #...# #..## .##.# .....",
    'v': "..... ..... #...# #...# #...# .#.#. ..#.. .....",
    'w': "..... ..... #...# #...# #.#.# #.#.# .#.#. .....",
    'x': "..... ..... #...# .#.#. ..#.. .#.#. #...# .....",
    'y': "..... ..... #...# #...# #...# .#### ....# .###.",
    'z': "..... ..... ##### ...#. ..#.. .#... ##### .....",
}
FONT = {k: v.split() for k, v in {**_U, **_L}.items()}
ADV = 6


def _runs(rows, x0, y0, sc, on="#"):
    d = []
    for gy, row in enumerate(rows):
        gx = 0
        while gx < len(row):
            if row[gx] == on:
                s = gx
                while gx < len(row) and row[gx] == on:
                    gx += 1
                w = (gx - s) * sc
                d.append(f"M{n(x0 + s * sc)} {n(y0 + gy * sc)}h{n(w)}v{n(sc)}h{n(-w)}z")
            else:
                gx += 1
    return "".join(d)


def text_d(s, x, y, sc):
    return "".join(_runs(FONT.get(ch, FONT["?"]), x + i * ADV * sc, y, sc) for i, ch in enumerate(s))


def tw(s, sc):
    return (len(s) * ADV - 1) * sc


def _a(attrs):
    return " " + attrs if attrs else ""


def text(s, x, y, sc, fill, attrs=""):
    return f'<path d="{text_d(s, x, y, sc)}" fill="{fill}"{_a(attrs)}/>'


def ctext(s, cx, y, sc, fill, attrs=""):
    return text(s, round(cx - tw(s, sc) / 2), y, sc, fill, attrs)


def stext(s, x, y, sc, fill, shadow, off=None, attrs=""):
    off = sc if off is None else off
    return f'<g{_a(attrs)}>{text(s, x + off, y + off, sc, shadow)}{text(s, x, y, sc, fill)}</g>'


def cstext(s, cx, y, sc, fill, shadow, off=None, attrs=""):
    return stext(s, round(cx - tw(s, sc) / 2), y, sc, fill, shadow, off, attrs)


# ------------------------------------------------------------------ primitives
def rect(x, y, w, h, fill, attrs=""):
    return f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" fill="{fill}"{_a(attrs)}/>'


def sprite(rows, pal, x0, y0, sc):
    layers = {}
    for gy, row in enumerate(rows):
        gx = 0
        while gx < len(row):
            c = row[gx]
            if c in pal:
                s = gx
                while gx < len(row) and row[gx] == c:
                    gx += 1
                w = (gx - s) * sc
                layers.setdefault(pal[c], []).append(
                    f"M{n(x0 + s * sc)} {n(y0 + gy * sc)}h{n(w)}v{n(sc)}h{n(-w)}z")
            else:
                gx += 1
    return "".join(f'<path d="{"".join(v)}" fill="{k}"/>' for k, v in layers.items())


def ppath(x, y, w, h, s=4, offs=(3, 1, 1)):
    """Rectangle with stair-stepped (pixel-rounded) corners."""
    o = list(offs) + [0]
    m = len(offs)
    pts = [(x + o[0] * s, y), (x + w - o[0] * s, y)]
    for k in range(m):
        pts += [(x + w - o[k] * s, y + (k + 1) * s), (x + w - o[k + 1] * s, y + (k + 1) * s)]
    pts.append((x + w, y + h - m * s))
    for k in reversed(range(m)):
        pts += [(x + w - o[k] * s, y + h - (k + 1) * s), (x + w - o[k] * s, y + h - k * s)]
    pts.append((x + o[0] * s, y + h))
    for k in range(m):
        pts += [(x + o[k] * s, y + h - (k + 1) * s), (x + o[k + 1] * s, y + h - (k + 1) * s)]
    pts.append((x, y + m * s))
    for k in reversed(range(m)):
        pts += [(x + o[k] * s, y + (k + 1) * s), (x + o[k] * s, y + k * s)]
    return "M" + "L".join(f"{n(a)} {n(b)}" for a, b in pts) + "Z"


def cells_d(cells, s, ox=0, oy=0):
    rows = {}
    for i, j in cells:
        rows.setdefault(j, set()).add(i)
    d = []
    for j in sorted(rows):
        xs = sorted(rows[j])
        k = 0
        while k < len(xs):
            a = xs[k]
            while k + 1 < len(xs) and xs[k + 1] == xs[k] + 1:
                k += 1
            w = (xs[k] - a + 1) * s
            d.append(f"M{n(ox + a * s)} {n(oy + j * s)}h{n(w)}v{n(s)}h{n(-w)}z")
            k += 1
    return "".join(d)


def disc_cells(r, s, inner=0.0, pred=None):
    R = int(math.ceil(r / s)) + 1
    out = []
    for j in range(-R, R):
        for i in range(-R, R):
            px, py = (i + 0.5) * s, (j + 0.5) * s
            dd = math.hypot(px, py)
            if inner <= dd <= r and (pred is None or pred(px, py)):
                out.append((i, j))
    return out


def disc_anim(attr, base, pairs, T):
    kt, vals = ["0"], [n(base)]
    for tt, v in pairs:
        kt.append(f"{tt / T:.4f}")
        vals.append(n(v))
    kt.append("1")
    vals.append(n(pairs[-1][1]))
    return (f'<animate attributeName="{attr}" dur="{T:.2f}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="{";".join(kt)}" values="{";".join(vals)}"/>')


REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
BLINK = ".bl{animation:bl 1.2s steps(1) infinite}@keyframes bl{50%{opacity:0}}"
TWINKLE = (".t0{animation:tw 2.6s steps(2) infinite}.t1{animation:tw 3.4s steps(2) infinite}"
           ".t2{animation:tw 4.2s steps(3) infinite}.t3{animation:tw 1.8s steps(2) infinite}"
           "@keyframes tw{0%,100%{opacity:1}50%{opacity:.15}}")


def svg(W, H, body, css="", defs="", label=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'shape-rendering="crispEdges" role="img" aria-label="{label}">'
            f'<title>{label}</title><style>{css}{REDUCED}</style><defs>{defs}</defs>{body}</svg>\n')


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{name:16s} {len(content) / 1024:6.1f} KB")


# ------------------------------------------------------------------ sprites
SNEK = [
    "..............KKKKK....",
    "............KKGGGGGKK..",
    "...........KGGGGGGGGGK.",
    "...........KGGGGGGGGGGK",
    "..........KSSSSSSBBBBSK",
    "..........KGGGGGSBWBBSK",
    "..........KGGGGGSBBBBSK",
    "..........KGGGGGGSSSSGK",
    "...........KGGGGGGGGGDK",
    "...........KYYYYYYYYYK.",
    "............KYYYYGKKK..",
    "...........KYYYGGK.....",
    "..........KYYYGGK......",
    ".KK......KYYYGGK.......",
    "KGGKKKKKKYYYGGGKKKK....",
    "KGGGGGGGGGGGGGGGGGGKK..",
    ".KGGDGGGDGGGDGGGDGGGGK.",
    "KGGYYYYYYYYYYYYYYYYYGGK",
    "KKGGGGGGGGGGGGGGGGGGGK.",
    ".KKKKKKKKKKKKKKKKKKKK..",
]
SNEK_PAL = {"K": "#0b0b1e", "G": "#3ddc84", "D": "#1b7f4b", "Y": "#b6ffcf",
            "S": "#ff4fd8", "B": "#38c6ff", "W": "#e8fbff"}
TONGUE = ["....R", "RRRR.", "....R"]


def snek(x, y, sc, tongue=True):
    out = sprite(SNEK, SNEK_PAL, x, y, sc)
    if tongue:
        out += f'<g class="flick">{sprite(TONGUE, {"R": "#ff4757"}, x + 22 * sc, y + 8 * sc, sc)}</g>'
    return out


FLICK = (".flick{animation:flick 3s steps(1) infinite}"
         "@keyframes flick{0%,70%{opacity:0}72%,78%{opacity:1}80%,83%{opacity:0}85%,90%{opacity:1}92%,100%{opacity:0}}")

PIECES = {
    "K": ["....#oo#....", "...#oooo#...", "....#oo#....", "..########..", "..#ohhhho#..",
          "..#oooooo#..", "...#oooo#...", "...#oooo#...", "..#oooooo#..", ".#oooooooo#.",
          ".##########.", "............"],
    "Q": [".#...##...#.", "#o#.#oo#.#o#", ".#o#oooo#o#.", ".#oooooooo#.", "..#ohhhho#..",
          "...#oooo#...", "...#oooo#...", "...#oooo#...", "..#oooooo#..", ".#oooooooo#.",
          ".##########.", "............"],
    "B": [".....##.....", "....#oo#....", "...#oo#o#...", "...#o#oo#...", "...#oooo#...",
          "....#oo#....", "...######...", "....#oo#....", "...#oooo#...", "..#oooooo#..",
          ".##########.", "............"],
    "R": [".##..##..##.", ".#o##oo##o#.", ".#oooooooo#.", "..#ohhhho#..", "..#oooooo#..",
          "..#oooooo#..", "..#oooooo#..", "..#oooooo#..", ".#oooooooo#.", "#oooooooooo#",
          "############", "............"],
    "P": ["............", "............", ".....##.....", "....#oo#....", "....#oo#....",
          ".....##.....", "....#oo#....", "...#oooo#...", "..#oooooo#..", ".#oooooooo#.",
          ".##########.", "............"],
}
KING_PAL = {"#": "#3a2200", "o": "#ffd36e", "h": "#fff4c2"}
FOE_PAL = {"#": "#1a0b2e", "o": "#ff6fa8", "h": "#ffc2dc"}


# ================================================================== BANNER
def banner():
    W, H, P = 960, 400, 4
    r = random.Random(4242)
    css, defs, b = [TWINKLE, BLINK], [], []
    defs.append(f'<clipPath id="fr"><path d="{ppath(0, 0, W, H, 4, (4, 2, 1, 1))}"/></clipPath>')
    b.append('<g clip-path="url(#fr)">')

    # --- sky (banded + dithered)
    bands = [(0, '#0b0a24'), (72, '#100c31'), (128, '#17113e'), (176, '#21154b'), (224, '#2f1957'),
             (256, '#451c61'), (280, '#632366'), (296, '#872c69'), (312, '#ab3b69')]
    for k, (y, c) in enumerate(bands):
        y2 = bands[k + 1][0] if k + 1 < len(bands) else 332
        b.append(rect(0, y, W, y2 - y, c))
    for k in range(1, len(bands)):
        y, c = bands[k]
        defs.append(f'<pattern id="dz{k}" width="8" height="8" patternUnits="userSpaceOnUse">'
                    f'<rect width="4" height="4" fill="{c}"/><rect x="4" y="4" width="4" height="4" fill="{c}"/></pattern>')
        b.append(f'<rect x="0" y="{y - 8}" width="{W}" height="8" fill="url(#dz{k})"/>')

    # --- stars
    for _ in range(120):
        x, y = r.randrange(0, W // P) * P, r.randrange(0, 260 // P) * P
        if (x - 872) ** 2 + (y - 62) ** 2 < 64 ** 2:
            continue
        c = r.choice(['#ffffff', '#d6ecff', '#fff1b8', '#ffc8f2', '#c9b8ff'])
        cls, dl = f"t{r.randrange(4)}", f'style="animation-delay:-{r.uniform(0, 4):.2f}s"'
        if r.random() < 0.12:
            b.append(f'<path class="{cls}" {dl} d="M{x} {y - 4}h4v12h-4zM{x - 4} {y}h12v4h-12z" fill="{c}"/>')
        else:
            b.append(f'<rect class="{cls}" {dl} x="{x}" y="{y}" width="4" height="4" fill="{c}"/>')

    # --- full moon (Loy Krathong vibes)
    mx, my = 872, 62
    css.append(".halo{animation:halo 4s ease-in-out infinite alternate}@keyframes halo{from{opacity:.5}to{opacity:1}}")
    b.append(f'<g class="halo"><path d="{cells_d(disc_cells(56, P, 29), P, mx, my)}" fill="#ffe9b0" opacity=".05"/>'
             f'<path d="{cells_d(disc_cells(42, P, 29), P, mx, my)}" fill="#ffe9b0" opacity=".09"/></g>')
    b.append(f'<path d="{cells_d(disc_cells(28, P), P, mx, my)}" fill="#fff4d6"/>')
    shade = disc_cells(28, P, pred=lambda px, py: math.hypot(px + 9, py + 9) > 27)
    b.append(f'<path d="{cells_d(shade, P, mx, my)}" fill="#f1d9a0"/>')
    craters = [(-3, -3), (-2, -3), (-3, -2), (2, 0), (3, 0), (2, 1), (-1, 3), (0, 3), (1, -5)]
    b.append(f'<path d="{cells_d(craters, P, mx, my)}" fill="#e6cc90"/>')

    # --- shooting star
    trail = "".join(rect(-k * 8, -k * 4, 4, 4, "#fff", f'opacity="{1 - k * 0.13:.2f}"') for k in range(8))
    css.append(".shoot{opacity:0;animation:shoot 8s linear 1.5s infinite}"
               "@keyframes shoot{0%{transform:translate(0,0);opacity:0}1%{opacity:1}"
               "10%{transform:translate(260px,130px);opacity:0}100%{transform:translate(260px,130px);opacity:0}}")
    b.append(f'<g transform="translate(96 24)"><g class="shoot">{trail}</g></g>')

    # --- golden glow behind Wat Arun
    defs.append('<radialGradient id="glow"><stop offset="0" stop-color="#ffb347" stop-opacity=".42"/>'
                '<stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient>')
    defs.append('<radialGradient id="lg"><stop offset="0" stop-color="#ffb347" stop-opacity=".7"/>'
                '<stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient>')
    b.append('<ellipse cx="154" cy="236" rx="180" ry="160" fill="url(#glow)"/>')

    # --- sky lanterns (khom loi) rising behind the skyline
    css.append(".rise{animation:rise 22s linear infinite}"
               "@keyframes rise{0%{transform:translateY(0);opacity:0}6%{opacity:1}72%{opacity:1}100%{transform:translateY(-370px);opacity:0}}"
               ".sway{animation:sway 3.2s ease-in-out infinite alternate}"
               "@keyframes sway{from{transform:translateX(-8px)}to{transform:translateX(8px)}}"
               ".fl{animation:fl .6s steps(2) infinite}@keyframes fl{50%{opacity:.5}}")
    LANT = [".ooo.", "ooooo", "oyyyo", "oyyyo", "oyyyo", ".ooo.", "..f.."]
    for x in [36, 118, 214, 300, 452, 528, 640, 706, 790, 912, 372, 580]:
        sc = r.choice([2, 2, 3])
        dur = r.uniform(18, 30)
        glow = f'<circle cx="{n(2.5 * sc)}" cy="{n(3 * sc)}" r="{n(7 * sc)}" fill="url(#lg)"/>'
        spr = sprite(LANT, {'o': '#ff8a3d', 'y': '#ffd36e', 'f': '#fff3b0'}, 0, 0, sc)
        b.append(f'<g transform="translate({x} 330)"><g class="rise" style="animation-duration:{dur:.1f}s;'
                 f'animation-delay:-{r.uniform(0, dur):.1f}s"><g class="sway" style="animation-delay:-{r.uniform(0, 3):.1f}s">'
                 f'<g class="fl">{glow}</g>{spr}</g></g></g>')

    # --- Wat Arun (temple of dawn) prangs
    BASE = 316
    lights = []

    def prang(cx, tiers):
        out, y = [], BASE
        cl, cd = ('#ffd98a', '#f5b456'), ('#d98c3c', '#c0702a')
        for idx, (hw, h) in enumerate(tiers):
            y -= h * P
            x0, wf, lw = cx - hw * P - 2, (2 * hw + 1) * P, (hw + 1) * P
            out.append(rect(x0, y, lw, h * P, cl[idx % 2]))
            if hw > 0:
                out.append(rect(x0 + lw, y, wf - lw, h * P, cd[idx % 2]))
            if h >= 2:
                out.append(rect(x0, y + h * P - P, wf, P, '#8f4a1c', 'opacity=".45"'))
            if hw >= 3 and r.random() < 0.7:
                lights.append((cx - 2 + r.randint(-hw + 1, hw - 1) * P, y + r.randrange(h) * P))
        out.append(rect(cx - 6, y + 8, 12, 4, '#ffd98a'))
        out.append(rect(cx - 6, y + 4, 4, 4, '#ffd98a'))
        out.append(rect(cx + 2, y + 4, 4, 4, '#ffd98a'))
        return "".join(out)

    sat = [(8, 2), (7, 1), (6, 2), (5, 1), (4, 3), (4, 2), (3, 3), (3, 2), (2, 2), (2, 2), (1, 2), (1, 2), (0, 4)]
    main = [(16, 2), (15, 1), (14, 2), (12, 2), (11, 1), (10, 2), (9, 1), (8, 2),
            (7, 3), (7, 3), (7, 2), (6, 3), (6, 2), (6, 2), (5, 3), (5, 2), (4, 2), (4, 2),
            (3, 2), (3, 2), (2, 2), (2, 1), (1, 2), (1, 2), (0, 6)]
    b.append(prang(66, sat))
    b.append(prang(242, sat))
    b.append(prang(154, main))
    for yy in (232, 196, 160):
        b.append(rect(152, yy, 4, 8, '#7a3a14'))
    for i, (lx, ly) in enumerate(lights):
        b.append(rect(lx, ly, 4, 4, '#fffbe6', f'class="t{i % 4}" style="animation-delay:-{i * 0.37:.2f}s"'))

    # palms
    PALM = ["..fff...fff..", ".f...f.f...f.", "f...fffff...f", "...f..t..f...", "..f...t...f..",
            "......t......", "......t......", ".....t.......", ".....t.......", ".....t.......",
            ".....t.......", ".....t.......", ".....t.......", ".....t......."]
    for px in (276, 298):
        b.append(sprite(PALM, {'f': '#180f2c', 't': '#180f2c'}, px, BASE - 14 * 4, 4))

    # --- city skyline (right side)
    blds = [(320, 30, 272), (352, 40, 258), (394, 28, 276), (424, 44, 250), (470, 26, 268), (498, 46, 256),
            (546, 36, 246), (584, 42, 264), (628, 44, 232), (674, 40, 190), (716, 20, 236), (738, 48, 116),
            (788, 42, 168), (832, 40, 150), (874, 44, 200), (920, 44, 226)]
    tones = ['#1a1233', '#201640', '#17102e', '#231845']
    win = {}
    flick = []
    for i, (x, w, top) in enumerate(blds):
        b.append(rect(x, top, w, BASE - top, tones[i % 4] if x != 738 else '#262050'))
        b.append(rect(x, top, w, 4, '#2f2458'))
        if x == 738:  # MahaNakhon-ish pixel ribbon
            for k in range((BASE - top) // 8):
                bx = x + ((k * 8) % w)
                b.append(rect(bx, top + k * 8, 8, 8, '#3d3170'))
                b.append(rect(bx, top + k * 8 + 4, 4, 4, '#4f4290'))
        for wx in range(x + 4, x + w - 4, 8):
            for wy in range(top + 8, BASE - 4, 8):
                if r.random() < 0.3:
                    c = r.choice(['#ffd36e', '#ffe9a8', '#7ee8ff', '#ff9be0', '#ffd36e'])
                    if r.random() < 0.08:
                        flick.append(rect(wx, wy, 4, 4, c, f'class="t{r.randrange(4)}"'))
                    else:
                        win.setdefault(c, []).append(f"M{wx} {wy}h4v4h-4z")
    for c, d in win.items():
        b.append(f'<path d="{"".join(d)}" fill="{c}" opacity=".9"/>')
    b += flick
    # Baiyoke-ish tower: antenna + LED crown
    css.append(".led{animation:led 4s steps(1) infinite}@keyframes led{0%{fill:#ff4fd8}25%{fill:#38c6ff}50%{fill:#3ddc84}75%{fill:#ffd36e}}")
    b.append(rect(850, 126, 4, 24, '#2a2150'))
    b.append(rect(832, 150, 40, 8, '#ff4fd8', 'class="led"'))
    b.append(rect(850, 122, 4, 4, '#ff3b5c', 'class="bl"'))
    b.append(rect(760, 112, 4, 4, '#ff3b5c', 'class="bl" style="animation-delay:-.6s"'))

    # --- road + river
    b.append(rect(0, BASE, W, 12, '#140c26'))
    b.append(rect(0, BASE, W, 4, '#2c1f4d'))
    river = [(328, '#0a1430'), (352, '#0c1838'), (376, '#0e1c42')]
    for k, (y, c) in enumerate(river):
        y2 = river[k + 1][0] if k + 1 < len(river) else H
        b.append(rect(0, y, W, y2 - y, c))
    css.append(".s0{animation:sh 3s steps(3) infinite}.s1{animation:sh 4.4s steps(3) infinite}.s2{animation:sh 2.2s steps(2) infinite}"
               "@keyframes sh{0%,100%{transform:translateX(0);opacity:.35}50%{transform:translateX(8px);opacity:.95}}")
    # reflections
    for y in range(332, 396, 8):
        fade = 1 - (y - 332) / 90
        full = 132 * (0.55 + 0.45 * fade)
        segs = [(154 - full / 2, full * r.uniform(.3, .45)), (154 + full * r.uniform(-.05, .1), full * r.uniform(.25, .4))]
        for sx, sw in segs:
            b.append(rect(round(sx / 4) * 4, y, max(4, round(sw / 4) * 4), 4, '#f5b456',
                          f'opacity="{0.25 + 0.5 * fade:.2f}" class="s{r.randrange(3)}" style="animation-delay:-{r.uniform(0, 3):.1f}s"'))
        mw = 24 * (0.4 + 0.6 * fade)
        b.append(rect(round((872 - mw / 2) / 4) * 4, y, max(4, round(mw / 4) * 4), 4, '#fff4d6',
                      f'opacity="{0.2 + 0.5 * fade:.2f}" class="s{r.randrange(3)}" style="animation-delay:-{r.uniform(0, 3):.1f}s"'))
    for _ in range(60):
        x, y = r.randrange(0, W // 4) * 4, r.randrange(333 // 4, 398 // 4) * 4
        c = r.choice(['#2b5aa0', '#4a86d6', '#9cc8ff', '#ff9be0', '#ffd36e'])
        b.append(rect(x, y, r.randint(2, 6) * 4, 4, c,
                      f'opacity=".5" class="s{r.randrange(3)}" style="animation-delay:-{r.uniform(0, 4):.1f}s"'))

    # --- long-tail boat (right -> left)
    BOAT = ["......................K.......", "......................K.......", "..R..................KKK......",
            "..W..................K.K..EE..", ".WW...................K..EEEE.", ".WWHHHHHHHHHHHHHHHHHHHHHHHHH.S",
            "..WHHHHHHHHHHHHHHHHHHHHHHHH..S", "....HHHHHHHHHHHHHHHHHHHHH....."]
    css.append(".boat{animation:boat 30s linear infinite}@keyframes boat{from{transform:translateX(1000px)}to{transform:translateX(-120px)}}"
               ".bob{animation:bob 1s steps(2) infinite alternate}@keyframes bob{from{transform:translateY(0)}to{transform:translateY(-3px)}}")
    b.append(f'<g transform="translate(0 336)"><g class="boat" style="animation-delay:-9s"><g class="bob">'
             f'{sprite(BOAT, {"K": "#0f0a1e", "R": "#ff4fd8", "W": "#c76b2e", "H": "#8a4a24", "E": "#2a2a3a", "S": "#6b6b80"}, 0, 0, 3)}'
             f'</g></g></g>')

    # --- krathongs floating (left -> right)
    KRA = ["....f....", "....c....", ".p..c..p.", ".pp.c.pp.", "ppwpppwpp", "ggggggggg", ".ggggggg."]
    css.append(".kra{animation:kra 70s linear infinite}@keyframes kra{from{transform:translateX(-40px)}to{transform:translateX(1000px)}}")
    for k, (y, dl) in enumerate([(360, 8), (378, 31), (366, 52), (382, 64)]):
        spr = sprite(KRA, {'c': '#fff6e0', 'p': '#ff8fc7', 'w': '#ffe3f1', 'g': '#2fb36b'}, 0, 0, 3)
        flame = f'<g class="fl"><circle cx="13" cy="2" r="12" fill="url(#lg)"/>{rect(12, 0, 3, 3, "#ffe066")}</g>'
        b.append(f'<g transform="translate(0 {y})"><g class="kra" style="animation-delay:-{dl}s">'
                 f'<g class="bob" style="animation-delay:-{k * 0.3:.1f}s">{flame}{spr}</g></g></g>')

    # --- tuk-tuk (left -> right)
    TUK = ["...RRRRRRRRRRRRRRRR...", "..RRRRRRRRRRRRRRRRRR..", "...K......K......K....",
           "...K..pp..K..dd..K....", "...K.pppp.K.dddd.KK...", "..YYYYYYYYYYYYYYYYYYL.",
           ".YYYYYYYYYYYYYYYYYYYY.", ".YYYSSSYYYYYYYYYYSSSY.", "..YSKKKSYYYYYYYYSKKKS.",
           "...KKWKK......KKKWKK..", "....KKK........KKK...."]
    css.append(".tuk{animation:tuk 13s linear infinite}@keyframes tuk{from{transform:translateX(-90px)}to{transform:translateX(1000px)}}"
               ".bump{animation:bob .25s steps(1) infinite alternate}")
    beam = '<path d="M66 15L150 4V36Z" fill="#fff3b0" opacity=".16"/>'
    b.append(f'<g transform="translate(0 291)"><g class="tuk"><g class="bump">{beam}'
             f'{sprite(TUK, {"R": "#ff4fd8", "K": "#0b0b1e", "p": "#1b1030", "d": "#1b1030", "Y": "#ffd36e", "S": "#d99a2b", "L": "#fff7c2", "W": "#9aa0b4"}, 0, 0, 3)}'
             f'</g></g></g>')

    # --- sparkles + title
    SPARK = ["..#..", "..#..", "##w##", "..#..", "..#.."]
    css.append(".sp{transform-box:fill-box;transform-origin:center;animation:sp 2.6s ease-in-out infinite}"
               "@keyframes sp{0%,100%{opacity:0;transform:scale(.3)}50%{opacity:1;transform:scale(1)}}")
    for k, (sx, sy, c) in enumerate([(366, 40, '#ffffff'), (588, 34, '#ffd36e'), (348, 110, '#7af6ff'),
                                     (606, 116, '#ffffff'), (318, 170, '#ffd36e'), (630, 156, '#ff9be0'),
                                     (292, 70, '#c9b8ff'), (660, 80, '#7af6ff')]):
        b.append(f'<g class="sp" style="animation-delay:-{k * 0.47:.2f}s">{sprite(SPARK, {"#": c, "w": "#fff"}, sx, sy, 3)}</g>')

    sc = 14
    x42, y42 = round((W - tw("42", sc)) / 2), 30
    defs.append('<linearGradient id="g42" x1="0" y1="0" x2="0" y2="1">'
                + "".join(f'<stop offset="{o:.4f}" stop-color="{c}"/>' for o, c in [
                    (0, '#9ffaff'), (2 / 7, '#9ffaff'), (2 / 7, '#5fd7ff'), (4 / 7, '#5fd7ff'),
                    (4 / 7, '#b18cff'), (6 / 7, '#b18cff'), (6 / 7, '#ff6fd8'), (1, '#ff6fd8')])
                + '</linearGradient>')
    d42 = text_d("42", x42, y42, sc)
    defs.append(f'<clipPath id="c42"><path d="{d42}"/></clipPath>')
    css.append(".bob42{animation:bob42 3.2s steps(4) infinite}@keyframes bob42{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}"
               ".shine{animation:shine 5s steps(28) infinite}@keyframes shine{0%{transform:translateX(360px)}38%,100%{transform:translateX(640px)}}")
    g = ['<g class="bob42">']
    for dx, dy in [(-4, 0), (0, -4), (-4, -4), (4, -4), (-4, 4)]:
        g.append(f'<path d="{text_d("42", x42 + dx, y42 + dy, sc)}" fill="#12052a"/>')
    for k, c in [(5, '#0c031d'), (4, '#12052a'), (3, '#2a0d4d'), (2, '#3d1468'), (1, '#521b82')]:
        g.append(f'<path d="{text_d("42", x42 + k * 4, y42 + k * 4, sc)}" fill="{c}"/>')
    g.append(f'<path d="{d42}" fill="url(#g42)"/>')
    g.append(f'<g clip-path="url(#c42)"><path class="shine" d="M0 {y42 - 10}h26l-60 120h-26z" fill="#fff" opacity=".6"/></g>')
    g.append('</g>')
    b += g

    word, sc2 = "BANGKOK", 6
    xb, yb = round((W - tw(word, sc2)) / 2), 152
    defs.append(f'<linearGradient id="gbk" gradientUnits="userSpaceOnUse" x1="0" y1="{yb}" x2="0" y2="{yb + 42}">'
                + "".join(f'<stop offset="{o:.4f}" stop-color="{c}"/>' for o, c in [
                    (0, '#fff1b8'), (3 / 7, '#fff1b8'), (3 / 7, '#ffd36e'), (5 / 7, '#ffd36e'), (5 / 7, '#ff9f43'), (1, '#ff9f43')])
                + '</linearGradient>')
    css.append(".wv{animation:wv 2.4s steps(3) infinite}@keyframes wv{0%,50%,100%{transform:translateY(0)}25%{transform:translateY(-6px)}}")
    for i, ch in enumerate(word):
        lx = xb + i * ADV * sc2
        b.append(f'<g class="wv" style="animation-delay:{i * 0.12:.2f}s">'
                 f'<path d="{text_d(ch, lx + 6, yb + 6, sc2)}" fill="#3a0f45"/>'
                 f'<path d="{text_d(ch, lx, yb, sc2)}" fill="url(#gbk)"/></g>')

    b.append(cstext("DISCOVERY PISCINE · PYTHON", W / 2, 210, 2, '#e3d6ff', '#2a1652'))
    b.append(f'<path d="{ppath(W // 2 - 100, 372, 200, 30, 2, (2, 1))}" fill="#060c22" opacity=".7"/>')
    b.append(cstext("- PRESS START -", W / 2, 380, 2, '#ffffff', '#0a1430', attrs='class="bl"'))
    b.append('</g>')
    return svg(W, H, "".join(b), "".join(css), "".join(defs),
               "42 Bangkok Discovery Piscine pixel-art banner")


# ================================================================== TERMINAL
def terminal():
    W, sc, LH = 960, 2, 28
    AP = ADV * sc
    x0, y0 = 40, 72
    PINK, CYAN, WHITE, GREEN, YEL = "#ff5fd2", "#5fe3ff", "#ecebff", "#5dff9a", "#ffd36e"
    seq = [
        ('cmd', [('$ ', PINK), ('python3 ', CYAN), ('cell00/ex01/42.py', WHITE)]),
        ('out', [('42', YEL)]),
        ('cmd', [('$ ', PINK), ('python3 ', CYAN), ('cell05/ex12/string_are_arrays.py ', WHITE), ('pizzazz', YEL)]),
        ('out', [('zzzz', GREEN)]),
        ('cmd', [('$ ', PINK), ('python3 ', CYAN), ('cell05/ex13/append_it.py ', WHITE), ('pixel art', YEL)]),
        ('out', [('pixelism', GREEN)]),
        ('out', [('artism', GREEN)]),
        ('cmd', [('$ ', PINK), ('python3 ', CYAN), ('RUSH/main.py', WHITE)]),
        ('out', [('Success', GREEN)]),
        ('cmd', [('$ ', PINK)]),
    ]
    H = y0 + len(seq) * LH + 16
    css, defs, b = [BLINK, FLICK], [], []

    # timeline
    t, CH = 0.8, 0.05
    line_pairs, cur = [], []
    success_t = 0
    for i, (kind, segs) in enumerate(seq):
        s = "".join(x for x, _ in segs)
        y = y0 + i * LH
        pairs = []
        if kind == 'cmd':
            pairs.append((t, 2))
            cur.append((t, x0 + 2 * AP, y))
            if len(s) > 2:
                t += 0.45
                for k in range(3, len(s) + 1):
                    pairs.append((t, k))
                    cur.append((t, x0 + k * AP, y))
                    t += CH
                t += 0.4
        else:
            pairs.append((t, len(s)))
            if s == "Success":
                success_t = t
            cur.append((t, x0, y + LH))
            t += 0.15
            if i + 1 < len(seq) and seq[i + 1][0] == 'cmd':
                t += 0.65
        line_pairs.append(pairs)
    R = t + 4.0
    T = R + 0.6

    b.append(f'<path d="{ppath(0, 0, W, H)}" fill="#3a2d7a"/>')
    b.append(f'<path d="{ppath(4, 4, W - 8, H - 8)}" fill="#0c0a1d"/>')
    defs.append(f'<clipPath id="scr"><path d="{ppath(4, 4, W - 8, H - 8)}"/></clipPath>')
    defs.append('<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" opacity=".22"/></pattern>')
    b.append('<g clip-path="url(#scr)">')
    b.append(rect(4, 4, W - 8, 40, '#1b1540'))
    b.append(rect(4, 44, W - 8, 4, '#3a2d7a'))
    for i, c in enumerate(['#ff5f56', '#ffbd2e', '#27c93f']):
        b.append(rect(22 + i * 22, 18, 12, 12, c))
    b.append(ctext("ZSH · ~/DISCOVERY_PISCINE", W / 2, 17, 2, '#9d8cff'))

    for i, ((kind, segs), pairs) in enumerate(zip(seq, line_pairs)):
        y = y0 + i * LH
        wp = [(tt, k * AP + 4) for tt, k in pairs] + [(R, 0)]
        defs.append(f'<clipPath id="L{i}"><rect x="{x0 - 2}" y="{y - 4}" width="0" height="{LH}">'
                    f'{disc_anim("width", 0, wp, T)}</rect></clipPath>')
        xx, parts = x0, []
        for s, c in segs:
            parts.append(text(s, xx, y, sc, c))
            xx += len(s) * AP
        glow = ' filter="url(#gl)"' if kind == 'out' and segs[0][0] == 'Success' else ''
        b.append(f'<g clip-path="url(#L{i})"{glow}>{"".join(parts)}</g>')
    defs.append('<filter id="gl" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/>'
                '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')

    cx_pairs = [(tt, x) for tt, x, _ in cur] + [(R, x0)]
    cy_pairs = [(tt, y) for tt, _, y in cur] + [(R, y0)]
    css.append(".cur{animation:bl .9s steps(1) infinite}")
    b.append(f'<rect class="cur" x="{x0}" y="{y0}" width="{5 * sc}" height="{7 * sc}" fill="#ecebff">'
             f'{disc_anim("x", x0, cx_pairs, T)}{disc_anim("y", y0, cy_pairs, T)}</rect>')

    # mascot + bubbles reacting to "Success"
    p = success_t / T * 100
    pr = R / T * 100
    msc = 6
    mx, my = 756, H - 20 - 20 * msc
    css.append(f".hop{{animation:hop {T:.2f}s linear infinite}}"
               f"@keyframes hop{{0%,{p:.2f}%{{transform:translateY(0)}}{p + 1.2:.2f}%{{transform:translateY(-28px)}}"
               f"{p + 2.4:.2f}%{{transform:translateY(0)}}{p + 3.4:.2f}%{{transform:translateY(-14px)}}{p + 4.4:.2f}%,100%{{transform:translateY(0)}}}}"
               f".b1{{animation:b1 {T:.2f}s steps(1) infinite}}.b2{{animation:b2 {T:.2f}s steps(1) infinite}}"
               f"@keyframes b1{{0%{{opacity:1}}{p:.2f}%{{opacity:0}}{pr:.2f}%{{opacity:1}}}}"
               f"@keyframes b2{{0%{{opacity:0}}{p:.2f}%{{opacity:1}}{pr:.2f}%{{opacity:0}}}}"
               ".idle{animation:bob 1.2s steps(1) infinite alternate}@keyframes bob{from{transform:translateY(0)}to{transform:translateY(-4px)}}")
    b.append(f'<g class="hop"><g class="idle">{snek(mx, my, msc)}</g></g>')

    def bubble(msg, bg, fg, cls):
        w = tw(msg, 2) + 24
        bx, by = mx + 15 * msc - w // 2, my - 56
        tail = rect(bx + w // 2 - 8, by + 34, 12, 6, bg) + rect(bx + w // 2 - 4, by + 40, 6, 6, bg)
        return (f'<g class="{cls}"><path d="{ppath(bx, by, w, 34, 2, (2, 1))}" fill="{bg}"/>{tail}'
                f'{text(msg, bx + 12, by + 10, 2, fg)}</g>')

    b.append(bubble("HELLO, 42!", '#f4f1ff', '#1b1540', 'b1'))
    b.append(bubble("SUCCESS!!", '#5dff9a', '#0b2a1a', 'b2'))

    # confetti burst
    rr = random.Random(7)
    ccx, ccy = mx + 15 * msc, my + 40
    for i in range(14):
        ang = -math.pi * (0.1 + 0.8 * i / 13)
        dist = rr.uniform(70, 120)
        dx, dy = math.cos(ang) * dist, math.sin(ang) * dist
        css.append(f"@keyframes cf{i}{{0%,{p:.2f}%{{transform:translate(0,0);opacity:0}}{p + 0.3:.2f}%{{opacity:1}}"
                   f"{p + 9:.2f}%{{transform:translate({dx:.0f}px,{dy + 30:.0f}px);opacity:0}}100%{{opacity:0}}}}"
                   f".cf{i}{{opacity:0;animation:cf{i} {T:.2f}s steps(12) infinite}}")
        c = rr.choice(['#ff5fd2', '#5fe3ff', '#ffd36e', '#5dff9a', '#b18cff'])
        b.append(rect(ccx, ccy, 6, 6, c, f'class="cf{i}"'))

    b.append(rect(4, 48, W - 8, H - 52, 'url(#scan)'))
    b.append('</g>')
    return svg(W, H, "".join(b), "".join(css), "".join(defs), "Animated terminal running the piscine exercises")


# ================================================================== WORLD MAP
def worldmap():
    W, H = 960, 390
    css, defs, b = [BLINK, FLICK], [], []
    defs.append(f'<clipPath id="fr"><path d="{ppath(0, 0, W, H)}"/></clipPath>')
    defs.append('<pattern id="tile" width="32" height="32" patternUnits="userSpaceOnUse"><rect width="32" height="32" fill="#0a2c57"/>'
                '<rect width="32" height="2" fill="#0e3668"/><rect width="2" height="32" fill="#0e3668"/></pattern>')
    defs.append('<pattern id="cau" width="64" height="48" patternUnits="userSpaceOnUse"><path d="M0 12h12v4H0zM12 8h8v4h-8zM20 12h10v4H20zM36 36h10v4H36zM46 32h8v4h-8zM54 36h10v4H54z" fill="#3b8ae0" opacity=".35"/></pattern>')
    defs.append('<pattern id="cau2" width="96" height="64" patternUnits="userSpaceOnUse"><path d="M8 40h14v4H8zM22 36h8v4h-8zM58 12h12v4H58zM70 8h8v4h-8zM78 12h10v4H78z" fill="#7fc4ff" opacity=".22"/></pattern>')
    css.append(".cau{animation:cau 4s linear infinite}@keyframes cau{to{transform:translateX(64px)}}"
               ".cau2{animation:cau2 7s linear infinite}@keyframes cau2{to{transform:translateX(-96px)}}")
    b.append('<g clip-path="url(#fr)">')
    b.append(rect(0, 0, W, H, 'url(#tile)'))
    for y in (126, 232, 338):
        b.append(rect(64, y - 4, W - 128, 8, '#06213f'))
        b.append(rect(64, y - 20, 8, 40, '#06213f'))
        b.append(rect(W - 72, y - 20, 8, 40, '#06213f'))
    b.append(f'<g class="cau">{rect(-64, 0, W + 128, H, "url(#cau)")}</g>')
    b.append(f'<g class="cau2">{rect(0, 0, W + 192, H, "url(#cau2)")}</g>')

    b.append(stext("WORLD 1 · DISCOVERY PISCINE", 28, 24, 3, '#ffffff', '#04142b'))
    sel = "▶ SELECT STAGE"
    b.append(text(sel, W - 28 - tw(sel, 2), 30, 2, '#ffd36e', 'class="bl"'))

    nodes = [('00', 'FIRST SPLASH'), ('01', 'VARIABLES'), ('02', 'IF / ELSE'), ('03', 'LOOPS'),
             ('04', 'STRINGS'), ('05', 'ARRAYS')]
    pos = [(96, 176), (226, 284), (356, 176), (486, 284), (616, 176), (746, 284)]
    boss = (880, 214)

    def ortho(pts):
        d = [f"M{pts[0][0]} {pts[0][1]}"]
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            d.append(f"H{bx}V{by}")
        return "".join(d)

    route = pos + [(boss[0] - 72, boss[1] + 10)]
    css.append(".march{animation:march .8s linear infinite}@keyframes march{to{stroke-dashoffset:-16}}")
    b.append(f'<path d="{ortho(route)}" fill="none" stroke="#04142b" stroke-width="10" opacity=".5"/>')
    b.append(f'<path class="march" d="{ortho(route)}" fill="none" stroke="#e8f4ff" stroke-width="6" stroke-dasharray="6 10" opacity=".75"/>')

    seg = lambda k: (lambda px, py: (int(((math.atan2(py, px) + math.pi / 4) % (2 * math.pi)) // (math.pi / 2)) % 2) == k)
    red_d, white_d = cells_d(disc_cells(30, 4, 16, seg(0)), 4), cells_d(disc_cells(30, 4, 16, seg(1)), 4)
    shadow_d = cells_d(disc_cells(30, 4, 16, lambda px, py: px + py > 22), 4)
    hi_d = cells_d(disc_cells(26, 4, 18, lambda px, py: px + py < -24), 4)
    rim_d = cells_d(disc_cells(34, 4, 30), 4)
    rip_d = cells_d(disc_cells(40, 4, 36), 4)
    CHECKM = ["....#", "...#.", "#.#..", ".#..."]
    css.append(".rb{animation:bob 1.6s steps(2) infinite alternate}@keyframes bob{from{transform:translateY(0)}to{transform:translateY(-4px)}}"
               ".rip{transform-box:fill-box;transform-origin:center;animation:rip 2.4s steps(6) infinite}"
               "@keyframes rip{0%{transform:scale(.8);opacity:.8}100%{transform:scale(1.5);opacity:0}}")
    for i, ((num, name), (cx, cy)) in enumerate(zip(nodes, pos)):
        dl = f'style="animation-delay:-{i * 0.4:.1f}s"'
        b.append(f'<g transform="translate({cx} {cy})"><path class="rip" {dl} d="{rip_d}" fill="#8fd0ff"/></g>')
        ring = (f'<path d="{rim_d}" fill="#04142b" opacity=".55"/><path d="{red_d}" fill="#ff4757"/>'
                f'<path d="{white_d}" fill="#f5f5ff"/><path d="{shadow_d}" fill="#000" opacity=".18"/>'
                f'<path d="{hi_d}" fill="#fff" opacity=".35"/>')
        badge = (f'<path d="{cells_d(disc_cells(9, 2), 2, 24, -24)}" fill="#3ddc84"/>'
                 f'{sprite(CHECKM, {"#": "#fff"}, 19, -28, 2)}')
        b.append(f'<g transform="translate({cx} {cy})"><g class="rb" {dl}>{ring}'
                 f'{stext(num, -11, -7, 2, "#ffffff", "#04142b")}{badge}</g></g>')
        lw = max(tw("CELL " + num, 2), tw(name, 2)) + 20
        ly = cy - 112 if i % 2 == 0 else cy + 38
        b.append(f'<path d="{ppath(cx - lw // 2, ly, lw, 46, 2, (2, 1))}" fill="#04142b" opacity=".78"/>')
        b.append(ctext("CELL " + num, cx, ly + 8, 2, '#7af6ff'))
        b.append(ctext(name, cx, ly + 26, 2, '#ffffff'))

    # boss: raft + golden king
    bx, by = boss
    css.append(".aura{animation:halo 1.6s ease-in-out infinite alternate}@keyframes halo{from{opacity:.35}to{opacity:.9}}")
    defs.append('<radialGradient id="kg"><stop offset="0" stop-color="#ffd36e" stop-opacity=".6"/><stop offset="1" stop-color="#ffd36e" stop-opacity="0"/></radialGradient>')
    b.append(f'<circle class="aura" cx="{bx}" cy="{by - 34}" r="70" fill="url(#kg)"/>')
    b.append(f'<path d="{ppath(bx - 48, by, 96, 20, 4, (1,))}" fill="#7a4a2a"/>')
    for k in range(1, 6):
        b.append(rect(bx - 48 + k * 16, by + 4, 4, 12, '#5a341c'))
    king = sprite(PIECES["K"], KING_PAL, bx - 30, by - 60, 5)
    b.append(f'<g class="ks">{king}</g>')
    b.append(cstext("BOSS", bx, by - 128, 3, '#ff3b5c', '#04142b', attrs='class="bl"'))
    b.append(cstext("CHECKMATE", bx, by - 96, 2, '#ffd36e', '#04142b'))
    b.append(cstext("RUSH", bx, by + 34, 2, '#7af6ff', '#04142b'))

    # traveling mascot (animateMotion with stops at each stage)
    sc = 2
    anchors = [(x, y - 30) for x, y in pos] + [(bx - 72, by + 10)]
    seglens = [abs(b2[0] - a[0]) + abs(b2[1] - a[1]) for a, b2 in zip(anchors, anchors[1:])]
    L = sum(seglens)
    tt, kp, kt = 0.0, [0.0], [0.0]
    acc = 0
    DW, SPD = 1.0, 180
    tt += DW
    kp.append(0.0)
    kt.append(tt)
    for sl in seglens:
        acc += sl
        tt += sl / SPD
        kp.append(acc / L)
        kt.append(tt)
        tt += DW
        kp.append(acc / L)
        kt.append(tt)
    arrive = kt[-2]
    tt += 2.2
    kp.append(1.0)
    kt.append(tt)
    T = tt
    mpath = ortho(anchors)
    b.append(f'<g><animate attributeName="opacity" dur="{T:.2f}s" repeatCount="indefinite" values="0;1;1;0" keyTimes="0;0.02;0.97;1"/>'
             f'<animateMotion dur="{T:.2f}s" repeatCount="indefinite" path="{mpath}" calcMode="linear" '
             f'keyPoints="{";".join(f"{v:.4f}" for v in kp)}" keyTimes="{";".join(f"{v / T:.4f}" for v in kt)}"/>'
             f'<g class="hopm">{snek(-23, -40, sc)}</g></g>')
    css.append(".hopm{animation:bob .3s steps(1) infinite alternate}")
    pa, pz = arrive / T * 100, 97.0
    frames = [f"0%,{pa:.2f}%{{transform:translateX(0)}}"]
    k, x = 0, pa
    while x < pz - 1:
        x += 0.8
        frames.append(f"{x:.2f}%{{transform:translateX({4 if k % 2 == 0 else -4}px)}}")
        k += 1
    frames.append(f"{pz:.2f}%,100%{{transform:translateX(0)}}")
    css.append(f".ks{{animation:ks {T:.2f}s steps(1) infinite}}@keyframes ks{{{''.join(frames)}}}"
               f".chk{{opacity:0;animation:chk {T:.2f}s steps(1) infinite}}@keyframes chk{{0%{{opacity:0}}{pa:.2f}%{{opacity:1}}{pz:.2f}%{{opacity:0}}}}")
    b.append(f'<g class="chk"><path d="{ppath(bx - 124, by - 82, 82, 26, 2, (2, 1))}" fill="#ff3b5c"/>'
             f'{rect(bx - 54, by - 56, 8, 6, "#ff3b5c")}{text("CHECK!", bx - 118, by - 76, 2, "#fff")}</g>')
    b.append('</g>')
    return svg(W, H, "".join(b), "".join(css), "".join(defs), "World map: Cell 00 to Cell 05 and the RUSH boss")


# ================================================================== CHECKMATE
def checkmate_svg():
    W, H = 960, 380
    board = ["..QB.", "K....", ".....", "R..P.", "....."]
    N, sq = len(board), 56
    bx, by = 52, 52
    css, defs, b = [BLINK], [], []
    T = 9
    b.append(f'<path d="{ppath(0, 0, W, H)}" fill="#3a2d7a"/>')
    b.append(f'<path d="{ppath(4, 4, W - 8, H - 8)}" fill="#100c24"/>')
    b.append(f'<path d="{ppath(bx - 16, by - 16, N * sq + 32, N * sq + 32)}" fill="#3a2d7a"/>')
    b.append(rect(bx - 4, by - 4, N * sq + 8, N * sq + 8, '#0b0820'))
    for rr in range(N):
        for cc in range(N):
            b.append(rect(bx + cc * sq, by + rr * sq, sq, sq, '#3b2f6e' if (rr + cc) % 2 == 0 else '#2a2154'))

    kr, kc = next((rr, row.index("K")) for rr, row in enumerate(board) if "K" in row)

    def walk(dr, dc):
        cells, d = [], 1
        while True:
            r2, c2 = kr + dr * d, kc + dc * d
            if not (0 <= r2 < N and 0 <= c2 < N):
                return cells, None
            if board[r2][c2] in "KQBRP":
                return cells, (r2, c2, board[r2][c2], d)
            cells.append((r2, c2, d))
            d += 1

    hits, dots = [], []
    for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        cells, hit = walk(dr, dc)
        dots += cells
        if hit and (hit[2] in "BQ" or (hit[2] == "P" and hit[3] == 1 and dr == 1)):
            hits.append(hit)
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        cells, hit = walk(dr, dc)
        dots += cells
        if hit and hit[2] in "RQ":
            hits.append(hit)

    for d in range(1, N):
        a = 6 + 5 * d
        css.append(f".r{d}{{opacity:0;animation:r{d} {T}s steps(1) infinite}}"
                   f"@keyframes r{d}{{0%{{opacity:0}}{a}%{{opacity:1}}44%{{opacity:0}}}}")
    for r2, c2, d in dots:
        b.append(rect(bx + c2 * sq + sq / 2 - 6, by + r2 * sq + sq / 2 - 6, 12, 12, '#7af6ff', f'class="r{d}"'))

    css.append(".hit{opacity:0;animation:hit %ss steps(1) infinite}@keyframes hit{0%%{opacity:0}30%%{opacity:.7}36%%{opacity:.3}42%%{opacity:.7}"
               "48%%{opacity:.3}54%%{opacity:.7}60%%{opacity:.3}66%%{opacity:.7}72%%{opacity:.3}78%%{opacity:.7}90%%{opacity:0}}" % T)
    for r2, c2, _, _ in hits:
        b.append(rect(bx + c2 * sq, by + r2 * sq, sq, sq, '#ff3b5c', 'class="hit"'))
        x1, y1 = bx + c2 * sq + sq // 2, by + r2 * sq + sq // 2
        x2, y2 = bx + kc * sq + sq // 2, by + kr * sq + sq // 2
        css.append(".laser{opacity:0;animation:laser %ss steps(1) infinite}@keyframes laser{0%%{opacity:0}40%%{opacity:1}"
                   "43%%{opacity:.4}46%%{opacity:1}60%%{opacity:.6}63%%{opacity:1}88%%{opacity:0}}" % T)
        b.append(f'<g class="laser"><line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#ff3b5c" stroke-width="10" opacity=".55"/>'
                 f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#fff" stroke-width="4"/></g>')

    frames = ["0%,44%{transform:translateX(0)}"]
    x, k = 44, 0
    while x < 84:
        x += 1.2
        frames.append(f"{x:.1f}%{{transform:translateX({3 if k % 2 == 0 else -3}px)}}")
        k += 1
    frames.append("86%,100%{transform:translateX(0)}")
    css.append(f".ks{{animation:ks {T}s steps(1) infinite}}@keyframes ks{{{''.join(frames)}}}")
    for rr, row in enumerate(board):
        for cc, ch in enumerate(row):
            if ch in PIECES:
                spr = sprite(PIECES[ch], KING_PAL if ch == "K" else FOE_PAL, bx + cc * sq + 4, by + rr * sq + 6, 4)
                b.append(f'<g class="ks">{spr}</g>' if ch == "K" else spr)

    css.append(".pop{opacity:0;animation:pop %ss steps(1) infinite}@keyframes pop{0%%{opacity:0}46%%{opacity:1}90%%{opacity:0}}" % T)
    kx, ky = bx + kc * sq, by + kr * sq
    b.append(f'<g class="pop"><path d="{ppath(kx + 20, ky - 36, 88, 30, 2, (2, 1))}" fill="#ff3b5c"/>'
             f'{rect(kx + 30, ky - 6, 8, 6, "#ff3b5c")}{text("CHECK!", kx + 28, ky - 28, 2, "#fff")}</g>')

    # right panel
    px = 400
    b.append(stext("RUSH · CHECKMATE", px, 44, 4, '#ffd36e', '#3a1250'))
    b.append(text("IS THE KING IN CHECK?", px, 88, 2, '#c9b8ff'))
    b.append(f'<path d="{ppath(px - 4, 116, 120, 160, 2, (2, 1))}" fill="#0b0820"/>')
    for rr, row in enumerate(board):
        for cc, ch in enumerate(row):
            col = {'K': '#ffd36e', '.': '#5a4f8a'}.get(ch, '#ff6fa8')
            b.append(text(ch, px + 12 + cc * 18, 130 + rr * 28, 3, col))
    log = [(10, "> SCAN 8 DIRECTIONS", '#7af6ff'), (22, "> DIAGONALS ..... CLEAR", '#9d8cff'),
           (32, "> STRAIGHTS .... ROOK!", '#ff6fa8'), (46, "> RESULT:", '#ecebff')]
    for i, (a, msg, col) in enumerate(log):
        css.append(f".lg{i}{{opacity:0;animation:lg{i} {T}s steps(1) infinite}}@keyframes lg{i}{{0%{{opacity:0}}{a}%{{opacity:1}}94%{{opacity:0}}}}")
        b.append(text(msg, px + 144, 126 + i * 28, 2, col, f'class="lg{i}"'))
    css.append(".win{opacity:0;animation:win %ss steps(1) infinite}@keyframes win{0%%{opacity:0}52%%{opacity:1}"
               "58%%{opacity:.2}61%%{opacity:1}67%%{opacity:.2}70%%{opacity:1}94%%{opacity:0}}" % T)
    result = "Success" if hits else "Fail"
    b.append(stext(result, px + 144, 238, 5, '#5dff9a' if hits else '#ff3b5c', '#0b2a1a', 5, 'class="win"'))
    b.append(text("$ python3 RUSH/main.py", px, 316, 2, '#6f66a0'))
    return svg(W, H, "".join(b), "".join(css), "".join(defs), "Checkmate rush: the rook gives check to the king")


# ================================================================== STATS
def stats():
    W, H = 960, 240
    css, defs, b = [BLINK, FLICK], [], []
    defs.append('<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#18206a"/><stop offset=".5" stop-color="#18206a"/>'
                '<stop offset=".5" stop-color="#121a55"/><stop offset="1" stop-color="#0c1240"/></linearGradient>')
    defs.append('<pattern id="pw" width="32" height="16" patternUnits="userSpaceOnUse"><rect width="32" height="16" fill="#0a5fa8"/>'
                '<path d="M0 8h8v4H0zM8 4h8v4H8zM16 8h8v4h-8z" fill="#3b9cf0" opacity=".45"/></pattern>')
    b.append(f'<path d="{ppath(0, 0, W, H)}" fill="#e8ecff"/>')
    b.append(f'<path d="{ppath(4, 4, W - 8, H - 8)}" fill="#3a46b0"/>')
    b.append(f'<path d="{ppath(8, 8, W - 16, H - 16)}" fill="url(#bg)"/>')

    b.append(f'<path d="{ppath(28, 28, 176, 184)}" fill="#e8ecff"/>')
    defs.append(f'<clipPath id="pf"><path d="{ppath(32, 32, 168, 176)}"/></clipPath>')
    css.append(".pw{animation:pw 3s linear infinite}@keyframes pw{to{transform:translateX(32px)}}"
               ".idle{animation:bob 1s steps(1) infinite alternate}@keyframes bob{from{transform:translateY(0)}to{transform:translateY(-6px)}}")
    b.append(f'<g clip-path="url(#pf)">{rect(32, 32, 168, 176, "#0a5fa8")}<g class="pw">{rect(0, 32, 240, 176, "url(#pw)")}</g>'
             f'<g class="idle">{snek(34, 76, 6)}</g></g>')

    b.append(stext("PLAYER 1", 232, 32, 4, '#ffd36e', '#2a1652'))
    b.append(text("CLASS: PISCINER", 232, 78, 2, '#c9d2ff'))
    b.append(text("GUILD: 42 BANGKOK", 448, 78, 2, '#c9d2ff'))
    b.append(text("LV", 788, 44, 3, '#c9d2ff'))
    b.append(stext("06", 836, 28, 6, '#ffffff', '#2a1652', 6))

    bars = [("CELLS", "06/06", "#3ddc84", "#b6ffcf"), ("QUESTS", "36/36", "#38c6ff", "#c4f0ff"),
            ("BOSS", "01/01", "#ff5fd2", "#ffc2ee")]
    css.append(".fill{transform-box:fill-box;transform-origin:0 50%;animation:fill 7s steps(24) infinite}"
               "@keyframes fill{0%{transform:scaleX(0)}35%,100%{transform:scaleX(1)}}")
    for i, (lab, val, c, hi) in enumerate(bars):
        y = 112 + i * 30
        b.append(text(lab, 232, y, 2, '#ffffff'))
        b.append(rect(332, y - 4, 368, 22, '#05081f'))
        b.append(rect(336, y, 360, 14, '#1d2470'))
        b.append(f'<g class="fill" style="animation-delay:{i * 0.25:.2f}s">{rect(336, y, 360, 14, c)}{rect(336, y, 360, 4, hi)}</g>')
        b.append(text(val, 716, y, 2, '#ffffff'))

    css.append(".lvup{opacity:0;animation:lvup 7s steps(1) infinite}@keyframes lvup{0%{opacity:0}42%{opacity:1}48%{opacity:0}"
               "52%{opacity:1}58%{opacity:0}62%{opacity:1}90%{opacity:0}}")
    b.append(f'<g class="lvup">{stext("LEVEL UP!", 800, 120, 2, "#ffd36e", "#2a1652")}'
             f'{text("♥ ♥ ♥", 818, 150, 2, "#ff5fd2")}</g>')
    b.append(text("> NEXT DIVE: ???   KEEP SWIMMING!", 232, 206, 2, '#9fb0ff'))
    b.append(text("▼", W - 44, 206, 2, '#ffffff', 'class="bl"'))
    return svg(W, H, "".join(b), "".join(css), "".join(defs), "RPG-style player stats card")


# ================================================================== POOL FOOTER
SWIM_HEAD = [
    ".....KKKKKKKK..",
    "...KKGGGGKBWBK.",
    "..KSSSSSSKBBBK.",
    ".KGGGGGGGGKKKGK",
    ".KGGGGGGGKKKGGK",
    "KGGGGGGGKWWKKGK",
    "KGGGGGGGKWKKKGK",
    "KGGGGGGGKKKWKGK",
    "KGGGGGGGGKKKGGK",
    "KGGGGGGGGGGPPGK",
    "KYYYYGGGGGGGKGK",
    ".KYYYYYYYYKKYK.",
    "..KKKKKKKKKKK..",
]
SWIM_PAL = {"K": "#0b0b1e", "G": "#3ddc84", "L": "#8ff5b8", "D": "#22a862", "Y": "#d4ffe6",
            "W": "#ffffff", "P": "#ff8fc7", "S": "#ff4fd8", "B": "#38c6ff", "R": "#ff4757"}


BUB_OPACITY = 'opacity=".7"'


def pool():
    W, H, P = 960, 128, 4
    css, defs, b = [FLICK], [], []
    defs.append(f'<clipPath id="fr"><path d="{ppath(0, 0, W, H)}"/></clipPath>')
    defs.append('<pattern id="edge" width="24" height="24" patternUnits="userSpaceOnUse"><rect width="24" height="24" fill="#dff6ff"/>'
                '<rect width="12" height="12" fill="#bfe9ff"/><rect x="12" y="12" width="12" height="12" fill="#bfe9ff"/></pattern>')
    defs.append('<pattern id="wav" width="48" height="24" patternUnits="userSpaceOnUse"><path d="M0 12h8v4H0zM8 8h8v4H8zM16 12h8v4h-8z" fill="#5fb8ff" opacity=".45"/></pattern>')
    defs.append('<pattern id="wav2" width="80" height="40" patternUnits="userSpaceOnUse"><path d="M12 28h12v4H12zM24 24h8v4h-8zM52 8h8v4h-8zM60 4h8v4h-8z" fill="#b8e4ff" opacity=".3"/></pattern>')
    b.append('<g clip-path="url(#fr)">')
    for y, c in [(24, '#0b6bbd'), (64, '#0a5ea6'), (100, '#08508f')]:
        b.append(rect(0, y, W, H - y, c))
    css.append(".w1{animation:w1 3s steps(12) infinite}@keyframes w1{to{transform:translateX(48px)}}"
               ".w2{animation:w2 6s steps(20) infinite}@keyframes w2{to{transform:translateX(-80px)}}")
    b.append(f'<g class="w1">{rect(-48, 24, W + 96, H, "url(#wav)")}</g>')
    b.append(f'<g class="w2">{rect(0, 24, W + 160, H, "url(#wav2)")}</g>')
    b.append(rect(0, 0, W, 24, 'url(#edge)'))
    b.append(rect(0, 24, W, 4, '#7cc7f0'))

    # lane rope (same 4px grid)
    css.append(".fb{animation:fb 1.4s steps(1) infinite alternate}@keyframes fb{from{transform:translateY(0)}to{transform:translateY(4px)}}")
    b.append(rect(0, 44, W, 4, '#e8f7ff', 'opacity=".55"'))
    fd = cells_d(disc_cells(8, P), P)
    for i, x in enumerate(range(8, W, 20)):
        c = ['#ff4757', '#f5f5ff', '#38c6ff'][i % 3]
        b.append(f'<g transform="translate({x} 44)"><g class="fb" style="animation-delay:-{(i * 0.2) % 1.4:.1f}s"><path d="{fd}" fill="{c}"/></g></g>')

    # bubbles from the pool floor
    r = random.Random(3)
    css.append(".bub{animation:bub 4s steps(20) infinite}@keyframes bub{0%{transform:translateY(0);opacity:0}10%{opacity:.8}100%{transform:translateY(-80px);opacity:0}}")
    for _ in range(16):
        x = r.randrange(0, W // P) * P
        s = r.choice([4, 4, 8])
        b.append(f'<g transform="translate({x} {H - 8})"><g class="bub" style="animation-delay:-{r.uniform(0, 4):.1f}s;animation-duration:{r.uniform(3, 6):.1f}s">'
                 f'{rect(0, 0, s, s, "#c9ecff", BUB_OPACITY)}</g></g>')

    # cute swimming python: every part on the same 4px grid
    T = 1.6
    css.append(f".sw{{animation:sw {T}s steps(1) infinite}}"
               "@keyframes sw{0%{transform:translateY(0)}12.5%{transform:translateY(-4px)}25%{transform:translateY(-8px)}"
               "37.5%{transform:translateY(-4px)}50%{transform:translateY(0)}62.5%{transform:translateY(4px)}"
               "75%{transform:translateY(8px)}87.5%{transform:translateY(4px)}}"
               f".hb{{animation:hb {T}s steps(1) infinite}}"
               "@keyframes hb{0%{transform:translateY(0)}25%{transform:translateY(-4px)}50%{transform:translateY(0)}75%{transform:translateY(4px)}}"
               ".swim{animation:swim 20s steps(330) infinite}@keyframes swim{from{transform:translateX(-240px)}to{transform:translateX(1080px)}}"
               ".mb{animation:mb 1.8s steps(6) infinite}@keyframes mb{0%{transform:translateY(0);opacity:0}15%{opacity:1}100%{transform:translateY(-24px);opacity:0}}"
               ".hrt{opacity:0;animation:hrt 5s steps(6) infinite}@keyframes hrt{0%,70%{transform:translateY(0);opacity:0}72%{opacity:1}100%{transform:translateY(-24px);opacity:0}}")

    def seg(rows, x, y, i):
        dl = -((T - (i + 1) * 0.12) % T)
        return f'<g class="sw" style="animation-delay:{dl:.2f}s">{sprite(rows, SWIM_PAL, x, y, P)}</g>'

    body_y = 5 * P
    parts = []
    N = 11
    tail = [(["KK", "GG", "GD", "YY", "KK"], 1), (["KK", "GG", "YY", "KK"], 1), ([".K", "KG", "KK"], 2), (["K", "K"], 2)]
    for j in reversed(range(len(tail))):
        rows, off = tail[j]
        x = -(N + j + 1) * 2 * P + (2 - len(rows[0])) * P
        parts.append(seg(rows, x, body_y + off * P, N + j))
    for i in reversed(range(N)):
        spot = "GD" if i % 2 == 0 else "DG"
        parts.append(seg(["KK", "LL", "GG", spot, "YY", "KK"], -(i + 1) * 2 * P, body_y, i))
    ring = ".W. W.W .W.".split()
    heart = ".#.#. ##### ##### .###. ..#..".split()
    head = (f'<g class="hb">{sprite(SWIM_HEAD, SWIM_PAL, 0, 0, P)}'
            f'<g class="flick">{sprite(["...R", "RRR.", "...R"], SWIM_PAL, 15 * P, 9 * P, P)}</g>'
            + "".join(f'<g class="mb" style="animation-delay:-{k * 0.6:.1f}s">{sprite(ring, SWIM_PAL, (15 + k) * P, (2 - k) * P, P)}</g>' for k in range(3))
            + f'<g class="hrt">{sprite(heart, {"#": "#ff8fc7"}, 6 * P, -6 * P, P)}</g></g>')
    b.append(f'<g transform="translate(0 60)"><g class="swim">{"".join(parts)}{head}</g></g>')
    b.append('</g>')
    return svg(W, H, "".join(b), "".join(css), "".join(defs), "Pixel pool with a cute python in swim goggles")


# ================================================================== DIVIDER
def divider():
    W, H = 960, 12
    cols = ['#ff5fd2', '#b18cff', '#5fe3ff', '#3ddc84', '#ffd36e', '#ff9f43']
    kf = "".join(f"{i * 100 / len(cols):.2f}%{{fill:{c}}}" for i, c in enumerate(cols)) + f"100%{{fill:{cols[0]}}}"
    css = f".q{{animation:rb 2.4s steps(1) infinite}}@keyframes rb{{{kf}}}"
    body = "".join(rect(i * 16 + 2, 2, 12, 8, cols[0], f'class="q" style="animation-delay:-{i * 0.08:.2f}s"') for i in range(60))
    return svg(W, H, body, css, "", "")


# ================================================================== FLOW DIAGRAM
HEAD_R = ["#......", "###....", "#####..", "#######", "#####..", "###....", "#......"]


def rot(rows):
    N = len(rows)
    return ["".join(rows[N - 1 - c][r] for c in range(N)) for r in range(N)]


HEAD_D = rot(HEAD_R)
HEAD_L = rot(HEAD_D)
HEAD_U = rot(HEAD_L)
DIAG_ICON = ["#.....#", ".#...#.", "..#.#..", "...#...", "..#.#..", ".#...#.", "#.....#"]
LINE_ICON = ["...#...", "...#...", "...#...", "#######", "...#...", "...#...", "...#..."]


def flow():
    W, H = 960, 488
    css, defs, b = [BLINK], [], []
    INK, LINE = '#ecebff', '#cfc6ff'
    b.append(f'<path d="{ppath(0, 0, W, H)}" fill="#3a2d7a"/>')
    b.append(f'<path d="{ppath(4, 4, W - 8, H - 8)}" fill="#100c24"/>')
    defs.append('<pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="#2a2154"/></pattern>')
    b.append(rect(8, 8, W - 16, H - 16, 'url(#dots)'))
    b.append(stext("BOSS STRATEGY", 28, 26, 3, '#ffd36e', '#3a1250'))
    b.append(text("how checkmate.py thinks", 28 + tw("BOSS STRATEGY", 3) + 24, 33, 2, '#9d8cff'))

    css.append(".march{animation:march .8s linear infinite}@keyframes march{to{stroke-dashoffset:-12}}")

    def wire(d):
        return (f'<path d="{d}" fill="none" stroke="#04020d" stroke-width="8" opacity=".6"/>'
                f'<path class="march" d="{d}" fill="none" stroke="{LINE}" stroke-width="4" stroke-dasharray="6 6"/>')

    def arrow_r(x1, x2, y):
        return wire(f"M{x1} {y}H{x2 - 12}") + sprite(HEAD_R, {"#": LINE}, x2 - 14, y - 7, 2)

    def arrow_d(x, y1, y2):
        return wire(f"M{x} {y1}V{y2 - 12}") + sprite(HEAD_D, {"#": LINE}, x - 7, y2 - 14, 2)

    def arrow_u(x, y1, y2):
        return wire(f"M{x} {y1}V{y2 + 12}") + sprite(HEAD_U, {"#": LINE}, x - 7, y2, 2)

    def node(x, y, w, h, border, fill, cls=""):
        c = f' class="{cls}"' if cls else ""
        return (f'<path{c} d="{ppath(x, y, w, h)}" fill="{border}"/>'
                f'<path d="{ppath(x + 4, y + 4, w - 8, h - 8, 4, (2, 1))}" fill="{fill}"/>')

    def badge(x, y, num):
        return (f'<path d="{ppath(x, y, 24, 24, 2, (2, 1))}" fill="#ffd36e"/>'
                f'{text(num, x + 7, y + 5, 2, "#2a1652")}')

    Y, NH = 176, 100
    MY = Y + NH // 2
    S = [(24, 150), (214, 170), (424, 140), (604, 140), (780, 132)]
    OUT_X, OUT_W = 756, 180
    OUT_CX = OUT_X + OUT_W // 2

    # travelling data packet (drawn under the boxes, so it only shows on the wires)
    S5c = S[4][0] + S[4][1] // 2
    b.append(f'<g><animate attributeName="opacity" dur="5s" repeatCount="indefinite" values="0;1;1;0" keyTimes="0;.04;.92;1"/>'
             f'<animateMotion dur="5s" repeatCount="indefinite" path="M{S[0][0] + S[0][1]} {MY}H{S5c}V{110}"/>'
             f'{rect(-9, -9, 18, 18, "#7af6ff", "opacity=\".35\"")}{rect(-4, -4, 8, 8, "#ffffff")}</g>')

    # wires
    for (x1, w1), (x2, _) in zip(S, S[1:]):
        b.append(arrow_r(x1 + w1, x2, MY))
    p2 = S[1][0] + S[1][1] // 2
    b.append(arrow_d(p2, Y + NH, 330))
    b.append(arrow_u(S5c, Y, 112))
    b.append(arrow_d(S5c, Y + NH, 330))
    b.append(wire(f"M{S[3][0] + S[3][1] // 2} {Y + NH}V306"))
    b.append(text("YES", S[1][0] + S[1][1] + 3, MY - 22, 2, '#5dff9a'))
    b.append(text("NO", p2 + 12, 292, 2, '#ff3b5c'))
    b.append(text("YES", S5c + 12, 134, 2, '#5dff9a', 'class="bl"'))
    b.append(text("NO", S5c + 12, 292, 2, '#ff3b5c'))

    # 1 · input board
    x, w = S[0]
    cx = x + w // 2
    b.append(node(x, Y, w, NH, '#5a4aa8', '#171233'))
    b.append(ctext("INPUT", cx, Y + 14, 2, '#7af6ff'))
    board = ["..QB.", "K....", ".....", "R..P.", "....."]
    for rr, row in enumerate(board):
        for cc, ch in enumerate(row):
            col = '#ffd36e' if ch == 'K' else '#ff6fa8' if ch != '.' else ('#3b2f6e' if (rr + cc) % 2 == 0 else '#2a2154')
            b.append(rect(cx - 25 + cc * 10, Y + 38 + rr * 10, 10, 10, col))
    b.append(badge(x - 8, Y - 12, "1"))

    # 2 · parse_board
    x, w = S[1]
    cx = x + w // 2
    b.append(node(x, Y, w, NH, '#5a4aa8', '#171233'))
    b.append(ctext("PARSE_BOARD", cx, Y + 14, 2, '#7af6ff'))
    b.append(ctext("SQUARE?", cx, Y + 44, 2, INK))
    b.append(ctext("ONE KING?", cx, Y + 68, 2, INK))
    b.append(badge(x - 8, Y - 12, "2"))

    # 3 · find_king
    x, w = S[2]
    cx = x + w // 2
    b.append(node(x, Y, w, NH, '#5a4aa8', '#171233'))
    b.append(ctext("FIND_KING", cx, Y + 14, 2, '#7af6ff'))
    b.append(sprite(PIECES["K"], KING_PAL, cx - 18, Y + 44, 3))
    b.append(badge(x - 8, Y - 12, "3"))

    # 4 · scan 8 rays (animated compass)
    x, w = S[3]
    cx = x + w // 2
    b.append(node(x, Y, w, NH, '#5a4aa8', '#171233'))
    b.append(ctext("SCAN RAYS", cx, Y + 14, 2, '#7af6ff'))
    ox, oy = cx - 22, Y + 42
    css.append(".ry{animation:ry 1.6s steps(1) infinite}@keyframes ry{0%{fill:#ffffff}14%,100%{fill:#3d5f9a}}")
    for i, (dx, dy) in enumerate([(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]):
        cells = [(5 + dx * k, 5 + dy * k) for k in range(2, 6) if 0 <= 5 + dx * k <= 10 and 0 <= 5 + dy * k <= 10]
        b.append(f'<path class="ry" style="animation-delay:{i * 0.2:.1f}s" d="{cells_d(cells, 4, ox, oy)}" fill="#3d5f9a"/>')
    b.append(f'<path d="{cells_d([(i, j) for i in range(4, 7) for j in range(4, 7)], 4, ox, oy)}" fill="#ffd36e"/>')
    b.append(badge(x - 8, Y - 12, "4"))

    # 5 · decision
    x, w = S[4]
    cx = x + w // 2
    css.append(".dec{animation:dec 1.2s steps(1) infinite}@keyframes dec{0%{fill:#ffd36e}50%{fill:#ff9f43}}")
    b.append(node(x, Y, w, NH, '#ffd36e', '#2a2010', 'dec'))
    b.append(ctext("ATTACKER", cx, Y + 14, 2, '#ffd36e'))
    b.append(ctext("IN RANGE?", cx, Y + 44, 2, INK))
    b.append(ctext("?", cx, Y + 70, 2, '#ffd36e', 'class="bl"'))
    b.append(badge(x - 8, Y - 12, "5"))

    # outputs
    css.append(".ok{animation:ok 1.6s steps(1) infinite}@keyframes ok{0%{fill:#5dff9a}50%{fill:#2fbf6a}}")
    b.append(node(OUT_X, 36, OUT_W, 76, '#5dff9a', '#0f2e22', 'ok'))
    b.append(cstext("SUCCESS", OUT_CX, 48, 3, '#5dff9a', '#062016'))
    b.append(ctext("KING IN CHECK", OUT_CX, 82, 2, INK))
    b.append(node(OUT_X, 330, OUT_W, 76, '#ff3b5c', '#2e0f18'))
    b.append(cstext("FAIL", OUT_CX, 342, 3, '#ff3b5c', '#1a050b'))
    b.append(ctext("KING IS SAFE", OUT_CX, 376, 2, INK))
    ix = p2 - OUT_W // 2
    b.append(node(ix, 330, OUT_W, 76, '#5a4f8a', '#15122a'))
    b.append(cstext("INVALID", p2, 342, 3, '#a59bd6', '#08060f'))
    b.append(ctext("PRINT NOTHING", p2, 376, 2, '#8c84b8'))

    # ray rules card
    rx, ry, rw, rh = 410, 306, 330, 164
    b.append(node(rx, ry, rw, rh, '#5a4aa8', '#120e2a'))
    b.append(text("RAY RULES", rx + 16, ry + 14, 2, '#ffd36e'))
    rows = [(DIAG_ICON, "BQ", "ANY RANGE"), (DIAG_ICON, "P", "1 STEP, FROM BELOW"), (LINE_ICON, "RQ", "ANY RANGE")]
    for i, (icon, pcs, rule) in enumerate(rows):
        yy = ry + 40 + i * 32
        b.append(sprite(icon, {"#": '#7af6ff'}, rx + 16, yy + 2, 3))
        for k, pc in enumerate(pcs):
            b.append(sprite(PIECES[pc], FOE_PAL, rx + 50 + k * 28, yy, 2))
        b.append(text(rule, rx + 50 + len(pcs) * 28 + 10, yy + 6, 2, INK))
    b.append(text("FIRST HIT BLOCKS THE RAY", rx + 16, ry + 136, 2, '#9d8cff'))
    return svg(W, H, "".join(b), "".join(css), "".join(defs), "Flow diagram: how checkmate.py decides Success or Fail")


if __name__ == "__main__":
    save("banner.svg", banner())
    save("terminal.svg", terminal())
    save("map.svg", worldmap())
    save("checkmate.svg", checkmate_svg())
    save("flow.svg", flow())
    save("stats.svg", stats())
    save("pool.svg", pool())
    save("divider.svg", divider())
