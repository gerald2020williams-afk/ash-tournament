"""Picture scenes, each drawn inside a 600 x 600 box."""
from art import *  # noqa: F401,F403

NIGHT = ("#1d2a5c", "#4f5f9e")
DAY = ("#8fd3f5", "#e6f6fd")
DUSK = ("#f6a46b", "#fde3b5")
STORM = ("#6c7a96", "#b6c0d3")


def night_stars(a, pts):
    for x, y, r in pts:
        star(a, x, y, r)


# ---------------- story scenes ----------------
def cover(a):
    sky(a, *NIGHT)
    night_stars(a, [(40, 560, 12), (560, 560, 12), (40, 400, 9), (560, 470, 9), (150, 330, 8)])
    moon(a, 500, 380, 56)
    mountain(a, 120, 150, 320, 260, "#6b7bb3")
    mountain(a, 470, 150, 300, 220, "#7d8dc4")
    hill(a, 150, "#4f9a6a", amp=22)
    hill(a, 90, "#5fae6f", amp=14, phase=2)
    ninja(a, 300, 100, 1.55, pose="cheer")
    cat(a, 150, 70, 0.9)
    grass(a, 470, 70, 1.4)
    grass(a, 60, 40, 1.2)


def village(a):
    sky(a, *DAY)
    sun(a, 500, 500, 46)
    cloud(a, 140, 500, 1.0)
    cloud(a, 330, 540, 0.7)
    mountain(a, 300, 200, 420, 230, "#9aaedb")
    hill(a, 190, "#8fce6a", amp=16)
    house(a, 150, 150, 1.1)
    tree(a, 460, 140, 1.0, "blossom")
    hill(a, 110, "#6dbb5b", amp=10, phase=1)
    ninja(a, 330, 60, 1.1, pose="wave")
    flower(a, 520, 50, 0.8)
    flower(a, 60, 40, 0.8, "#f7c531")


def meet_sensei(a):
    sky(a, *DAY)
    cloud(a, 120, 520, 0.8)
    cloud(a, 470, 540, 0.9)
    bamboo(a, 40, 100, 420)
    bamboo(a, 560, 100, 380)
    bamboo(a, 520, 100, 260, 0.8)
    hill(a, 120, "#8fce6a", amp=8)
    rock(a, 400, 110, 170, 70)
    owl(a, 390, 176, 1.15)
    ninja(a, 180, 70, 1.3, pose="bow", face="happy")


def five_secrets(a):
    sky(a, *DUSK)
    for i, (x, y) in enumerate([(110, 500), (210, 545), (300, 560), (390, 545), (490, 500)]):
        star(a, x, y, 30, ["#ffd84a", "#7ed0f5", "#9ad46b", "#f58fb0", "#ffa94d"][i])
    hill(a, 130, "#8fce6a", amp=10)
    owl(a, 420, 110, 1.25)
    ninja(a, 180, 90, 1.25, pose="sit")
    flower(a, 40, 70, 0.7)
    flower(a, 560, 60, 0.7, "#f7c531")


def quiet(a):
    sky(a, *NIGHT)
    moon(a, 480, 480, 56)
    night_stars(a, [(80, 520, 12), (200, 560, 9), (330, 500, 10), (560, 380, 8)])
    hill(a, 130, "#4f8f6a", amp=8)
    cat(a, 440, 100, 1.1, sleeping=True)
    zzz(a, 470, 250, 1.0)
    ninja(a, 190, 100, 1.4, pose="tiptoe", face="o")
    grass(a, 40, 90, 1.2)
    grass(a, 300, 80, 1.0)


def patient(a):
    sky(a, *DAY)
    sun(a, 90, 500, 40)
    cloud(a, 420, 520, 0.9)
    hill(a, 140, "#8fce6a", amp=12)
    tree(a, 470, 150, 1.0)
    ninja(a, 200, 130, 1.3, pose="sit", eyes_closed=True)
    turtle(a, 420, 70, 1.1, flip=True)
    flower(a, 70, 80, 0.9)
    flower(a, 330, 60, 0.7, "#f7c531")
    butterfly(a, 330, 360, 1.1)


def strong(a):
    sky(a, *DAY)
    sun(a, 500, 500, 42)
    mountain(a, 160, 160, 360, 220, "#9aaedb")
    hill(a, 140, "#8fce6a", amp=10)
    rock(a, 180, 120, 150, 60)
    ninja(a, 180, 176, 1.15, pose="crane")
    ninja(a, 400, 80, 1.15, gi=MIKO_GI, band=MIKO_BAND, pose="kick", bun=True, face="brave")


