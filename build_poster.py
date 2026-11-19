#!/usr/bin/env python3
"""Build the news poster for 18 November 2026.

Draws a 1024x1024 newspaper-style poster with PIL only: a big date header
and six panels, one per top story of Wednesday 18 November 2026, each with a
simple pictogram, a bold headline and a short factual subline.

Stories (all reported on 18 Nov 2026; sources: Reuters, AP, BBC, PAHO, UN,
CNBC via the day's news digests):
  1. Iran strikes Kuwait and Bahrain after the U.S. hit Qeshm Island.
  2. Ukraine hits the Kerch Bridge a second day; a road span collapses.
  3. Xi Jinping and Vladimir Putin meet in Shenzhen ahead of a trilateral
     summit with Donald Trump on Thursday.
  4. Democrat Mary Peltola wins Alaska's Senate seat; Democrats take a
     56-44 majority.
  5. Nvidia posts a record $115.8B quarter; its board rejects Jensen
     Huang's offer to return as CEO.
  6. The Ebola outbreak in DR Congo passes 11,000 cases, 5,400 dead.

Run: python3 build_poster.py  ->  writes entry.png next to this file.
"""

import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (245, 241, 232)
NAVY = (16, 39, 63)
CARD = (255, 255, 255)
BORDER = (206, 200, 186)
INK = (24, 28, 34)
MUTED = (88, 92, 98)
FOOTER_INK = (110, 112, 116)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_burst(d, cx, cy, r, color, spikes=12):
    pts = []
    for i in range(spikes * 2):
        ang = math.pi * i / spikes
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=color)
    d.ellipse([cx - r * 0.28, cy - r * 0.28, cx + r * 0.28, cy + r * 0.28],
              fill=(255, 255, 255))


def draw_bridge(d, x, y, w, h, color):
    # Two deck segments with a broken gap in the middle, cables, one falling piece.
    deck_y = y + h * 0.62
    d.line([(x, deck_y), (x + w * 0.38, deck_y)], fill=color, width=7)
    d.line([(x + w * 0.62, deck_y), (x + w, deck_y)], fill=color, width=7)
    # Support towers
    d.line([(x + w * 0.16, y + h * 0.18), (x + w * 0.16, deck_y)],
           fill=color, width=6)
    d.line([(x + w * 0.84, y + h * 0.18), (x + w * 0.84, deck_y)],
           fill=color, width=6)
    # Cables (two per tower, for a fuller span)
    d.line([(x + w * 0.16, y + h * 0.18), (x + w * 0.38, deck_y)],
           fill=color, width=3)
    d.line([(x + w * 0.16, y + h * 0.18), (x + w * 0.30, deck_y)],
           fill=color, width=3)
    d.line([(x + w * 0.84, y + h * 0.18), (x + w * 0.62, deck_y)],
           fill=color, width=3)
    d.line([(x + w * 0.84, y + h * 0.18), (x + w * 0.70, deck_y)],
           fill=color, width=3)
    # Falling piece in the gap, tilted and larger
    d.polygon([(x + w * 0.42, y + h * 0.74), (x + w * 0.58, y + h * 0.68),
               (x + w * 0.62, y + h * 0.84), (x + w * 0.46, y + h * 0.90)],
              fill=color)
    # Water below
    for i, xx in enumerate(range(int(x), int(x + w), 14)):
        d.line([(xx, y + h * 0.94), (xx + 8, y + h * 0.94)],
               fill=color, width=3)


