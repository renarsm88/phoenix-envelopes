#!/usr/bin/env python3
"""Draw the app icon: a Sonoran sunset, to match the contour map on the page."""
from PIL import Image, ImageDraw
from pathlib import Path

S = 2048                      # draw big, shrink down, so the edges stay smooth
HERE = Path(__file__).resolve().parent

def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

img = Image.new("RGB", (S, S))
d = ImageDraw.Draw(img)

# --- sky: dusk purple at the top, warm sand at the horizon -------------------
TOP, MID, HOR = (0x5B, 0x41, 0x76), (0xC9, 0x6F, 0x5A), (0xF2, 0xBE, 0x88)
horizon = int(S * 0.70)
for y in range(horizon):
    t = y / horizon
    d.line([(0, y), (S, y)], fill=lerp(TOP, MID, t * t) if t < .55
           else lerp(MID, HOR, (t - .55) / .45))

# --- the sun, low and fat ---------------------------------------------------
sr, sx, sy = int(S * .155), int(S * .63), int(S * .565)
for i in range(28, 0, -1):                       # soft halo
    r = sr + i * int(S * .009)
    d.ellipse([sx - r, sy - r, sx + r, sy + r],
              fill=lerp((0xE8, 0x9A, 0x66), (0xF7, 0xD9, 0xA0), 1 - i / 28))
d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(0xFF, 0xEE, 0xC9))

# --- two ridgelines, the far one hazier -------------------------------------
def ridge(pts, col):
    d.polygon([(0, S)] + pts + [(S, S)], fill=col)

ridge([(0, int(S*.615)), (int(S*.17), int(S*.545)), (int(S*.31), int(S*.60)),
       (int(S*.47), int(S*.515)), (int(S*.66), int(S*.605)), (int(S*.84), int(S*.545)),
       (S, int(S*.60))], (0x9B, 0x6A, 0x6B))
ridge([(0, int(S*.70)), (int(S*.22), int(S*.655)), (int(S*.42), int(S*.715)),
       (int(S*.60), int(S*.655)), (int(S*.80), int(S*.72)), (S, int(S*.675))],
      (0x6B, 0x45, 0x50))

# --- desert floor -----------------------------------------------------------
d.rectangle([0, int(S*.745), S, S], fill=(0x46, 0x2C, 0x38))

# --- the saguaro, dead centre-left, big enough to read at 32px ---------------
CAC = (0x24, 0x16, 0x22)
def limb(x0, y0, x1, y1, w):
    d.rounded_rectangle([x0 - w//2, y0, x1 + w//2, y1], radius=w//2, fill=CAC)

tw = int(S * .105)
tx = int(S * .335)
limb(tx, int(S*.375), tx, int(S*.86), tw)                       # trunk
aw = int(S * .075)
# left arm: up the side, then a bend upward
d.rounded_rectangle([tx - int(S*.185), int(S*.545), tx, int(S*.545) + aw],
                    radius=aw//2, fill=CAC)
limb(tx - int(S*.185) + aw//2, int(S*.455), tx - int(S*.185) + aw//2, int(S*.60), aw)
# right arm, a little higher
d.rounded_rectangle([tx, int(S*.475), tx + int(S*.165), int(S*.475) + aw],
                    radius=aw//2, fill=CAC)
limb(tx + int(S*.165) - aw//2, int(S*.375), tx + int(S*.165) - aw//2, int(S*.53), aw)

# a small second cactus for depth
limb(int(S*.78), int(S*.665), int(S*.78), int(S*.80), int(S*.055))

for size, name in [(512, "icon-512.png"), (192, "icon-192.png"),
                   (180, "apple-touch-icon.png"), (32, "favicon.png")]:
    img.resize((size, size), Image.LANCZOS).save(HERE / name)
    print("wrote", name)