def kind(a):
    sky(a, *DAY)
    cloud(a, 120, 520, 0.8)
    hill(a, 120, "#8fce6a", amp=10)
    with a.at(380, 90, 1.8):
        tree(a, 0, 0, 1.0)
    cat(a, 360, 300, 0.8, flip=True)
    ninja(a, 240, 70, 1.25, pose="reach")
    flower(a, 70, 70, 0.8)


def brave(a):
    sky(a, *DAY)
    cloud(a, 480, 520, 0.9)
    mountain(a, 90, 200, 260, 250, "#8a9cc7")
    mountain(a, 520, 200, 260, 220, "#9aaedb")
    hill(a, 200, "#6dbb5b", amp=0)
    river(a, -10, 150)
    a.poly([(-10, 200), (-10, 140), (90, 140), (110, 200)], "#8fce6a")
    a.poly([(610, 200), (610, 140), (510, 140), (490, 200)], "#8fce6a")
    bridge(a, 100, 500, 280, sag=60)
    ninja(a, 300, 223, 0.9, pose="cheer", face="brave")


def storm(a):
    sky(a, *STORM)
    rain_cloud(a, 140, 520, 1.3)
    rain_cloud(a, 430, 540, 1.1)
    for i in range(16):
        x = 40 + (i * 37) % 560
        y = 160 + (i * 71) % 280
        a.line([(x, y), (x - 8, y - 22)], w=2.5)
    hill(a, 120, "#6f9f62", amp=10)
    with a.at(140, 90, 1.5):
        tree(a, 0, 0, 1.0)
    bird(a, 120, 300, 0.9, col="#f7c531")
    ninja(a, 380, 70, 1.3, pose="hold", face="o")
    lantern(a, 380, 160, 0.9)


def home_nest(a):
    sky(a, *DUSK)
    sun(a, 90, 470, 38, smile=True)
    hill(a, 110, "#8fce6a", amp=10)
    with a.at(400, 80, 1.7):
        tree(a, 0, 0, 1.0)
    nest(a, 380, 320, 1.0)
    bird(a, 360, 345, 0.7, col="#f7c531")
    bird(a, 405, 345, 0.7, col="#f7c531", flip=True)
    bird(a, 450, 420, 1.0, col="#5ab3e8", flip=True)
    ninja(a, 170, 60, 1.25, pose="cheer")
    ninja(a, 300, 60, 0.95, gi=MIKO_GI, band=MIKO_BAND, pose="wave", bun=True)


def big_heart(a):
    sky(a, *DUSK)
    heart(a, 300, 420, 1.9)
    star(a, 120, 500, 20)
    star(a, 480, 510, 22)
    star(a, 520, 380, 14)
    hill(a, 120, "#8fce6a", amp=8)
    owl(a, 440, 90, 1.1)
    ninja(a, 190, 80, 1.3, pose="bow")


def goodnight(a):
    sky(a, *NIGHT)
    moon(a, 470, 490, 60)
    night_stars(a, [(70, 540, 12), (160, 470, 9), (280, 560, 12), (350, 470, 8), (560, 380, 10)])
    hill(a, 120, "#3f7a5c", amp=10)
    house(a, 220, 100, 1.4, lit=True)
    cat(a, 470, 80, 1.0, sleeping=True)
    zzz(a, 500, 220, 0.9)


# ---------------- coloring-only scenes ----------------
def solo_kai(a):
    ninja(a, 300, 60, 2.4, pose="wave")
    grass(a, 90, 40, 2)
    grass(a, 510, 40, 2)


def solo_miko(a):
    ninja(a, 300, 60, 2.3, gi=MIKO_GI, band=MIKO_BAND, pose="cheer", bun=True)
    star(a, 90, 480, 34)
    star(a, 510, 500, 28)


def solo_owl(a):
    owl(a, 270, 70, 2.6)


def solo_cat(a):
    cat(a, 300, 70, 3.6)
    flower(a, 80, 40, 1.4)


def kai_and_pip(a):
    hill(a, 120, "#8fce6a", amp=10)
    sun(a, 480, 480, 50)
    ninja(a, 230, 80, 1.8, pose="stand")
    cat(a, 430, 80, 1.4, flip=True)


def dojo(a):
    hill(a, 100, "#8fce6a", amp=0)
    house(a, 300, 100, 2.6)
    cloud(a, 120, 530, 0.8)


def blossom(a):
    hill(a, 100, "#8fce6a", amp=10)
    with a.at(300, 90, 2.0):
        tree(a, 0, 0, 1.0, "blossom")
    ninja(a, 140, 60, 1.1, gi=MIKO_GI, band=MIKO_BAND, pose="wave", bun=True)
    butterfly(a, 500, 200, 1.2)


