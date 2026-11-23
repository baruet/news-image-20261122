#!/usr/bin/env python3
"""Draw the v3 front page for news-image-20261122 (FINAL EDITION).

Renders "THE WORLD TODAY — SUNDAY 22 NOVEMBER 2026" as a dense newspaper
front page: masthead + date banner, one big lead story (COP31 collapses),
16 compact story cells in a 4x4 grid, and an "ALSO TODAY" ticker strip.
All text is drawn programmatically with PIL + DejaVu fonts; the output is
fully deterministic (no randomness, no network, no timestamps in the image).
"""

import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (25, 25, 25)
NAVY = (20, 38, 74)
GOLD = (217, 164, 65)
RED = (164, 31, 31)
CREAM = (247, 243, 232)
WHITE = (255, 255, 255)
GREY = (90, 88, 80)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = FONT_DIR + "/DejaVuSans-Bold.ttf"
F_REG = FONT_DIR + "/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_lines(draw, text, fnt, max_width, max_lines):
    """Greedy word wrap; truncate the last line with an ellipsis if needed."""
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
            if len(lines) == max_lines:
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
    # If text was cut off, mark the last line.
    full = " ".join(lines)
    if len(full) < len(text):
        last = lines[-1]
        while last and draw.textlength(last + "…", font=fnt) > max_width:
            last = last[:-1]
        lines[-1] = (last + "…").strip()
    return lines


def fit_text(draw, text, fnt_path, start_size, min_size, max_width, max_lines):
    """Shrink the font until the text fits in max_lines at max_width."""
    size = start_size
    while size >= min_size:
        fnt = font(fnt_path, size)
        lines = wrap_lines(draw, text, fnt, max_width, max_lines)
        joined = " ".join(lines)
        if len(joined) >= len(text) or size == min_size:
            return fnt, lines
        size -= 1
    fnt = font(fnt_path, min_size)
    return fnt, wrap_lines(draw, text, fnt, max_width, max_lines)


def draw_sun(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    for k in range(8):
        a = math.pi * k / 4.0
        x1 = cx + int(math.cos(a) * (r + 4))
        y1 = cy + int(math.sin(a) * (r + 4))
        x2 = cx + int(math.cos(a) * (r + 12))
        y2 = cy + int(math.sin(a) * (r + 12))
        d.line([x1, y1, x2, y2], fill=color, width=3)


def draw_waves(d, x0, y0, x1, y1, color):
    for row in range(3):
        yy = y0 + row * 9
        pts = []
        for x in range(x0, x1 + 1, 8):
            pts.append((x, yy + int(3 * math.sin((x - x0) / 14.0))))
        d.line(pts, fill=color, width=2)


def draw_target(d, cx, cy, r, color):
    for i, rr in enumerate([r, int(r * 0.66), int(r * 0.33)]):
        if i == 2:
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=color)
        else:
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=color, width=3)


