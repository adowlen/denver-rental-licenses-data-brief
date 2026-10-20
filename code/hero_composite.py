"""Composite the headline figure onto the hero illustration.
Figure text is the verified share of active long-term rental licenses that are
their holder's only license (license basis), from stats.json - checked by
assertion before compositing.
"""
import json
from PIL import Image, ImageDraw, ImageFont

PKG = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/denver-rental-licenses-brief-2026-10-20"
SRC = f"{PKG}/hero_source/media-generation-hero-illustration-0-09931326-7d0b-42fd-a210-eb1aca116a47.webp"
S = json.load(open(f"{PKG}/stats.json"))
share = S["concentration_active_licenses"]["share_whose_holder_has_exactly_1_pct"]
only = S["concentration_active_licenses"]["units_whose_holder_has_exactly_1"]
total_named = S["concentration_active_licenses"]["units"]
holders = S["concentration_active_licenses"]["distinct_holders"]
total_active = S["register"]["distinct_license_nums_active"]
assert share == 68.57 and only == 18471 and total_named == 26939 and holders == 20780 and total_active == 26941, (share, only, total_named, holders, total_active)
# The printed composition is asserted in full (Section 11 fix loop, adversarial
# Finding 4): the share's denominator is the 26,939 NAMED active licenses, not
# the 26,941 total, and the holder count is a count of holder names as filed.
composition_line = f"{only:,} of {total_named:,} named active licenses, held by {holders:,} holder names"
assert composition_line == "18,471 of 26,939 named active licenses, held by 20,780 holder names", composition_line

img = Image.open(SRC).convert("RGB")
W, H = img.size
# dark gradient scrim across the top two-thirds for text legibility
# (the sublines cross the top of the left-hand building; the scrim must
# stay strong that far down or the lit windows wash the text out)
scrim = Image.new("L", (1, H))
for y in range(H):
    scrim.putpixel((0, y), int(242 * max(0.0, 1 - y / (H * 0.72))))
scrim = scrim.resize((W, H))
black = Image.new("RGB", (W, H), (5, 6, 7))
img = Image.composite(black, img, scrim.point(lambda v: int(v * 0.62)))

# translucent dark band behind the sublines, which cross the lit windows
# of the left-hand building; drawn before the text so the type stays clean
_band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
_bd = ImageDraw.Draw(_band)
scale0 = W / 3000.0
_y_sub = int(70 * scale0) + 20 + int(330 * scale0) + 60
_bd.rectangle([58, _y_sub - 14, W - 58, _y_sub + int(150 * scale0) + 96], fill=(4, 5, 6, 118))
img = Image.alpha_composite(img.convert("RGBA"), _band).convert("RGB")

d = ImageDraw.Draw(img)
FD = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/denver-crime-brief-2026-10-17/.venv/lib/python3.12/site-packages/matplotlib/mpl-data/fonts/ttf"
scale = W / 3000.0
f_kick = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", int(52 * scale) + 20)
f_big = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", int(200 * scale) + 40)
f_sub = ImageFont.truetype(f"{FD}/DejaVuSans.ttf", int(54 * scale) + 16)
AMBER, FG, MUT = (245, 168, 0), (232, 230, 225), (200, 205, 210)

x = int(110 * scale) + 30
y = int(70 * scale) + 20
d.text((x, y), "DENVER LONG-TERM RENTAL LICENSES, 2026", font=f_kick, fill=AMBER)
d.text((x, y + int(90 * scale) + 26), "68.6%", font=f_big, fill=FG)
d.text((x, y + int(330 * scale) + 60), "of active long-term rental licenses are their holder's only license:", font=f_sub, fill=MUT)
d.text((x, y + int(400 * scale) + 76), composition_line, font=f_sub, fill=MUT)
img.save(f"{PKG}/hero.png")
print("hero.png written", img.size)
