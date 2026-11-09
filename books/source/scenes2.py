"""Scenes for Story 2 (Little Ninja and the Dark Night) and Story 3 (The Ninja Team).
Each scene is drawn inside a 600 x 600 box, like scenes.py."""
from art import *  # noqa: F401,F403
from scenes import NIGHT, DAY, DUSK, night_stars

WALL_DUSK = "#c9d3f0"
WALL_DARK = "#4a5585"
FLOOR = "#b98a5a"


def room(a, wall, rug=True):
    if a.color:
        a.c.setFillColor(HexColor(wall))
        a.c.rect(0, 0, 600, 600, stroke=0, fill=1)
    a.rect(-10, -10, 620, 110, FLOOR)
    for xx in (120, 260, 400, 540):
        a.line([(xx, -10), (xx - 30, 100)], w=2)
    if rug:
        a.ellipse(420, 40, 120, 28, "#f58fb0")


def note(a, x, y, s=1.0):
    with a.at(x, y, s):
        a.ellipse(0, 0, 9, 7, "#ffffff")
        a.line([(8, 2), (8, 36), (20, 30)], w=3)


def word(a, x, y, txt, size, rot=0, fill="#ffffff"):
    with a.at(x, y, 1, rot=rot):
        a.text(0, 0, txt, size, fill=fill)


# =====================================================================
# Story 2: Little Ninja and the Dark Night
# =====================================================================
def d_cover(a):
    sky(a, *NIGHT)
    moon(a, 470, 330, 60)
    night_stars(a, [(40, 560, 12), (560, 560, 12), (60, 380, 9), (550, 440, 8)])
    hill(a, 150, "#3f7a5c", amp=18)
    with a.at(110, 120, 1.4):
        tree(a, 0, 0, 1.0)
    owl(a, 470, 120, 0.85, stick=False)
    ninja(a, 290, 80, 1.35, pose="hold")
    lantern(a, 290, 166, 0.9, "#ffa94d")
    for x, y in [(160, 250), (410, 280), (220, 330), (520, 230), (90, 300), (370, 380)]:
        firefly(a, x, y, 0.8)


def d_bedtime(a):
    room(a, WALL_DUSK)
    window(a, 380, 250, 160, 170)
    bed(a, 200, 60, 1.25, who=(KAI_GI, KAI_BAND))
    cat(a, 470, 30, 0.75, sleeping=True)


def d_dark(a):
    room(a, WALL_DARK)
    window(a, 380, 250, 160, 170)
    bed(a, 200, 60, 1.25, who=(KAI_GI, KAI_BAND), peeking=True, face="o")
    word(a, 470, 210, "Creak!", 40, rot=-8)
    word(a, 170, 360, "Whoosh!", 44, rot=8)


def d_shadow(a):
    room(a, WALL_DARK, rug=False)
    # the big shadow on the wall
    sh = "#2b2547"
    a.poly([(300, 370), (290, 520), (350, 430)], sh)
    a.poly([(460, 370), (470, 520), (410, 430)], sh)
    a.ellipse(380, 330, 120, 140, sh)
    a.limb([(480, 250), (560, 300), (570, 400)], 34, sh)
    lamp(a, 300, 60, 1.0)
    cat(a, 380, 60, 0.7)
    bed(a, 160, 60, 0.95, who=(KAI_GI, KAI_BAND), peeking=True, face="o")


def d_only_pip(a):
    room(a, WALL_DUSK)
    lamp(a, 520, 90, 1.0)
    ninja(a, 220, 70, 1.5, pose="cheer", face="laugh")
    cat(a, 410, 50, 1.1, flip=True)
    word(a, 430, 230, "Meow!", 36, fill="#e8423a")


def d_owl_window(a):
    room(a, WALL_DARK)
    window(a, 170, 240, 260, 280, moon_in=False)
    if a.color:
        star(a, 220, 480, 10)
        star(a, 390, 470, 8)
    owl(a, 300, 240, 1.15, stick=False)
    ninja(a, 110, 60, 1.05, pose="wave", face="o")
    word(a, 500, 330, "Tap, tap!", 32, rot=-6)


