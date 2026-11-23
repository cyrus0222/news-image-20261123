#!/usr/bin/env python3
"""Draw the news-image entry for 23 November 2026.

A one-page newspaper front page, drawn programmatically so every word is
crisp (no AI-generated garbled text). Renders at 2x then downscales to
1024x1024 for smooth edges. Deterministic: same input, same bytes.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
S = 2  # supersample factor

PAPER = (250, 246, 238)
INK = (20, 24, 31)
MUTED = (74, 74, 68)
RULE = (20, 24, 31)
PANEL = (255, 255, 255)
BORDER = (216, 210, 196)
RED = (179, 38, 30)
BLUE = (29, 78, 158)
GREEN = (27, 107, 58)
DARKRED = (142, 31, 31)
NAVY = (20, 70, 124)
PURPLE = (75, 58, 122)
SKY = (214, 232, 244)
SEA = (168, 205, 230)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS_BLK = "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf"


def font(path, size):
    return ImageFont.truetype(path, int(size * S))


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w pixels."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    """x, y, leading in 1024-space; returns the next y in 1024-space."""
    for i, line in enumerate(lines):
        draw.text((x * S, (y + i * leading) * S), line, font=fnt, fill=fill)
    return y + len(lines) * leading


def panel_box(draw, x, y, w, h, accent):
    draw.rounded_rectangle([x * S, y * S, (x + w) * S, (y + h) * S],
                           radius=6 * S, fill=PANEL, outline=BORDER, width=1 * S)
    draw.rectangle([x * S, y * S, (x + w) * S, (y + 5) * S], fill=accent)


def kicker(draw, x, y, text, color):
    f = font(SANS_B, 13)
    draw.text((x * S, y * S), text, font=f, fill=color)
    return y + 20


def headline(draw, x, y, w, text, size=27):
    f = font(SERIF, size)
    lines = wrap(draw, text, f, w * S)
    return draw_lines(draw, lines, x, y, f, INK, int(size * 1.18)), len(lines)


def deck(draw, x, y, w, text, size=16.5):
    f = font(SANS, size)
    lines = wrap(draw, text, f, w * S)
    return draw_lines(draw, lines, x, y, f, MUTED, int(size * 1.32))


# ---- illustrations (flat editorial pictograms, drawn in 1024-space) ----

def art_cop31(draw, x, y, w, h):
    """Globe with rising thermometer and factory smoke."""
    cx, cy, r = x + w * 0.30, y + h * 0.52, min(w, h) * 0.36
    # sun rays
    for i in range(8):
        ang = i * 0.785
        x0 = cx + (r + 8) * __import__('math').cos(ang)
        y0 = cy + (r + 8) * __import__('math').sin(ang)
        x1 = cx + (r + 20) * __import__('math').cos(ang)
        y1 = cy + (r + 20) * __import__('math').sin(ang)
        draw.line([(x0 * S, y0 * S), (x1 * S, y1 * S)], fill=(232, 180, 60), width=4 * S)
    draw.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S],
                 fill=(96, 165, 210), outline=INK, width=2 * S)
    # continents
    for ex, ey, erx, ery in [(cx - r * 0.35, cy - r * 0.3, r * 0.42, r * 0.3),
                             (cx + r * 0.35, cy + r * 0.25, r * 0.38, r * 0.28),
                             (cx + r * 0.1, cy - r * 0.55, r * 0.3, r * 0.2)]:
        draw.ellipse([(ex - erx) * S, (ey - ery) * S, (ex + erx) * S, (ey + ery) * S],
                     fill=(96, 170, 90))
    # jagged crack down the globe's right side
    draw.line([((cx + r * 0.15) * S, (cy - r * 0.75) * S),
               ((cx + r * 0.35) * S, (cy - r * 0.35) * S),
               ((cx + r * 0.12) * S, (cy - r * 0.05) * S),
               ((cx + r * 0.38) * S, (cy + r * 0.35) * S),
               ((cx + r * 0.18) * S, (cy + r * 0.70) * S)],
              fill=INK, width=3 * S)
    # thermometer
    tx, ty = x + w * 0.68, y + h * 0.12
    tw, th = 26, h * 0.62
    draw.rounded_rectangle([tx * S, ty * S, (tx + tw) * S, (ty + th) * S],
                           radius=13 * S, fill=(255, 255, 255), outline=INK, width=2 * S)
    draw.rectangle([(tx + 6) * S, (ty + th * 0.25) * S, (tx + tw - 6) * S,
                    (ty + th - 6) * S], fill=RED)
    draw.ellipse([(tx - 8) * S, (ty + th - 14) * S, (tx + tw + 8) * S, (ty + th + 18) * S],
                 fill=RED, outline=INK, width=2 * S)
    # factory with smoke
    fx, fy = x + w * 0.78, y + h * 0.62
    draw.rectangle([fx * S, (fy + 18) * S, (fx + 64) * S, (fy + 52) * S], fill=(90, 90, 86))
    draw.rectangle([(fx + 8) * S, fy * S, (fx + 22) * S, (fy + 22) * S], fill=(90, 90, 86))
    for i, (sx, sy, sr) in enumerate([(fx + 15, fy - 12, 9), (fx + 24, fy - 26, 12), (fx + 38, fy - 38, 14)]):
        draw.ellipse([(sx - sr) * S, (sy - sr) * S, (sx + sr) * S, (sy + sr) * S],
                     fill=(170, 170, 164))


def art_capitol(draw, x, y, w, h):
    """Compact US Capitol dome (left) with 258 (right). Stays inside its box."""
    dw = w * 0.52
    cx = x + dw * 0.5
    base_y = y + h * 0.94
    draw.rectangle([(x + 6) * S, base_y * S, (x + dw - 6) * S, (base_y + 5) * S], fill=BLUE)
    draw.rectangle([(x + 14) * S, (base_y - 20) * S, (x + dw - 14) * S, base_y * S], fill=BLUE)
    for i in range(5):
        px = x + 24 + i * ((dw - 48) / 4)
        draw.rectangle([(px - 4) * S, (base_y - 17) * S, (px + 4) * S, (base_y - 3) * S],
                       fill=(255, 255, 255))
    draw.pieslice([(cx - 34) * S, (base_y - 56) * S, (cx + 34) * S, (base_y + 12) * S],
                  180, 360, fill=BLUE)
    draw.rectangle([(cx - 3) * S, (base_y - 64) * S, (cx + 3) * S, (base_y - 54) * S], fill=BLUE)
    draw.ellipse([(cx - 5) * S, (base_y - 70) * S, (cx + 5) * S, (base_y - 60) * S], fill=BLUE)
    f = font(SANS_BLK, 40)
    tx = x + dw + 8
    draw.text((tx * S, (y + h * 0.04) * S), "258", font=f, fill=RED)
    f2 = font(SANS_B, 12)
    draw.text((tx * S, (y + h * 0.68) * S), "SEATS", font=f2, fill=MUTED)


def art_dymer(draw, x, y, w, h):
    """Damaged apartment block with smoke. Stays inside its box."""
    bx, by, bw, bh = x + w * 0.16, y + h * 0.42, w * 0.68, h * 0.52
    draw.rectangle([bx * S, by * S, (bx + bw) * S, (by + bh) * S],
                   fill=(196, 190, 176), outline=INK, width=2 * S)
    # collapsed corner (scaled coords)
    draw.polygon([((bx + bw) * S, by * S), ((bx + bw) * S, (by + bh * 0.5) * S),
                  ((bx + bw * 0.70) * S, (by + bh * 0.20) * S)],
                 fill=PAPER, outline=INK)
    for r in range(2):
        for c in range(5):
            wx = bx + 10 + c * ((bw - 20) / 5)
            wy = by + 8 + r * ((bh - 16) / 2)
            draw.rectangle([wx * S, wy * S, (wx + 12) * S, (wy + 12) * S], fill=(60, 66, 74))
    # smoke plume, capped inside the box top
    for sx, sy, sr in [(bx + bw * 0.85, by - 8, 9), (bx + bw * 0.95, by - 20, 11),
                       (bx + bw * 0.82, by - 30, 12)]:
        draw.ellipse([(sx - sr) * S, (sy - sr) * S, (sx + sr) * S, (sy + sr) * S],
                     fill=(140, 140, 134))
    # small candle of mourning
    cx = x + w * 0.07
    draw.rectangle([(cx - 4) * S, (by + bh - 22) * S, (cx + 4) * S, (by + bh) * S], fill=(240, 230, 200))
    draw.ellipse([(cx - 5) * S, (by + bh - 34) * S, (cx + 5) * S, (by + bh - 22) * S],
                 fill=(240, 170, 40))


def art_ship(draw, x, y, w, h):
    """Warship on waves with a drone above and a blast. Stays inside its box."""
    wy = y + h * 0.66
    draw.rectangle([x * S, wy * S, (x + w) * S, (y + h) * S], fill=SEA)
    for i in range(4):
        wx = x + 8 + i * (w / 4)
        draw.arc([(wx - 22) * S, (wy + 4) * S, (wx + 22) * S, (wy + 18) * S],
                 180, 360, fill=(255, 255, 255), width=3 * S)
    hx, hy, hw = x + w * 0.20, wy - 22, w * 0.56
    draw.polygon([(hx * S, hy * S), ((hx + hw) * S, hy * S),
                  ((hx + hw - 12) * S, (hy + 20) * S), ((hx + 12) * S, (hy + 20) * S)],
                 fill=(70, 76, 84))
    draw.rectangle([(hx + hw * 0.35) * S, (hy - 16) * S, (hx + hw * 0.62) * S, hy * S],
                   fill=(70, 76, 84))
    draw.rectangle([(hx + hw * 0.46) * S, (hy - 28) * S, (hx + hw * 0.52) * S, (hy - 16) * S],
                   fill=(70, 76, 84))
    # drone
    dx, dy = x + w * 0.80, y + h * 0.18
    draw.ellipse([(dx - 9) * S, (dy - 5) * S, (dx + 9) * S, (dy + 5) * S], fill=INK)
    draw.line([(dx - 20) * S, (dy - 7) * S, (dx + 20) * S, (dy - 7) * S], fill=INK, width=3 * S)
    draw.ellipse([(dx - 24) * S, (dy - 11) * S, (dx - 16) * S, (dy - 3) * S], fill=(150, 150, 150))
    draw.ellipse([(dx + 16) * S, (dy - 11) * S, (dx + 24) * S, (dy - 3) * S], fill=(150, 150, 150))
    # blast star at the bow
    import math
    bx, by = hx + 4, hy + 4
    for ang in range(0, 360, 45):
        x1 = bx + 16 * math.cos(math.radians(ang))
        y1 = by + 16 * math.sin(math.radians(ang))
        draw.line([(bx * S, by * S), (x1 * S, y1 * S)], fill=(240, 140, 30), width=4 * S)
    draw.ellipse([(bx - 7) * S, (by - 7) * S, (bx + 7) * S, (by + 7) * S], fill=(250, 200, 60))


def art_market(draw, x, y, w, h):
    """Falling chart with -5.06%."""
    cx, cy, cw, ch = x + 14, y + 12, w - 28, h * 0.52
    draw.rectangle([cx * S, cy * S, (cx + cw) * S, (cy + ch) * S],
                   fill=(255, 255, 255), outline=BORDER, width=1 * S)
    pts = [(cx + cw * f, cy + ch * v) for f, v in
           [(0.0, 0.15), (0.2, 0.30), (0.35, 0.22), (0.55, 0.55), (0.7, 0.48), (1.0, 0.88)]]
    draw.line([(px * S, py * S) for px, py in pts], fill=RED, width=4 * S)
    for px, py in pts:
        draw.ellipse([(px - 4) * S, (py - 4) * S, (px + 4) * S, (py + 4) * S], fill=RED)
    f = font(SANS_BLK, 34)
    draw.text(((x + 14) * S, (cy + ch + 10) * S), "-5.06%", font=f, fill=RED)
    f2 = font(SANS_B, 13)
    draw.text(((x + 14) * S, (cy + ch + 52) * S), "NIKKEI 225  •  TOKYO", font=f2, fill=MUTED)


def art_mercury(draw, x, y, w, h):
    """Cratered Mercury with a probe."""
    cx, cy, r = x + w * 0.30, y + h * 0.52, min(w, h) * 0.34
    draw.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S],
                 fill=(178, 168, 152), outline=INK, width=2 * S)
    for ex, ey, er in [(cx - r * 0.4, cy - r * 0.3, r * 0.22), (cx + r * 0.3, cy + r * 0.2, r * 0.28),
                       (cx + r * 0.1, cy - r * 0.5, r * 0.16), (cx - r * 0.15, cy + r * 0.45, r * 0.18)]:
        draw.ellipse([(ex - er) * S, (ey - er) * S, (ex + er) * S, (ey + er) * S],
                     fill=(150, 140, 126))
    # probe with solar wings
    px, py = x + w * 0.68, y + h * 0.30
    draw.rectangle([(px - 26) * S, (py - 4) * S, (px - 8) * S, (py + 4) * S], fill=(40, 90, 180))
    draw.rectangle([(px + 8) * S, (py - 4) * S, (px + 26) * S, (py + 4) * S], fill=(40, 90, 180))
    draw.rectangle([(px - 8) * S, (py - 10) * S, (px + 8) * S, (py + 10) * S],
                   fill=(200, 200, 200), outline=INK, width=1 * S)
    draw.ellipse([(px - 3) * S, (py - 20) * S, (px + 3) * S, (py - 14) * S], fill=INK)
    for sx, sy in [(x + w * 0.55, y + h * 0.12), (x + w * 0.88, y + h * 0.55),
                   (x + w * 0.92, y + h * 0.18), (x + w * 0.48, y + h * 0.85)]:
        draw.ellipse([(sx - 2) * S, (sy - 2) * S, (sx + 2) * S, (sy + 2) * S], fill=(100, 100, 100))
    f = font(SANS_B, 13)
    draw.text(((x + w * 0.52) * S, (y + h * 0.72) * S), "8 YEARS IN FLIGHT", font=f, fill=MUTED)


# ---- composition ----

def main():
    img = Image.new("RGB", (W * S, H * S), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # side margin

    # Masthead
    d.rectangle([0, 0, W * S, 8 * S], fill=INK)
    f_title = font(SERIF, 54)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W * S - tw) / 2, 18 * S), title, font=f_title, fill=INK)
    d.line([(M * S, 92 * S), ((W - M) * S, 92 * S)], fill=INK, width=2 * S)
    f_date = font(SANS_BLK, 24)
    date = "MONDAY, 23 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W * S - dw) / 2, 100 * S), date, font=f_date, fill=RED)
    f_sub = font(SERIF_I, 17)
    sub = "One day in the world's news  •  Six stories from around the world"
    sw = d.textlength(sub, font=f_sub)
    d.text(((W * S - sw) / 2, 132 * S), sub, font=f_sub, fill=MUTED)
    d.line([(M * S, 160 * S), ((W - M) * S, 160 * S)], fill=INK, width=3 * S)

    # Hero: COP31
    hx, hy, hw, hh = M, 172, W - 2 * M, 252
    panel_box(d, hx, hy, hw, hh, GREEN)
    art_cop31(d, hx + 16, hy + 14, 300, hh - 28)
    tx = hx + 332
    y = kicker(d, tx, hy + 18, "CLIMATE  •  ANTALYA, TÜRKIYE", GREEN)
    y, _ = headline(d, tx, y + 2, hw - 348, "COP31 ends with no deal", size=40)
    y = deck(d, tx, y + 8, hw - 348,
             "Two weeks of UN climate talks collapse after the EU and about 130 "
             "countries reject a draft with no fossil-fuel phase-out.", size=18)
    d.text((tx * S, (hy + hh - 30) * S), "The longest climate summit on record ends empty-handed.",
           font=font(SERIF_I, 16), fill=MUTED)

    # Middle row: three panels
    my, mh = 438, 236
    mw = (W - 2 * M - 24) // 3
    panels = [
        (hx, BLUE, "U.S. POLITICS  •  WASHINGTON", "Democrats win biggest House majority since 1992",
         "At least 258 seats after a North Carolina recount — the party's largest House majority in 34 years.", art_capitol),
        (hx + mw + 12, DARKRED, "WAR IN UKRAINE  •  KYIV REGION", "Russian strikes kill at least 15 in Kyiv region",
         "A block of flats is hit in Dymer, north of Kyiv. The region marks 23 November a day of mourning.", art_dymer),
        (hx + 2 * (mw + 12), NAVY, "WAR AT SEA  •  OFF LIBYA", "Sea drones hit Russian warship off Libya",
         "The corvette Merkury is struck at Benghazi naval base in a Ukrainian naval drone attack, Kyiv says.", art_ship),
    ]
    for px, color, kick, head, dk, art in panels:
        panel_box(d, px, my, mw, mh, color)
        y = kicker(d, px + 14, my + 12, kick, color)
        y, _ = headline(d, px + 14, y + 1, mw - 28, head, size=21)
        art(d, px + 14, y + 4, mw - 28, 78)
        deck(d, px + 14, my + mh - 62, mw - 28, dk, size=14.5)

    # Bottom row: two panels
    by, bh = 688, 178
    bw = (W - 2 * M - 12) // 2
    panel_box(d, hx, by, bw, bh, RED)
    y = kicker(d, hx + 14, by + 12, "MARKETS  •  TOKYO", RED)
    y, _ = headline(d, hx + 14, y + 1, bw - 28, "Nikkei falls 5.06% as AI sell-off spreads", size=21)
    art_market(d, hx + 14, y + 2, 190, 96)
    deck(d, hx + 214, y + 10, bw - 228,
         "Tokyo leads a slide across Asia as investors dump AI stocks.", size=14.5)

    bx2 = hx + bw + 12
    panel_box(d, bx2, by, bw, bh, PURPLE)
    y = kicker(d, bx2 + 14, by + 12, "SPACE  •  MERCURY ORBIT", PURPLE)
    y, _ = headline(d, bx2 + 14, y + 1, bw - 28, "BepiColombo reaches Mercury", size=21)
    art_mercury(d, bx2 + 14, y + 2, 190, 96)
    deck(d, bx2 + 214, y + 10, bw - 228,
         "The European-Japanese probe enters orbit after an eight-year voyage.", size=14.5)

    # Ticker
    ty = 882
    d.rectangle([M * S, ty * S, (W - M) * S, (ty + 56) * S], fill=INK)
    f_tick = font(SANS_B, 15)
    tick = ("ALSO TODAY   •   NATO to meet on Russian missiles over Poland   •   "
            "Mexico captures cartel boss 'Chapo Isidro'; 11 killed   •   "
            "France arrests 144 in cost-of-living protests")
    lines = wrap(d, tick, f_tick, (W - 2 * M - 24) * S)
    for i, line in enumerate(lines):
        d.text(((M + 12) * S, (ty + 8 + i * 20) * S), line, font=f_tick, fill=(255, 255, 255))

    # Footer
    f_foot = font(SANS, 13)
    foot = "Sources: BBC, Reuters, The New York Times, The Guardian, Xinhua, SCMP  •  Stories as reported on 23 November 2026"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W * S - fw) / 2, 952 * S), foot, font=f_foot, fill=MUTED)
    d.rectangle([0, (H - 8) * S, W * S, H * S], fill=INK)

    img = img.resize((W, H), Image.LANCZOS)
    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