def draw_flame(d, x0, y0, x1, y1, color):
    cx = (x0 + x1) // 2
    pts = [(cx, y0), (x1 - 2, y0 + (y1 - y0) // 2), (cx + 4, y1),
           (cx - 2, y1 - 6), (x0 + 2, y1 - 2), (x0 + 6, y0 + (y1 - y0) // 2)]
    d.polygon(pts, fill=color)


def draw_stumps(d, x0, y0, x1, y1, color):
    # Three cricket stumps + a diagonal bat + a ball.
    w = (x1 - x0) // 5
    for i in range(3):
        xx = x0 + i * (w + 2)
        d.rectangle([xx, y0 + 4, xx + w, y1 - 8], fill=color)
    d.line([x1 - 12, y0 + 2, x1 - 2, y1 - 10], fill=color, width=4)
    d.ellipse([x1 - 8, y1 - 8, x1, y1], fill=color)


def draw_checker(d, x0, y0, x1, y1, color):
    # A small chequered flag.
    n = 4
    cw = (x1 - x0) // n
    ch = (y1 - y0) // n
    for r in range(n):
        for c in range(n):
            if (r + c) % 2 == 0:
                d.rectangle([x0 + c * cw, y0 + r * ch,
                             x0 + (c + 1) * cw, y0 + (r + 1) * ch], fill=color)
    d.line([x0, y0, x0, y1], fill=color, width=3)


def draw_ball(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
    d.arc([cx - r, cy - r, cx + r, cy + r], start=300, end=60, fill=color, width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], start=120, end=240, fill=color, width=2)


def draw_star(d, cx, cy, r, color):
    pts = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else int(r * 0.45)
        pts.append((cx + int(math.cos(ang) * rr), cy + int(math.sin(ang) * rr)))
    d.polygon(pts, fill=color)


def draw_globe(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
    d.ellipse([cx - int(r * 0.45), cy - r, cx + int(r * 0.45), cy + r],
              outline=color, width=2)
    d.line([cx - r, cy, cx + r, cy], fill=color, width=2)


def draw_bridge(d, x0, y0, x1, y1, color):
    d.arc([x0, y0, x1, y1 + (y1 - y0)], start=180, end=360, fill=color, width=3)
    for i in range(5):
        xx = x0 + (i + 1) * (x1 - x0) // 6
        d.line([xx, y0 + (y1 - y0) // 2, xx, y1], fill=color, width=2)
    d.line([x0, y1, x1, y1], fill=color, width=3)


def draw_bars(d, x0, y0, x1, y1, color):
    n = 4
    bw = (x1 - x0) // (n * 2)
    for i in range(n):
        h = (y1 - y0) * (i + 1) // (n + 1)
        xx = x0 + i * 2 * bw
        d.rectangle([xx, y1 - h, xx + bw, y1], fill=color)


def draw_megaphone(d, x0, y0, x1, y1, color):
    pts = [(x0, y0 + (y1 - y0) // 3), (x1 - 6, y0), (x1 - 6, y1),
           (x0, y0 + 2 * (y1 - y0) // 3)]
    d.polygon(pts, fill=color)
    d.line([x0 + 2, y1 - 4, x0 + 10, y1 - 4], fill=color, width=3)


def draw_burst(d, cx, cy, r, color):
    pts = []
    for k in range(16):
        ang = k * math.pi / 8
        rr = r if k % 2 == 0 else int(r * 0.4)
        pts.append((cx + int(math.cos(ang) * rr), cy + int(math.sin(ang) * rr)))
    d.polygon(pts, fill=color)


def draw_ship(d, x0, y0, x1, y1, color):
    mid = (y0 + y1) // 2
    d.polygon([(x0, mid), (x1, mid), (x1 - 8, y1), (x0 + 8, y1)], fill=color)
    d.line([(x0 + x1) // 2, y0, (x0 + x1) // 2, mid], fill=color, width=3)
    d.polygon([((x0 + x1) // 2, y0), ((x0 + x1) // 2 + 14, mid - 2),
               ((x0 + x1) // 2, mid - 2)], fill=color)


def draw_cap(d, x0, y0, x1, y1, color):
    cx = (x0 + x1) // 2
    d.polygon([(x0, y0 + (y1 - y0) // 2), (cx, y0), (x1, y0 + (y1 - y0) // 2),
               (x1 - 4, y1), (x0 + 4, y1)], fill=color)
    d.line([x0, y0 + (y1 - y0) // 2, x1, y0 + (y1 - y0) // 2], fill=color, width=2)


def draw_boat(d, x0, y0, x1, y1, color):
    mid = (y0 + y1) // 2
    d.polygon([(x0, mid), (x1, mid), (x1 - 6, y1), (x0 + 6, y1)], fill=color)
    d.line([(x0 + x1) // 2, y0, (x0 + x1) // 2, mid], fill=color, width=2)
    d.polygon([((x0 + x1) // 2 + 2, y0 + 2), ((x0 + x1) // 2 + 2, mid - 2),
               ((x0 + x1) // 2 + 16, mid - 2)], fill=color)


def draw_plane(d, x0, y0, x1, y1, color):
    # Simple side-view plane: fuselage, nose, wings, tail.
    my = (y0 + y1) // 2
    d.line([x0 + 2, my, x1 - 6, my], fill=color, width=4)
    d.polygon([(x1 - 14, my), (x1 - 2, my), (x1 - 8, my - 6)], fill=color)
    d.line([(x0 + x1) // 2, my, (x0 + x1) // 2 - 4, y0 + 2], fill=color, width=3)
    d.line([(x0 + x1) // 2, my, (x0 + x1) // 2 - 4, y1 - 2], fill=color, width=3)
    d.line([x0 + 4, my, x0 + 2, y0 + 4], fill=color, width=3)


ICONS = {
    "sun": draw_sun, "target": draw_target, "flame": draw_flame,
    "stumps": draw_stumps, "checker": draw_checker, "ball": draw_ball,
    "star": draw_star, "globe": draw_globe, "bridge": draw_bridge,
    "bars": draw_bars, "megaphone": draw_megaphone, "burst": draw_burst,
    "ship": draw_ship, "cap": draw_cap, "boat": draw_boat, "plane": draw_plane,
}


def draw_icon(d, kind, box, color):
    """Draw a small white glyph centred in box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = min(x1 - x0, y1 - y0) // 2 - 2
    fn = ICONS[kind]
    if kind in ("sun", "target", "ball", "star", "burst", "globe"):
        fn(d, cx, cy, r, color)
    else:
        fn(d, x0 + 3, y0 + 3, x1 - 3, y1 - 3, color)


# ---------------------------------------------------------------------------
# The stories. Every item happened or was first reported on Sunday 22 Nov 2026.
# Sources checked 23 Nov: Reuters / AP / ATP Tour / formula1.com / Le Monde.
# ---------------------------------------------------------------------------

LEAD = {
    "kicker": "LEAD STORY  •  CLIMATE  •  ANTALYA",
    "headline": "COP31 COLLAPSES",
    "subline": "NO DEAL IN ANTALYA — LONGEST COP EVER",
    "body": ("EU and 130 nations reject a text with no fossil fuels. "
             "The longest COP ever ends without a deal."),
    "caption": "ANTALYA  •  COP31",
}

# (kicker, headline, body, icon, band colour)
CELLS = [
    ("MIDDLE EAST  •  BAHRAIN",
     "IRAN HITS US BASES",
     "IRGC claims hits on US Patriot radars; Bahrain reports a civilian site hit.",
     "target", (143, 29, 29)),
    ("EUROPE  •  UKRAINE",
     "186 DRONES HIT KYIV",
     "Overnight barrage; a block in Dymer collapses — 4 killed, 14 missing.",
     "burst", (20, 38, 74)),
    ("EUROPE  •  BALTIC",
     "SPARTA II STILL BURNING",
     "Struck Saturday, the cargo ship burns on off Finland; 16 crew evacuated.",
     "flame", (110, 20, 35)),
    ("SPORT  •  CRICKET",
     "INDIA 720/9 IN WELLINGTON",
     "Pant 128, Rahul 136; all seven pairs pass 50; NZ 119/2, trail 233.",
     "stumps", (30, 92, 46)),
    ("SPORT  •  FORMULA 1",
     "VERSTAPPEN WINS VEGAS",
     "From pole, 35 lead changes; beats Norris by 0.6s; 3rd Vegas win in 4 years.",
     "checker", (75, 42, 107)),
    ("SPORT  •  TENNIS",
     "ALCARAZ TAKES TURIN",
     "Beats No. 1 Zverev 6-2, 7-6(7); first ATP Finals title; a 5-0 week.",
     "ball", (15, 91, 91)),
    ("EUROPE  •  BELGIUM",
     "BELGIUM FLIGHTS GROUNDED",
     "Skeyes halts air traffic control; Monday flights cancelled; 429 flights hit.",
     "plane", (154, 106, 18)),
    ("ASIA  •  DIPLOMACY",
     "NEPAL PM IN NEW DELHI",
     "Balendra Shah's first bilateral visit since March; Modi talks Monday.",
     "globe", (29, 58, 110)),
    ("ASIA  •  INDIA",
     "MODI OPENS NITISH SETU",
     "New Patna–Vaishali bridge; projects worth Rs 34,000 crore unveiled.",
     "bridge", (110, 20, 35)),
    ("TRADE  •  ASIA",
     "INDIA, CANADA WRAP TRADE TALKS",
     "Latest round tied up as a Modi visit nears; both sides eye a deal.",
     "bars", (30, 92, 46)),
    ("ASIA  •  INDONESIA",
     "36 MISSING IN FACTORY FIRE",
     "Cikande candy plant blaze kills 3, hurts 4; rescuers search on Sunday.",
     "flame", (143, 29, 29)),
    ("EUROPE  •  FRANCE",
     "FRANCE PROTESTS, 6TH WEEKEND",
     "Tens of thousands march over living costs and police powers.",
     "megaphone", (20, 38, 74)),
    ("MIDDLE EAST  •  ISRAEL",
     "SETTLER ARSON IN WEST BANK",
     "Settlers torch villages early Sunday; Eisenkot condemns; police probe.",
     "burst", (110, 20, 35)),
    ("AFRICA  •  LIBYA",
     "RUSSIAN SHIP SUNK OFF LIBYA",
     "Corvette Merkury sunk after a drone strike in Benghazi; Kyiv suspected.",
     "ship", (15, 91, 91)),
    ("ASIA  •  KOREA",
     "SOUTH KOREA MINISTER QUITS",
     "Education chief resigns over AI-cheating exam rule chaos.",
     "cap", (75, 42, 107)),
    ("AFRICA  •  NIGERIA",
     "NIGERIA BOAT CAPSIZES",
     "24 mourners drown as their boat overturns on the river.",
     "boat", (29, 58, 110)),
]

TICKER = ("ALSO TODAY:  Brazil storm kills 3   •   Myanmar M4.1 quake   •   "
          "Gaza aid-truck strike, 3 killed")


def draw_cell(d, x, y, w, h, cell):
    kicker, headline, body, icon, band = cell
    # Card outline and icon band.
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=(200, 192, 172), width=1)
    d.rectangle([x, y, x + w - 1, y + 30], fill=band)
    draw_icon(d, icon, (x + 4, y + 3, x + 30, y + 27), WHITE)
    # Region kicker, right of the glyph.
    kf = font(F_BOLD, 14)
    d.text((x + 34, y + 8), kicker, font=kf, fill=WHITE)
    inner = w - 16
    # Headline, up to 2 lines, shrinking if needed.
    hf, hlines = fit_text(d, headline, F_BOLD, 24, 20, inner, 2)
    hy = y + 36
    for ln in hlines:
        d.text((x + 8, hy), ln, font=hf, fill=INK)
        hy += 27
    # Body, up to 3 lines, shrinking if needed.
    bf, blines = fit_text(d, body, F_REG, 18, 15, inner, 3)
    by = y + 92
    for ln in blines:
        d.text((x + 8, by), ln, font=bf, fill=(60, 58, 50))
        by += 20


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- Masthead ------------------------------------------------------------
    d.rectangle([0, 0, W - 1, 95], fill=NAVY)
    ef = font(F_BOLD, 17)
    d.text((24, 12), "FINAL EDITION", font=ef, fill=GOLD)
    tf = font(F_BOLD, 42)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 6), title, font=tf, fill=GOLD)
    df = font(F_BOLD, 33)
    date = "SUNDAY 22 NOVEMBER 2026"
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 52), date, font=df, fill=WHITE)
    d.line([0, 97, W - 1, 97], fill=GOLD, width=3)

    # --- Lead story ----------------------------------------------------------
    lx, ly, lw, lh = 12, 106, 1000, 172
    d.rectangle([lx, ly, lx + lw - 1, ly + lh - 1], outline=(200, 192, 172), width=1)
    # Left image panel: sun over waves on navy.
    px0, py0, px1, py1 = lx, ly, lx + 280, ly + lh - 1
    d.rectangle([px0, py0, px1, py1], fill=NAVY)
    draw_sun(d, px0 + 140, py0 + 62, 34, GOLD)
    draw_waves(d, px0 + 24, py1 - 58, px1 - 24, py1 - 20, GOLD)
    cf = font(F_BOLD, 17)
    d.text((px0 + 16, py1 - 26), LEAD["caption"], font=cf, fill=WHITE)
    # Right: kicker, headline, body.
    tx = px1 + 16
    twd = lx + lw - 16 - tx
    kf = font(F_BOLD, 19)
    d.text((tx, ly + 10), LEAD["kicker"], font=kf, fill=RED)
    hf, hlines = fit_text(d, LEAD["headline"], F_BOLD, 44, 36, twd, 1)
    hy = ly + 34
    for ln in hlines:
        d.text((tx, hy), ln, font=hf, fill=INK)
        hy += 50
    sf = font(F_BOLD, 22)
    d.text((tx, ly + 86), LEAD["subline"], font=sf, fill=RED)
    bf, blines = fit_text(d, LEAD["body"], F_REG, 21, 18, twd, 2)
    by = ly + 118
    for ln in blines:
        d.text((tx, by), ln, font=bf, fill=(60, 58, 50))
        by += 26
    d.line([12, 288, W - 13, 288], fill=(200, 192, 172), width=1)

    # --- 4x4 story grid ------------------------------------------------------
    gx, gy = 12, 298
    gw = (W - 24 - 3 * 8) // 4
    gh = 156
    for i, cell in enumerate(CELLS):
        row, col = divmod(i, 4)
        draw_cell(d, gx + col * (gw + 8), gy + row * (gh + 8), gw, gh, cell)

    # --- Ticker --------------------------------------------------------------
    d.rectangle([0, 964, W - 1, H - 1], fill=NAVY)
    tf2 = font(F_BOLD, 16)
    tw2 = d.textlength(TICKER, font=tf2)
    d.text(((W - tw2) / 2, 988), TICKER, font=tf2, fill=WHITE)
    d.line([0, 962, W - 1, 962], fill=GOLD, width=2)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    draw()