def d_moon(a):
    sky(a, *NIGHT)
    moon(a, 300, 420, 120)
    night_stars(a, [(60, 540, 12), (540, 540, 12), (80, 330, 9), (520, 300, 9)])
    hill(a, 140, "#3f7a5c", amp=14)
    ninja(a, 200, 90, 1.2, pose="point")
    owl(a, 420, 90, 1.0)


def d_frogs(a):
    sky(a, *NIGHT)
    moon(a, 500, 500, 44)
    night_stars(a, [(70, 540, 10), (200, 500, 8), (330, 560, 10)])
    hill(a, 230, "#3f7a5c", amp=10)
    pond(a, 330, 120, 260, 80)
    lily_pad(a, 230, 120, 1.3)
    lily_pad(a, 430, 90, 1.3)
    frog(a, 230, 128, 1.0, singing=True)
    frog(a, 430, 98, 1.0, flip=True, singing=True)
    note(a, 270, 220)
    note(a, 470, 200, 1.2)
    note(a, 350, 250, 0.9)
    ninja(a, 90, 190, 0.95, pose="stand", face="o")
    owl(a, 540, 220, 0.6, stick=False)


def d_fireflies(a):
    sky(a, *NIGHT)
    night_stars(a, [(60, 540, 12), (540, 560, 12), (300, 560, 9)])
    hill(a, 140, "#3f7a5c", amp=12)
    for i in range(10):
        grass(a, 30 + i * 62, 100 + (i % 3) * 12, 1.2)
    ninja(a, 300, 80, 1.45, pose="cheer", face="laugh")
    for x, y in [(110, 260), (480, 260), (160, 400), (450, 410), (90, 470), (520, 480), (300, 500), (230, 180), (400, 170)]:
        firefly(a, x, y, 1.1)


def d_stars(a):
    sky(a, *NIGHT)
    pts = [(80, 520), (150, 470), (230, 500), (300, 450), (380, 520), (450, 480), (530, 540), (500, 380),
           (120, 360), (260, 380), (400, 400), (560, 300), (60, 280)]
    for i, (x, y) in enumerate(pts):
        star(a, x, y, 12 + (i % 3) * 5)
    hill(a, 140, "#3f7a5c", amp=8)
    ninja(a, 220, 100, 1.2, pose="point")
    owl(a, 430, 100, 0.9, stick=False)
    for i, (x, y) in enumerate([(120, 360), (260, 380), (400, 400)]):
        a.text(x, y + 22, str(i + 1), 20, fill="#ffffff")


def d_friends(a):
    sky(a, *NIGHT)
    moon(a, 480, 480, 54)
    night_stars(a, [(70, 540, 12), (200, 520, 9), (320, 570, 10)])
    hill(a, 140, "#3f7a5c", amp=10)
    pond(a, 500, 80, 110, 34)
    frog(a, 500, 80, 0.8, flip=True)
    owl(a, 380, 110, 0.95, stick=False)
    ninja(a, 190, 90, 1.25, pose="cheer")
    cat(a, 70, 70, 0.8)
    for x, y in [(110, 300), (300, 360), (520, 300), (440, 400), (60, 420)]:
        firefly(a, x, y, 0.9)


def d_sleep(a):
    room(a, "#7d88b8")
    window(a, 380, 250, 160, 170)
    bed(a, 200, 60, 1.25, who=(KAI_GI, KAI_BAND), eyes_closed=True)
    cat(a, 470, 30, 0.75, sleeping=True)
    zzz(a, 120, 300, 1.0)


# ---- Dark Night coloring-only pages ----
def d_big_frog(a):
    pond(a, 300, 90, 280, 70)
    lily_pad(a, 300, 80, 3.6)
    frog(a, 300, 110, 3.6, singing=True)
    note(a, 120, 440, 2.0)
    note(a, 470, 460, 1.6)


def d_big_fireflies(a):
    moon(a, 470, 470, 70)
    firefly(a, 170, 380, 5.0)
    firefly(a, 360, 220, 3.5)
    firefly(a, 120, 140, 2.5)
    for i in range(6):
        grass(a, 40 + i * 104, 0, 2.2)


