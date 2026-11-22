#!/usr/bin/env python3
"""news-image-20261122 v2 (evening edition) — render "THE WORLD TODAY"
front page (1024x1024) for Sunday 22 November 2026.

All text is drawn programmatically with Pillow + system DejaVu fonts.
No network, no AI image generation, no external assets.
Every story was verified as 22 November 2026 news (first reported that
day, or happening that day) via Reuters / AP / The Times / ESPNcricinfo /
Wisden. Stories checked and deliberately excluded as NOT 22 Nov news:
El Chapo Isidro capture (announced Sat 21 Nov), Trump-Xi-Putin Shenzhen
summit (Thu 19 Nov), EU-Indonesia trade deal (signed Sat 21 Nov),
US AI stock sell-off (Fri 20 Nov close), Cikande factory fire as a
Saturday event (fire broke out Sat evening; only the Sunday search for
the 36 missing is a 22 Nov development — ticker only).

v2 changes vs v1 (morning edition): masthead EVENING EDITION; lead
rewritten to the day's outcome (final COP31 text put to vote, no fossil
fuels named, 1.5C breach admitted, deal far from certain); cricket cell
updated to the completed day four (India declare 720/9, records);
ticker refreshed (Turin final tonight, Cikande search, Myanmar quake).

Usage: python3 draw.py [output.png]   (default: entry.png)
"""
import math
import random
import sys

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
REG = FONT_DIR + "DejaVuSans.ttf"

PAPER = (246, 241, 231)
INK = (26, 26, 26)
NAVY = (16, 36, 62)
GOLD = (201, 162, 39)
RED = (179, 35, 27)
RULE = (180, 172, 152)
GREY = (60, 60, 60)
GREY2 = (70, 70, 70)
WHITE = (255, 255, 255)
PANEL = (18, 28, 48)
SEA = (24, 90, 140)
TEAL = (14, 110, 96)

