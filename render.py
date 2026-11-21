#!/usr/bin/env python3
"""Render 'The World Today' -- a 1024x1024 newspaper front page summing up
the world news of Friday 20 November 2026.

Deterministic: no network, no randomness, no timestamps. Running it twice
produces a byte-identical entry.png. Only Pillow and the DejaVu system fonts
are used; every illustration is drawn from code.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
MARGIN = 28
CONTENT_W = W - 2 * MARGIN

PAPER = (248, 244, 233)
INK = (26, 26, 26)
RED = (185, 28, 28)
BLUE = (31, 58, 95)
GREY = (110, 108, 100)
LIGHT_LINE = (180, 175, 160)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, fnt, x, y, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fit_text(draw, text, fnt, max_w, max_lines, x, y, fill, leading,
             min_size=None):
    """Wrap text to fit; shrink the font (serif/sans bold kept) if needed."""
    lines = wrap(text, fnt, max_w)
    size = fnt.size
    while len(lines) > max_lines and min_size is not None and size > min_size:
        size -= 1
        fnt = ImageFont.truetype(fnt.path, size)
        lines = wrap(text, fnt, max_w)
    return draw_lines(draw, lines[:max_lines], fnt, x, y, fill, leading)


# ---------------------------------------------------------------- stories

LEAD = {
    "kicker": "KYIV, UKRAINE",
    "headline": "Russia hits Kyiv's bridges in overnight barrage",
    "summary": ("Russian missiles struck three of Kyiv's road bridges "
                "overnight, killing eight people and injuring 28 across "
                "nine regions, the capital's mayor said, as explosions "
                "lit up the city and debris set a tower block ablaze."),
    "source": "Source: Reuters",
}

STORIES = [
    {
        "kicker": "WARSAW, POLAND",
        "headline": "Russian missile crashes in Poland",
        "summary": ("Poland said two Russian missiles and a drone violated "
                    "its airspace overnight. Warsaw condemned the incursion "
                    "as intentional."),
        "source": "Source: BBC",
        "art": "poland",
    },
    {
        "kicker": "BRUSSELS",
        "headline": "UK and EU agree new deal at summit",
        "summary": ("Britain and the EU agreed a deal on food exports, "
                    "emissions trading and a youth mobility scheme at "
                    "their Brussels summit."),
        "source": "Source: BBC",
        "art": "ukeu",
    },
    {
        "kicker": "WASHINGTON",
        "headline": "Trump threatens ban on overseas AI data centres",
        "summary": ("President Trump threatened to ban US firms from "
                    "building AI data centres abroad, escalating his "
                    "technology crackdown."),
        "source": "Source: BBC",
        "art": "datacentre",
    },
    {
        "kicker": "RIYADH",
        "headline": "Houthi missile hits Riyadh tower",
        "summary": ("A Houthi missile damaged the sovereign wealth fund "
                    "tower in Riyadh, and Saudi defences intercepted more "
                    "missiles on Friday."),
        "source": "Source: AP / Sky News",
        "art": "riyadh",
    },
    {
        "kicker": "NEW YORK",
        "headline": "Tech sell-off deepens after Anthropic debut",
        "summary": ("Anthropic shares fell a day after their blockbuster "
                    "Nasdaq debut, and Asian markets slid \u2014 Japan's "
                    "Nikkei down 4.8%."),
        "source": "Source: BBC / CNBC",
        "art": "stocks",
    },
    {
        "kicker": "EUROPE",
        "headline": "Cost-of-living protests sweep Europe",
        "summary": ("Thousands marched across Europe on Friday against "
                    "the cost of living, in coordinated protests over "
                    "prices and household bills."),
        "source": "Source: BBC",
        "art": "protest",
    },
    {
        "kicker": "SPACE",
        "headline": "BepiColombo reaches Mercury after eight years",
        "summary": ("The BepiColombo probe reached Mercury after an "
                    "eight-year, six-billion-mile voyage; it enters orbit "
                    "on Saturday."),
        "source": "Source: BBC / NPR",
        "art": "mercury",
    },
]


# ------------------------------------------------------- illustration art

def burst(draw, cx, cy, r, colour):
    """Spiky explosion burst centred on (cx, cy)."""
    pts = []
    for i in range(16):
        ang = math.pi * 2 * i / 16
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=colour)
    draw.ellipse([cx - r * 0.35, cy - r * 0.35, cx + r * 0.35, cy + r * 0.35],
                 fill=(255, 220, 120))


def art_kyiv(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(16, 24, 54))
    for sx, sy, sr in [(0.12, 0.18, 2), (0.3, 0.1, 2), (0.55, 0.22, 3),
                       (0.72, 0.12, 2), (0.88, 0.28, 2), (0.45, 0.3, 2)]:
        draw.ellipse([x + w * sx - sr, y + h * sy - sr,
                      x + w * sx + sr, y + h * sy + sr], fill=(240, 240, 220))
    # city skyline
    for bx, bw, bh in [(0.02, 0.10, 0.30), (0.14, 0.08, 0.42), (0.24, 0.12, 0.26),
                       (0.62, 0.09, 0.36), (0.73, 0.11, 0.28), (0.86, 0.10, 0.40)]:
        draw.rectangle([x + w * bx, y + h * (0.72 - bh), x + w * (bx + bw),
                        y + h * 0.72], fill=(8, 12, 30))
    # river
    draw.rectangle([x, y + h * 0.72, x + w, y + h], fill=(28, 52, 96))
    # bridge arc across the river (kept inside the illustration)
    draw.arc([x + w * 0.05, y + h * 0.55, x + w * 0.95, y + h * 1.02],
             start=200, end=340, fill=(200, 200, 190), width=6)
    draw.line([x + w * 0.30, y + h * 0.72, x + w * 0.30, y + h * 0.88],
              fill=(200, 200, 190), width=4)
    draw.line([x + w * 0.68, y + h * 0.72, x + w * 0.68, y + h * 0.88],
              fill=(200, 200, 190), width=4)
    # explosion over the bridge
    burst(draw, x + w * 0.5, y + h * 0.42, 34, (255, 140, 40))
    for sx, sy, sr in [(0.42, 0.30, 12), (0.60, 0.32, 9), (0.52, 0.24, 7)]:
        draw.ellipse([x + w * sx - sr, y + h * sy - sr,
                      x + w * sx + sr, y + h * sy + sr], fill=(90, 90, 95))


def art_poland(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(214, 232, 245))
    draw.rectangle([x, y + h * 0.62, x + w, y + h], fill=(96, 160, 96))
    # dashed border line
    for i in range(9):
        bx = x + w * (0.05 + i * 0.11)
        draw.line([bx, y + h * 0.62, bx + w * 0.06, y + h * 0.62],
                  fill=(120, 40, 40), width=3)
    # Polish flag
    draw.rectangle([x + w * 0.10, y + h * 0.16, x + w * 0.34, y + h * 0.34],
                   fill=(255, 255, 255), outline=(60, 60, 60), width=2)
    draw.rectangle([x + w * 0.10, y + h * 0.25, x + w * 0.34, y + h * 0.34],
                   fill=(220, 20, 60))
    draw.line([x + w * 0.10, y + h * 0.16, x + w * 0.10, y + h * 0.62],
              fill=(60, 60, 60), width=3)
    # missile streaking down
    draw.line([x + w * 0.86, y + h * 0.10, x + w * 0.58, y + h * 0.52],
              fill=(255, 120, 30), width=5)
    draw.line([x + w * 0.58, y + h * 0.52, x + w * 0.50, y + h * 0.60],
              fill=(60, 60, 60), width=7)
    burst(draw, x + w * 0.48, y + h * 0.62, 14, (255, 140, 40))
    # warning triangle
    tri = [(x + w * 0.78, y + h * 0.66), (x + w * 0.92, y + h * 0.92),
           (x + w * 0.64, y + h * 0.92)]
    draw.polygon(tri, fill=(255, 200, 0), outline=(0, 0, 0))
    draw.text((x + w * 0.765, y + h * 0.76), "!", font=font(SANS_B, 18),
              fill=(0, 0, 0))


def art_ukeu(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(30, 60, 120))
    # EU flag: circle of stars
    cx, cy, r = x + w * 0.28, y + h * 0.42, h * 0.26
    for i in range(12):
        ang = math.pi * 2 * i / 12 - math.pi / 2
        sx, sy = cx + r * math.cos(ang), cy + r * math.sin(ang)
        draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 220, 60))
    # Union Jack, simplified
    fx, fy, fw, fh = x + w * 0.58, y + h * 0.18, w * 0.34, h * 0.48
    draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(20, 40, 120),
                   outline=(255, 255, 255), width=2)
    draw.line([fx, fy, fx + fw, fy + fh], fill=(255, 255, 255), width=5)
    draw.line([fx + fw, fy, fx, fy + fh], fill=(255, 255, 255), width=5)
    draw.line([fx + fw / 2, fy, fx + fw / 2, fy + fh], fill=(200, 30, 40),
              width=7)
    draw.line([fx, fy + fh / 2, fx + fw, fy + fh / 2], fill=(200, 30, 40),
              width=7)
    # summit table
    draw.rectangle([x + w * 0.08, y + h * 0.78, x + w * 0.92, y + h * 0.86],
                   fill=(120, 82, 50))
    draw.rectangle([x + w * 0.14, y + h * 0.86, x + w * 0.20, y + h],
                   fill=(90, 60, 36))
    draw.rectangle([x + w * 0.80, y + h * 0.86, x + w * 0.86, y + h],
                   fill=(90, 60, 36))


def art_datacentre(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 234, 238))
    # server racks
    for i, rx in enumerate([0.08, 0.40, 0.72]):
        draw.rectangle([x + w * rx, y + h * 0.18, x + w * (rx + 0.20),
                        y + h * 0.82], fill=(70, 80, 95),
                       outline=(40, 45, 55), width=2)
        for j in range(4):
            yy = y + h * (0.26 + j * 0.14)
            draw.rectangle([x + w * (rx + 0.03), yy,
                            x + w * (rx + 0.17), yy + h * 0.07],
                           fill=(120, 200, 120) if j % 2 else (90, 140, 200))
    # big red ban circle over "AI"
    cx, cy, r = x + w * 0.5, y + h * 0.5, h * 0.34
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
                 outline=RED, width=6)
    draw.text((cx - 13, cy - 15), "AI", font=font(SANS_B, 24), fill=INK)
    draw.line([cx - r * 0.7, cy + r * 0.7, cx + r * 0.7, cy - r * 0.7],
              fill=RED, width=6)


def art_riyadh(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(250, 190, 110))
    draw.ellipse([x + w * 0.78, y + h * 0.08, x + w * 0.98, y + h * 0.28],
                 fill=(255, 240, 180))
    # skyline
    for bx, bw, bh in [(0.00, 0.12, 0.30), (0.14, 0.10, 0.42), (0.26, 0.12, 0.24),
                       (0.62, 0.10, 0.36), (0.74, 0.12, 0.28), (0.88, 0.12, 0.44)]:
        draw.rectangle([x + w * bx, y + h * (0.95 - bh), x + w * (bx + bw),
                        y + h * 0.95], fill=(70, 45, 60))
    # twisted PIF tower
    tx = x + w * 0.44
    draw.polygon([(tx, y + h * 0.12), (tx + w * 0.10, y + h * 0.12),
                  (tx + w * 0.07, y + h * 0.95), (tx + w * 0.03, y + h * 0.95)],
                 fill=(52, 68, 110))
    for j in range(6):
        yy = y + h * (0.20 + j * 0.11)
        draw.line([tx + w * 0.01, yy, tx + w * 0.09, yy],
                  fill=(160, 190, 230), width=2)
    # incoming missile + interception burst
    draw.line([x + w * 0.95, y + h * 0.05, x + w * 0.55, y + h * 0.35],
              fill=(255, 90, 20), width=4)
    burst(draw, x + w * 0.52, y + h * 0.38, 13, (255, 200, 60))
    draw.rectangle([x, y + h * 0.95, x + w, y + h], fill=(60, 38, 52))


def art_stocks(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                   outline=LIGHT_LINE, width=1)
    for j in range(1, 4):
        yy = y + h * j / 4
        draw.line([x + w * 0.06, yy, x + w * 0.94, yy], fill=(225, 225, 225),
                  width=1)
    pts = [(0.06, 0.25), (0.22, 0.35), (0.38, 0.30), (0.54, 0.55),
           (0.70, 0.62), (0.86, 0.85)]
    xy = [(x + w * px, y + h * py) for px, py in pts]
    draw.line(xy, fill=RED, width=5, joint="curve")
    ex, ey = xy[-1]
    draw.polygon([(ex, ey + 12), (ex - 12, ey - 4), (ex + 2, ey - 10)],
                 fill=RED)
    draw.text((x + w * 0.08, y + h * 0.06), "-4.8%", font=font(SANS_B, 20),
              fill=RED)


def art_protest(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 228, 205))
    # placards behind the crowd
    for px, pc in [(0.10, (185, 28, 28)), (0.38, (31, 58, 95)),
                   (0.66, (40, 120, 60))]:
        draw.line([x + w * px, y + h * 0.30, x + w * px, y + h * 0.62],
                  fill=(90, 80, 70), width=3)
        draw.rectangle([x + w * (px - 0.09), y + h * 0.12,
                        x + w * (px + 0.09), y + h * 0.30], fill=pc)
    # crowd of heads and shoulders
    colours = [(185, 28, 28), (31, 58, 95), (40, 120, 60), (200, 130, 30),
               (120, 60, 140), (30, 110, 110)]
    for i in range(7):
        cx = x + w * (0.06 + i * 0.14)
        cy = y + h * 0.72
        draw.ellipse([cx - 11, cy - 11, cx + 11, cy + 11],
                     fill=(232, 190, 150), outline=(90, 70, 50), width=1)
        draw.rectangle([cx - 16, cy + 10, cx + 16, y + h],
                       fill=colours[i % len(colours)])


def art_mercury(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(10, 10, 26))
    for sx, sy, sr in [(0.10, 0.15, 2), (0.25, 0.30, 1), (0.85, 0.12, 2),
                       (0.92, 0.35, 1), (0.60, 0.10, 1)]:
        draw.ellipse([x + w * sx - sr, y + h * sy - sr,
                      x + w * sx + sr, y + h * sy + sr], fill=(255, 255, 255))
    # Mercury with craters
    cx, cy, r = x + w * 0.68, y + h * 0.55, h * 0.36
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 160, 148))
    for kx, ky, kr in [(0.55, 0.45, 0.10), (0.75, 0.62, 0.13),
                       (0.62, 0.70, 0.08), (0.80, 0.42, 0.07)]:
        draw.ellipse([x + w * kx - r * kr, y + h * ky - r * kr,
                      x + w * kx + r * kr, y + h * ky + r * kr],
                     fill=(140, 132, 120))
    # spacecraft with solar panels
    sx, sy = x + w * 0.22, y + h * 0.42
    draw.rectangle([sx - 26, sy - 6, sx + 26, sy + 6], fill=(40, 90, 180))
    draw.rectangle([sx - 8, sy - 12, sx + 8, sy + 12], fill=(220, 180, 60))
    draw.line([sx + 26, sy, sx + 44, sy - 10], fill=(200, 200, 200), width=2)
    # dashed trajectory to the planet
    for i in range(6):
        t = i / 6
        px = sx + (cx - sx) * t
        py = sy + (cy - sy) * t - 14 * math.sin(math.pi * t)
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 220, 120))


ART = {
    "kyiv": art_kyiv,
    "poland": art_poland,
    "ukeu": art_ukeu,
    "datacentre": art_datacentre,
    "riyadh": art_riyadh,
    "stocks": art_stocks,
    "protest": art_protest,
    "mercury": art_mercury,
}


# ------------------------------------------------------------- page build

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 62)
    d.text(((W - tf.getlength(title)) / 2, 26), title, font=tf, fill=INK)
    d.line([MARGIN, 104, W - MARGIN, 104], fill=INK, width=3)
    d.line([MARGIN, 110, W - MARGIN, 110], fill=INK, width=1)

    date = "FRIDAY  \u00b7  20 NOVEMBER 2026"
    df = font(SANS_B, 26)
    d.text(((W - df.getlength(date)) / 2, 122), date, font=df, fill=RED)

    kick = "EIGHT STORIES FROM THE WORLD'S NEWS WIRES  \u2014  ALL REPORTED ON 20 NOVEMBER 2026"
    kf = font(SANS, 13)
    d.text(((W - kf.getlength(kick)) / 2, 158), kick, font=kf, fill=GREY)

    # lead story
    lx, ly, lw, lh = MARGIN, 184, 460, 244
    art_kyiv(d, lx, ly, lw, lh)
    d.rectangle([lx, ly, lx + lw, ly + lh], outline=INK, width=2)

    tx = MARGIN + lw + 22
    tw = W - MARGIN - tx
    y = ly + 2
    y = draw_lines(d, [LEAD["kicker"]], font(SANS_B, 14), tx, y, RED, 20)
    y = fit_text(d, LEAD["headline"], font(SERIF_B, 30), tw, 3, tx, y + 4,
                 INK, 36, min_size=24)
    y = fit_text(d, LEAD["summary"], font(SANS, 16), tw, 5, tx, y + 8,
                 INK, 22, min_size=13)
    sf = font(SANS_B, 12)
    d.text((tx, ly + lh - 16), LEAD["source"], font=sf, fill=GREY)

    d.line([MARGIN, 444, W - MARGIN, 444], fill=INK, width=2)

    # grid rows: 4 stories, then 3 stories
    rows = [(STORIES[:4], 460, 264), (STORIES[4:], 740, 252)]
    for stories, ry, rh in rows:
        n = len(stories)
        gap = 16
        cw = (CONTENT_W - gap * (n - 1)) // n
        for i, s in enumerate(stories):
            cx = MARGIN + i * (cw + gap)
            ah = 96 if n == 4 else 108
            ART[s["art"]](d, cx, ry, cw, ah)
            d.rectangle([cx, ry, cx + cw, ry + ah], outline=INK, width=1)
            y = ry + ah + 8
            y = draw_lines(d, [s["kicker"]], font(SANS_B, 11), cx, y, RED, 15)
            y = fit_text(d, s["headline"], font(SERIF_B, 17 if n == 4 else 19),
                         cw, 2, cx, y + 2, INK, 21, min_size=14)
            y = fit_text(d, s["summary"], font(SANS, 13), cw, 4 if n == 4 else 3,
                         cx, y + 4, INK, 16, min_size=11)
            d.text((cx, ry + rh - 14), s["source"], font=font(SANS_B, 11),
                   fill=GREY)

    # footer
    foot = ("Sources: Reuters  \u00b7  AP  \u00b7  BBC  \u00b7  Sky News  \u00b7  CNBC  \u00b7  NPR"
            "     \u2014     The World Today, Friday 20 November 2026")
    ff = font(SANS, 12)
    d.text(((W - ff.getlength(foot)) / 2, 1002), foot, font=ff, fill=GREY)

    return img


def main():
    img = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print(f"wrote {out} {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