def d_moon_face(a):
    a.circle(300, 320, 230, "#fbe9a6")
    a.dot(230, 350, 14)
    a.dot(370, 350, 14)
    a.arc(300, 310, 70, 210, 120)
    star(a, 70, 540, 30)
    star(a, 540, 70, 26)


def d_draw_window(a):
    room(a, WALL_DUSK, rug=False)
    window(a, 80, 160, 440, 380, moon_in=False)


# =====================================================================
# Story 3: The Ninja Team
# =====================================================================
def big_hill(a, peach_on_top=True, tree_on_top=True):
    a.poly([(-10, -10), (-10, 120), (120, 160, 220, 380, 420, 400), (520, 410, 600, 300, 610, 260), (610, -10)], "#8fce6a")
    if tree_on_top:
        tree(a, 480, 395, 0.8)
    if peach_on_top:
        peach(a, 400, 398, 0.75)


def t_cover(a):
    sky(a, *DAY)
    sun(a, 545, 330, 32)
    cloud(a, 70, 400, 0.6)
    hill(a, 130, "#8fce6a", amp=12)
    peach(a, 380, 110, 1.8)
    ninja(a, 160, 100, 1.15, pose="push", face="laugh", tilt=-12)
    ninja(a, 250, 100, 1.0, gi=MIKO_GI, band=MIKO_BAND, bun=True, pose="push", face="laugh", tilt=-12)
    cat(a, 560, 80, 0.7, flip=True)


def t_challenge(a):
    sky(a, *DAY)
    cloud(a, 120, 520, 0.9)
    cloud(a, 470, 540, 0.8)
    hill(a, 120, "#8fce6a", amp=10)
    owl(a, 300, 100, 1.2)
    scroll(a, 300, 160, 1.0)
    ninja(a, 110, 70, 1.05, pose="wave")
    ninja(a, 490, 70, 1.0, gi=MIKO_GI, band=MIKO_BAND, bun=True, pose="wave", flip=True)
    cat(a, 200, 50, 0.6)


def t_hill(a):
    sky(a, *DAY)
    sun(a, 90, 500, 40)
    cloud(a, 300, 540, 0.8)
    big_hill(a)
    ninja(a, 120, 110, 0.7, pose="point")
    ninja(a, 220, 120, 0.65, gi=MIKO_GI, band=MIKO_BAND, bun=True, pose="cheer")
    star(a, 400, 520, 18)
    star(a, 460, 480, 12)


def slope(a):
    a.poly([(-10, -10), (-10, 150), (610, 250), (610, -10)], "#8fce6a")


def t_kai_push(a):
    sky(a, *DAY)
    cloud(a, 120, 520, 0.8)
    slope(a)
    peach(a, 400, 210, 1.7)
    ninja(a, 190, 175, 1.15, pose="push", face="grumpy", tilt=-14)
    word(a, 300, 412, "Huff! Puff!", 34, fill="#e8423a")


def t_miko_pull(a):
    sky(a, *DAY)
    cloud(a, 480, 520, 0.8)
    slope(a)
    peach(a, 230, 180, 1.7)
    ninja(a, 450, 214, 1.1, gi=MIKO_GI, band=MIKO_BAND, bun=True, pose="push", face="grumpy", flip=True, tilt=14)
    word(a, 90, 396, "Ugh!", 40, fill="#e8423a")


def t_grumpy(a):
    sky(a, *DAY)
    slope(a)
    peach(a, 430, 220, 1.3)
    ninja(a, 160, 190, 1.1, pose="sit", face="grumpy", flip=True)
    ninja(a, 280, 210, 1.0, gi=MIKO_GI, band=MIKO_BAND, bun=True, pose="sit", face="grumpy")
    rain_cloud(a, 220, 500, 0.8)