W, H = 1024, 1024


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(fnt, text, width):
    """Greedy word wrap; returns list of lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if fnt.getlength(t) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered(d, cx, y, text, fnt, fill):
    d.text((cx - fnt.getlength(text) / 2, y), text, font=fnt, fill=fill)


def draw_sun_and_sea(d, rng):
    """COP31 lead art: gold sun with rays over a teal sea, Antalya coast."""
    cx, cy = 176, 232
    # Sun rays.
    for i in range(12):
        ang = math.radians(i * 30)
        x1 = cx + 52 * math.cos(ang)
        y1 = cy + 52 * math.sin(ang)
        x2 = cx + 66 * math.cos(ang)
        y2 = cy + 66 * math.sin(ang)
        d.line([(x1, y1), (x2, y2)], fill=GOLD, width=5)
    d.ellipse([cx - 46, cy - 46, cx + 46, cy + 46], fill=(255, 205, 80))
    d.ellipse([cx - 46, cy - 46, cx + 46, cy + 46], outline=(255, 240, 180),
              width=2)
    # Sea waves.
    for j, yy in enumerate([330, 352, 374]):
        pts = []
        for x in range(16, 337, 8):
            pts.append((x, yy + 6 * math.sin((x + j * 40) / 28.0)))
        d.line(pts, fill=SEA if j % 2 == 0 else (52, 140, 190), width=4,
               joint="curve")
    # A small white sailboat on the waves.
    d.polygon([(252, 330), (252, 296), (282, 330)], fill=WHITE)
    d.polygon([(248, 330), (248, 302), (226, 330)], fill=(220, 225, 240))
    d.line([(252, 330), (292, 330)], fill=WHITE, width=3)


def icon_radar(d, cx, cy):
    # Radar sweep: concentric circles + sweep line + blips.
    for r in (34, 24, 14):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=2)
    d.line([(cx, cy), (cx + 30, cy - 18)], fill=(255, 205, 80), width=3)
    d.ellipse([cx + 22, cy - 14, cx + 30, cy - 6], fill=(255, 205, 80))
    d.ellipse([cx - 18, cy + 12, cx - 10, cy + 20], fill=WHITE)
    d.ellipse([cx - 4, cy - 2, cx + 4, cy + 6], fill=(255, 90, 70))


def icon_cricket(d, cx, cy):
    # Three stumps + bails, angled bat, red ball.
    for i in range(3):
        x0 = cx - 46 + i * 9
        d.rectangle([x0, cy - 22, x0 + 5, cy + 24], fill=WHITE)
    d.rectangle([cx - 46, cy - 26, cx - 19, cy - 22], fill=WHITE)
    d.line([(cx + 4, cy + 30), (cx + 30, cy - 24)], fill=(230, 190, 130),
           width=9)
    d.ellipse([cx + 42, cy + 18, cx + 56, cy + 32], fill=(200, 40, 40))
    d.ellipse([cx + 42, cy + 18, cx + 56, cy + 32], outline=WHITE, width=1)


def icon_globe(d, cx, cy):
    d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(52, 120, 190))
    d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], outline=WHITE, width=2)
    d.ellipse([cx - 14, cy - 34, cx + 14, cy + 34], outline=WHITE, width=2)
    d.line([(cx - 34, cy), (cx + 34, cy)], fill=WHITE, width=2)
    d.polygon([(cx - 18, cy + 8), (cx + 2, cy - 14), (cx + 20, cy + 10)],
              fill=(60, 170, 90))


def icon_flag(d, cx, cy):
    # Chequered flag on a pole + speed lines.
    d.line([(cx - 44, cy - 34), (cx - 44, cy + 34)], fill=WHITE, width=4)
    for r in range(3):
        for c in range(4):
            if (r + c) % 2 == 0:
                d.rectangle([cx - 40 + c * 18, cy - 30 + r * 18,
                             cx - 40 + c * 18 + 18, cy - 30 + r * 18 + 18],
                            fill=WHITE)
    for yy in (cy - 10, cy + 8, cy + 26):
        d.line([(cx + 38, yy), (cx + 56, yy)], fill=(255, 205, 80), width=3)


def icon_bridge(d, cx, cy):
    # Suspension bridge: deck, arc cable, two towers.
    d.line([(cx - 56, cy + 22), (cx + 56, cy + 22)], fill=WHITE, width=4)
    d.arc([cx - 56, cy - 30, cx + 56, cy + 40], 180, 360, fill=WHITE,
          width=3)
    for x0 in (cx - 44, cx + 40):
        d.line([(x0, cy - 26), (x0, cy + 22)], fill=WHITE, width=4)
    for x0 in range(cx - 36, cx + 40, 12):
        d.line([(x0, cy - 12), (x0, cy + 22)], fill=(255, 205, 80), width=2)


def icon_chart_up(d, cx, cy):
    # Axes + 4 rising bars + rising arrow.
    d.line([(cx - 54, cy + 30), (cx + 54, cy + 30)], fill=WHITE, width=3)
    d.line([(cx - 54, cy + 30), (cx - 54, cy - 30)], fill=WHITE, width=3)
    heights = [14, 24, 34, 44]
    for i, hh in enumerate(heights):
        x0 = cx - 44 + i * 24
        d.rectangle([x0, cy + 28 - hh, x0 + 14, cy + 28], fill=(255, 205, 80))
    d.line([(cx - 52, cy + 14), (cx + 50, cy - 28)], fill=WHITE, width=3)
    d.polygon([(cx + 50, cy - 28), (cx + 32, cy - 28), (cx + 50, cy - 10)],
              fill=WHITE)


CELLS = [
    ((140, 30, 30), icon_radar, "MIDDLE EAST  •  BAHRAIN",
     "IRAN HITS US BASES IN BAHRAIN",
     "IRGC claims strikes on US Patriot radars at al-Riffa and Awali; "
     "a factory fire, no injuries"),
    ((24, 110, 60), icon_cricket, "SPORT  •  CRICKET",
     "INDIA'S RECORD 720/9 IN WELLINGTON",
     "Pant 128, Rahul 136; first time all seven pairs pass 50; NZ 119/2, "
     "trail 233"),
    ((16, 60, 110), icon_globe, "ASIA  •  DIPLOMACY",
     "NEPAL PM LANDS IN NEW DELHI",
     "Balendra Shah's first bilateral visit since March; meets "
     "Jaishankar today, Modi talks Monday"),
    ((88, 32, 96), icon_flag, "SPORT  •  FORMULA 1",
     "VERSTAPPEN ON POLE IN LAS VEGAS",
     "Dutchman fastest in qualifying; the race runs under the lights "
     "tonight"),
    ((179, 35, 27), icon_bridge, "ASIA  •  INDIA",
     "MODI OPENS NITISH SETU IN BIHAR",
     "New bridge links Patna and Vaishali; projects worth Rs 34,000 "
     "crore unveiled"),
    ((14, 110, 96), icon_chart_up, "TRADE  •  ASIA",
     "INDIA, CANADA WRAP TRADE TALKS",
     "Latest round tied up as a Modi visit nears; both sides eye a deal"),
]


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    rng = random.Random(42)

    # ---- Masthead ----
    d.rectangle([4, 4, 1019, 116], fill=NAVY)
    d.text((24, 18), "EVENING EDITION", font=font(BOLD, 16), fill=GOLD)
    draw_centered(d, W // 2, 16, "T H E   W O R L D   T O D A Y",
                  font(BOLD, 26), GOLD)
    draw_centered(d, W // 2, 52, "SUNDAY 22 NOVEMBER 2026",
                  font(BOLD, 52), WHITE)
    d.line([(24, 112), (1000, 112)], fill=GOLD, width=2)

    # ---- Lead art panel ----
    d.rectangle([16, 130, 336, 424], fill=PANEL)
    draw_sun_and_sea(d, rng)
    d.text((28, 392), "ANTALYA  •  COP31", font=font(BOLD, 17), fill=WHITE)

    # ---- Lead text ----
    d.text((356, 138), "LEAD STORY  •  CLIMATE", font=font(BOLD, 22),
           fill=RED)
    hl_lines = wrap(font(BOLD, 52), "COP31 ON THE BRINK", 648)
    for i, ln in enumerate(hl_lines):
        d.text((356, 158 + i * 58), ln, font=font(BOLD, 52), fill=INK)
    sub_lines = wrap(
        font(REG, 27),
        "Final 10-page text put to vote in Antalya with no fossil fuels "
        "named; first COP to admit 1.5°C will be breached — deal far "
        "from certain",
        652)
    for i, ln in enumerate(sub_lines):
        d.text((356, 250 + i * 34), ln, font=font(REG, 27), fill=GREY)
    d.line([(356, 408), (1008, 408)], fill=RULE, width=2)

    # ---- Grid of 6 cells ----
    xs = [16, 352, 688]
    ys = [430, 704]
    for idx, (band, icon_fn, kicker, headline, sub) in enumerate(CELLS):
        x0 = xs[idx % 3]
        y0 = ys[idx // 3]
        d.rectangle([x0, y0, x0 + 319, y0 + 95], fill=band)
        icon_fn(d, x0 + 160, y0 + 48)
        d.rectangle([x0, y0, x0 + 319, y0 + 267], outline=RULE, width=2)
        d.text((x0 + 12, y0 + 106), kicker, font=font(BOLD, 17), fill=RED)
        hl = wrap(font(BOLD, 27), headline, 296)
        bottom = y0 + 122
        for i, ln in enumerate(hl):
            yy = y0 + 122 + i * 28
            d.text((x0 + 12, yy), ln, font=font(BOLD, 27), fill=INK)
            _, _, _, b = d.textbbox((x0 + 12, yy), ln, font=font(BOLD, 27))
            bottom = max(bottom, b)
        sb = wrap(font(REG, 19), sub, 296)
        for i, ln in enumerate(sb):
            d.text((x0 + 12, bottom + 4 + i * 20), ln, font=font(REG, 19),
                   fill=GREY2)

    # ---- Bottom ticker ----
    d.rectangle([4, 976, 1019, 1020], fill=NAVY)
    d.text((20, 988), "ALSO TODAY:", font=font(BOLD, 20), fill=GOLD)
    ticker_long = ("Zverev v Alcaraz, Turin final tonight  •  Cikande: 36 "
                   "missing  •  Myanmar M4.1 quake")
    ticker_short = ("Turin final tonight  •  Cikande: 36 missing  •  "
                    "Myanmar quake")
    ticker = (ticker_long if font(REG, 19).getlength(ticker_long) <= 836
              else ticker_short)
    d.text((172, 989), ticker, font=font(REG, 19), fill=WHITE)

    # ---- Outer frame (drawn last so it stays on top) ----
    d.rectangle([0, 0, 1023, 1023], outline=INK, width=4)

    img.save(out, optimize=True)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