def draw_flags(d, x, y, w, h):
    # Three small flags stacked vertically: China, Russia, USA
    # (simplified). A horizontal row would not fit the icon column.
    fw, fh, gap = w * 0.92, h * 0.28, h * 0.04
    fx = x + (w - fw) / 2
    fy = y + (h - (3 * fh + 2 * gap)) / 2
    # China: red field, yellow stars
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16),
                outline=(120, 120, 120), width=2)
    for sx, sy, sr in [(0.16, 0.5, 0.26), (0.42, 0.28, 0.11),
                       (0.5, 0.62, 0.11), (0.34, 0.78, 0.11)]:
        draw_burst(d, fx + fw * sx, fy + fh * sy, fh * sr, (255, 222, 0), 5)
    # Russia: white / blue / red horizontal stripes
    ry = fy + fh + gap
    d.rectangle([fx, ry, fx + fw, ry + fh / 3], fill=(255, 255, 255),
                outline=(120, 120, 120), width=2)
    d.rectangle([fx, ry + fh / 3, fx + fw, ry + 2 * fh / 3], fill=(0, 57, 166))
    d.rectangle([fx, ry + 2 * fh / 3, fx + fw, ry + fh], fill=(213, 0, 50))
    # USA: red/white stripes with a blue canton and star dots
    uy = ry + fh + gap
    for i in range(7):
        d.rectangle([fx, uy + i * fh / 7, fx + fw, uy + (i + 1) * fh / 7],
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([fx, uy, fx + fw * 0.45, uy + fh * 0.55], fill=(60, 59, 110))
    for sx in (0.12, 0.28):
        for sy in (0.15, 0.35):
            d.ellipse([fx + fw * sx - 2, uy + fh * sy - 2,
                       fx + fw * sx + 2, uy + fh * sy + 2], fill=(255, 255, 255))
    d.rectangle([fx, uy, fx + fw, uy + fh], outline=(120, 120, 120), width=2)


def draw_ballot(d, x, y, w, h, color):
    # Ballot box with a slot and a big check mark.
    d.rectangle([x + w * 0.08, y + h * 0.35, x + w * 0.92, y + h * 0.95],
                fill=color)
    d.rectangle([x + w * 0.08, y + h * 0.35, x + w * 0.92, y + h * 0.52],
                fill=(255, 255, 255), outline=color, width=3)
    d.line([(x + w * 0.3, y + h * 0.43), (x + w * 0.7, y + h * 0.43)],
           fill=color, width=5)
    # Check mark
    d.line([(x + w * 0.18, y + h * 0.62), (x + w * 0.42, y + h * 0.85),
            (x + w * 0.86, y + h * 0.28)], fill=(255, 255, 255), width=9,
           joint="curve")


def draw_chip(d, x, y, w, h, color):
    # Microchip: square body, inner square, pins on all sides.
    d.rectangle([x + w * 0.2, y + h * 0.2, x + w * 0.8, y + h * 0.8],
                fill=color)
    d.rectangle([x + w * 0.36, y + h * 0.36, x + w * 0.64, y + h * 0.64],
                outline=(255, 255, 255), width=4)
    for i in range(3):
        t = 0.3 + i * 0.2
        d.line([(x + w * t, y), (x + w * t, y + h * 0.2)], fill=color, width=5)
        d.line([(x + w * t, y + h * 0.8), (x + w * t, y + h)], fill=color, width=5)
        d.line([(x, y + h * t), (x + w * 0.2, y + h * t)], fill=color, width=5)
        d.line([(x + w * 0.8, y + h * t), (x + w, y + h * t)], fill=color, width=5)


def draw_virus(d, x, y, w, h, color):
    cx, cy, r = x + w / 2, y + h / 2, w * 0.3
    for i in range(10):
        ang = 2 * math.pi * i / 10
        d.line([(cx + r * 0.85 * math.cos(ang), cy + r * 0.85 * math.sin(ang)),
                (cx + r * 1.45 * math.cos(ang), cy + r * 1.45 * math.sin(ang))],
               fill=color, width=6)
        d.ellipse([cx + r * 1.45 * math.cos(ang) - 5,
                   cy + r * 1.45 * math.sin(ang) - 5,
                   cx + r * 1.45 * math.cos(ang) + 5,
                   cy + r * 1.45 * math.sin(ang) + 5], fill=color)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    for dx, dy in [(-0.35, -0.3), (0.3, 0.25), (0.05, -0.45)]:
        d.ellipse([cx + r * dx - 6, cy + r * dy - 6,
                   cx + r * dx + 6, cy + r * dy + 6], fill=(255, 255, 255))


ICONS = {
    "burst": lambda d, x, y, w, h, c: draw_burst(d, x + w / 2, y + h / 2,
                                                w * 0.42, c),
    "bridge": draw_bridge,
    "flags": lambda d, x, y, w, h, c: draw_flags(d, x, y, w, h),
    "ballot": draw_ballot,
    "chip": draw_chip,
    "virus": draw_virus,
}

STORIES = [
    ("burst", (192, 57, 43),
     "IRAN STRIKES KUWAIT & BAHRAIN",
     "After the U.S. hit Qeshm Island; the Gulf on edge"),
    ("bridge", (46, 94, 140),
     "KERCH BRIDGE HIT AGAIN",
     "A road span falls into the strait"),
    ("flags", (142, 68, 173),
     "XI & PUTIN MEET IN SHENZHEN",
     "Trilateral summit with Trump on Thursday"),
    ("ballot", (31, 97, 141),
     "PELTOLA WINS ALASKA SENATE",
     "Democrats take a 56\u201344 majority"),
    ("chip", (30, 132, 73),
     "NVIDIA'S RECORD $115.8B QUARTER",
     "Board rejects Huang's return as CEO"),
    ("virus", (146, 43, 33),
     "EBOLA PASSES 11,000 CASES IN CONGO",
     "5,400 dead; children hit hardest"),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Header band -------------------------------------------------
    d.rectangle([0, 0, W, 168], fill=NAVY)
    f_kicker = font(FONT_BOLD, 25)
    f_date = font(FONT_BOLD, 66)
    f_sub = font(FONT_REG, 24)
    kicker = "T H E   W O R L D   I N   O N E   D A Y"
    d.text(((W - d.textlength(kicker, font=f_kicker)) / 2, 16), kicker,
           font=f_kicker, fill=(214, 178, 94))
    date = "18 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 48), date,
           font=f_date, fill=(255, 255, 255))
    sub = "Wednesday  \u00b7  Six stories that defined the day"
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 128), sub,
           font=f_sub, fill=(190, 200, 212))

    # ---- Story grid: 2 cols x 3 rows ---------------------------------
    margin, gap = 24, 16
    grid_top, grid_bottom = 188, 972
    col_w = (W - 2 * margin - gap) // 2
    row_h = (grid_bottom - grid_top - 2 * gap) // 3
    f_head = font(FONT_BOLD, 31)
    f_body = font(FONT_REG, 21)

    for i, (icon, accent, headline, subline) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = margin + col * (col_w + gap)
        y0 = grid_top + row * (row_h + gap)
        x1, y1 = x0 + col_w, y0 + row_h
        d.rectangle([x0, y0, x1, y1], fill=CARD, outline=BORDER, width=2)
        d.rectangle([x0, y0, x1, y0 + 8], fill=accent)
        # Measure the text block first, then centre icon + text vertically.
        tx = x0 + 148
        tw = x1 - tx - 18
        head_lines = wrap(d, headline, f_head, tw)
        body_lines = wrap(d, subline, f_body, tw)
        block_h = (len(head_lines) * 38 + 8 + len(body_lines) * 27)
        block_top = y0 + (row_h - block_h) // 2 + 4
        # Icon on the left, centred on the same block
        ix, iy, iw, ih = x0 + 16, block_top - 8, 120, 120
        ICONS[icon](d, ix, iy, iw, ih, accent)
        # Headline + subline on the right
        ly = block_top
        for ln in head_lines:
            d.text((tx, ly), ln, font=f_head, fill=INK)
            ly += 38
        ly += 8
        for ln in body_lines:
            d.text((tx, ly), ln, font=f_body, fill=MUTED)
            ly += 27

    # ---- Footer -------------------------------------------------------
    f_foot = font(FONT_REG, 17)
    foot = ("Sources: Reuters  \u00b7  Associated Press  \u00b7  BBC  \u00b7  PAHO  \u00b7  "
            "United Nations  \u00b7  CNBC   \u2014   reported 18 November 2026")
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, 984), foot,
           font=f_foot, fill=FOOTER_INK)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