def night_mountains(a):
    cover(a)


def friends(a):
    hill(a, 110, "#8fce6a", amp=8)
    owl(a, 300, 90, 1.2, stick=False)
    ninja(a, 130, 70, 1.15, pose="wave")
    ninja(a, 470, 70, 1.15, gi=MIKO_GI, band=MIKO_BAND, pose="wave", bun=True, flip=True)
    cat(a, 300, 20, 0.6)
    star(a, 300, 480, 34)


def big_bird(a):
    with a.at(300, 290, 1.0):
        a.limb([(-260, -90), (260, -110)], 22, "#9a6a3e")
    bird(a, 300, 320, 6.0, col="#f7c531")


def draw_your_face(a):
    ninja(a, 300, 40, 2.6, pose="stand", blank_face=True)


def crane_solo(a):
    sun(a, 480, 490, 50)
    hill(a, 120, "#8fce6a", amp=10)
    rock(a, 300, 100, 220, 70)
    ninja(a, 290, 168, 1.75, pose="crane")


def kick_practice(a):
    hill(a, 110, "#8fce6a", amp=6)
    # practice pad on a post
    a.rect(460, 100, 20, 220, "#9a6a3e")
    a.ellipse(470, 330, 50, 60, "#e8423a")
    a.circle(470, 330, 30, "#ffffff")
    a.circle(470, 330, 12, "#e8423a")
    ninja(a, 230, 80, 1.6, gi=MIKO_GI, band=MIKO_BAND, pose="kick", bun=True, face="brave")


def run_with_pip(a):
    sky(a, *DAY)
    cloud(a, 140, 500, 1.0)
    cloud(a, 450, 530, 0.8)
    hill(a, 120, "#8fce6a", amp=12)
    ninja(a, 240, 90, 1.6, pose="run")
    with a.at(450, 80, 1.0):
        cat(a, 0, 0, 1.0, flip=True)
    for y in (200, 240, 280):
        a.line([(60, y), (120, y)], w=3)


def stretch(a):
    sun(a, 480, 480, 56)
    hill(a, 120, "#8fce6a", amp=10)
    ninja(a, 300, 90, 1.6, pose="cheer")
    flower(a, 90, 80, 1.1)
    flower(a, 510, 80, 1.1)


def breathing(a):
    hill(a, 120, "#8fce6a", amp=10)
    owl(a, 430, 110, 1.3, stick=False, eyes_closed=True)
    ninja(a, 180, 120, 1.35, pose="sit", eyes_closed=True)
    cloud(a, 300, 500, 1.1)


def star_badge(a):
    star(a, 300, 300, 270, "#ffd84a")
    a.circle(300, 300, 120, "#ffffff")
    ninja(a, 300, 200, 0.9, pose="cheer")


def kite_day(a):
    sky(a, *DAY)
    hill(a, 120, "#8fce6a", amp=12)
    cloud(a, 120, 520, 0.8)
    kite(a, 420, 450, 1.1, string_to=(240, 205))
    ninja(a, 200, 80, 1.2, pose="reach")
    ninja(a, 400, 80, 1.05, gi=MIKO_GI, band=MIKO_BAND, pose="cheer", bun=True)


def lantern_night(a):
    sky(a, *NIGHT)
    moon(a, 110, 490, 50)
    for x, y, s in [(260, 470, 0.9), (380, 520, 0.8), (500, 440, 1.0), (440, 330, 0.7)]:
        lantern(a, x, y, s, "#ffa94d")
    hill(a, 110, "#3f7a5c", amp=10)
    ninja(a, 200, 70, 1.35, pose="hold")
    lantern(a, 200, 160, 0.9)
    ninja(a, 400, 70, 1.1, gi=MIKO_GI, band=MIKO_BAND, pose="reach", bun=True)


def friends_bridge(a):
    sky(a, *DAY)
    mountain(a, 300, 230, 420, 260, "#9aaedb")
    hill(a, 200, "#6dbb5b", amp=0)
    river(a, -10, 150)
    a.poly([(-10, 200), (-10, 140), (90, 140), (110, 200)], "#8fce6a")
    a.poly([(610, 200), (610, 140), (510, 140), (490, 200)], "#8fce6a")
    bridge(a, 100, 500, 280, sag=60)
    ninja(a, 240, 228, 0.8, pose="wave")
    ninja(a, 360, 228, 0.8, gi=MIKO_GI, band=MIKO_BAND, pose="wave", bun=True, flip=True)


def empty(a):
    pass