def t_pip_idea(a):
    sky(a, *DAY)
    slope(a)
    peach(a, 360, 200, 1.6)
    cat(a, 230, 175, 0.9)
    a.limb([(250, 205), (262, 214)], 9, "#f29b38")
    ninja(a, 80, 140, 0.85, pose="stand", face="o")
    ninja(a, 540, 240, 0.8, gi=MIKO_GI, band=MIKO_BAND, bun=True, pose="stand", face="o", flip=True)
    star(a, 220, 360, 22)
    star(a, 260, 400, 12)


def t_team_push(a):
    sky(a, *DAY)
    sun(a, 520, 510, 40)
    slope(a)
    peach(a, 420, 220, 1.6)
    ninja(a, 160, 168, 1.05, pose="push", face="laugh", tilt=-14)
    ninja(a, 250, 182, 1.0, gi=MIKO_GI, band=MIKO_BAND, bun=True, pose="push", face="laugh", tilt=-14)
    cat(a, 70, 145, 0.6)
    word(a, 330, 412, "PUSH!", 44, fill="#e8423a")


def t_rolling(a):
    sky(a, *DAY)
    cloud(a, 480, 530, 0.8)
    a.poly([(-10, -10), (-10, 80), (610, 380), (610, -10)], "#8fce6a")
    peach(a, 200, 150, 1.0, rot=40)
    motion_lines(a, 290, 210, n=3, gap=26, length=60)
    ninja(a, 440, 300, 0.8, pose="run", flip=True)
    ninja(a, 540, 350, 0.75, gi=MIKO_GI, band=MIKO_BAND, bun=True, pose="cheer")
    word(a, 200, 420, "Roll, roll, roll!", 38, fill="#e8423a")


def t_picnic(a):
    sky(a, *DAY)
    sun(a, 90, 500, 40)
    hill(a, 200, "#8fce6a", amp=8)
    blanket(a, 120, 40, 380, 120)
    peach(a, 310, 80, 1.1)
    basket(a, 470, 140, 0.8)
    owl(a, 520, 110, 0.75, stick=False)
    ninja(a, 90, 140, 0.8, pose="cheer")
    word(a, 300, 400, "PLOP!", 56, fill="#e8423a")


def t_share(a):
    sky(a, *DUSK)
    hill(a, 220, "#8fce6a", amp=8)
    blanket(a, 60, 40, 480, 140)
    for i, (x, y) in enumerate([(160, 90), (240, 110), (330, 90), (420, 110)]):
        peach_slice(a, x - 10, y - 10, 1.8, rot=(i % 2) * 20)
    ninja(a, 120, 170, 0.9, pose="hold")
    ninja(a, 470, 170, 0.85, gi=MIKO_GI, band=MIKO_BAND, bun=True, pose="hold", flip=True)
    cat(a, 300, 180, 0.6)
    bird(a, 300, 340, 0.9, col="#f7c531")
    turtle(a, 560, 40, 0.7, flip=True)
    frog(a, 40, 20, 0.7)


def t_team(a):
    sky(a, *DUSK)
    heart(a, 300, 450, 1.4)
    hill(a, 120, "#8fce6a", amp=8)
    ninja(a, 160, 80, 1.15, pose="cheer", face="laugh")
    ninja(a, 440, 80, 1.1, gi=MIKO_GI, band=MIKO_BAND, bun=True, pose="cheer", face="laugh")
    owl(a, 300, 70, 0.85, stick=False)
    cat(a, 560, 60, 0.55, flip=True)


# ---- Ninja Team coloring-only pages ----
def t_big_peach(a):
    peach(a, 300, 110, 3.3)
    for i in range(5):
        grass(a, 60 + i * 120, 40, 2)


def t_high_five(a):
    hill(a, 100, "#8fce6a", amp=6)
    ninja(a, 190, 70, 1.5, pose="reach", face="laugh")
    ninja(a, 410, 70, 1.45, gi=MIKO_GI, band=MIKO_BAND, bun=True, pose="reach", face="laugh", flip=True)
    star(a, 300, 470, 30)


def t_picnic_basket(a):
    blanket(a, 60, 40, 480, 160)
    basket(a, 300, 140, 3.0)
    peach_slice(a, 120, 80, 1.6)
    peach_slice(a, 440, 80, 1.6, rot=15)
