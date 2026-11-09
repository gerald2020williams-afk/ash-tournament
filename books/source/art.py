"""Drawing kit for "The Way of the Ninja" books.

Every picture is drawn with an `Art` object.  In color mode shapes are filled
with color; in coloring mode the very same shapes are drawn as thick black
outlines on white, so the story book and the coloring books always match.
"""
from contextlib import contextmanager
import math

from reportlab.lib.colors import HexColor, white, black

INK_COLOR = "#2b2240"

# Character palette
KAI_GI, KAI_BAND = "#3a6fd6", "#e8423a"
MIKO_GI, MIKO_BAND = "#d94f86", "#f7c531"
SKIN = "#f6c9a0"
SHOE = "#3d3550"


class Art:
    def __init__(self, c, color=True):
        self.c = c
        self.color = color
        self.k = [1.0]
        self.ink = HexColor(INK_COLOR) if color else black
        self.base = 1.8 if color else 3.2

    # ---- transforms -------------------------------------------------
    @contextmanager
    def at(self, x, y, s=1.0, flip=False, rot=0):
        c = self.c
        c.saveState()
        c.translate(x, y)
        if rot:
            c.rotate(rot)
        c.scale(-s if flip else s, s)
        self.k.append(self.k[-1] * s)
        try:
            yield
        finally:
            self.k.pop()
            c.restoreState()

    @property
    def lw(self):
        return self.base / self.k[-1]

    def fillc(self, h):
        if h is None:
            return None
        return HexColor(h) if self.color else white

    def _style(self, f, lw=None):
        c = self.c
        c.setLineWidth(lw if lw is not None else self.lw)
        c.setStrokeColor(self.ink)
        c.setLineJoin(1)
        c.setLineCap(1)
        if f is not None:
            c.setFillColor(self.fillc(f))

    # ---- primitives -------------------------------------------------
    def circle(self, x, y, r, f):
        self._style(f)
        self.c.circle(x, y, r, stroke=1, fill=1 if f else 0)

    def ellipse(self, x, y, rx, ry, f):
        self._style(f)
        self.c.ellipse(x - rx, y - ry, x + rx, y + ry, stroke=1, fill=1 if f else 0)

    def rrect(self, x, y, w, h, r, f):
        self._style(f)
        self.c.roundRect(x, y, w, h, r, stroke=1, fill=1 if f else 0)

    def rect(self, x, y, w, h, f):
        self._style(f)
        self.c.rect(x, y, w, h, stroke=1, fill=1 if f else 0)

    def _path(self, segs, close):
        p = self.c.beginPath()
        p.moveTo(*segs[0])
        for s in segs[1:]:
            if len(s) == 2:
                p.lineTo(*s)
            else:
                p.curveTo(*s)
        if close:
            p.close()
        return p

    def poly(self, pts, f, close=True):
        self._style(f)
        self.c.drawPath(self._path(pts, close), stroke=1, fill=1 if (f and close) else 0)

    def line(self, pts, w=None):
        self._style(None, lw=(w / self.k[-1]) if w else self.lw)
        self.c.drawPath(self._path(pts, False), stroke=1, fill=0)

    def dot(self, x, y, r):
        self.c.setFillColor(self.ink)
        self.c.circle(x, y, r, stroke=0, fill=1)

    def arc(self, x, y, r, start, extent, w=None):
        self._style(None, lw=(w / self.k[-1]) if w else self.lw)
        p = self.c.beginPath()
        p.arc(x - r, y - r, x + r, y + r, start, extent)
        self.c.drawPath(p, stroke=1, fill=0)

    def limb(self, pts, w, f):
        """A thick rounded stroke with an outline (arms, legs, tails, ribbons)."""
        c = self.c
        p = self._path(pts, False)
        c.setLineJoin(1)
        c.setLineCap(1)
        c.setStrokeColor(self.ink)
        c.setLineWidth(w + 2 * self.lw)
        c.drawPath(p, stroke=1, fill=0)
        c.setStrokeColor(self.fillc(f))
        c.setLineWidth(w)
        c.drawPath(self._path(pts, False), stroke=1, fill=0)

    def blob(self, circles, f):
        """Union of circles with one outline (clouds, tree tops, bushes)."""
        c = self.c
        h = self.lw / 2
        c.setFillColor(self.ink)
        for x, y, r in circles:
            c.circle(x, y, r + h, stroke=0, fill=1)
        c.setFillColor(self.fillc(f))
        for x, y, r in circles:
            c.circle(x, y, r - h, stroke=0, fill=1)

    def only_color(self):
        return self.color

    def text(self, x, y, s, size, font="Kid", fill=None, center=True):
        c = self.c
        c.setFont(font, size)
        c.setFillColor(HexColor(fill) if (fill and self.color) else self.ink)
        if center:
            c.drawCentredString(x, y, s)
        else:
            c.drawString(x, y, s)


# =====================================================================
# Characters
# =====================================================================
POSES = {
    "stand": dict(
        arms=[[(-30, 96), (-44, 76), (-46, 58)], [(30, 96), (44, 76), (46, 58)]],
        legs=[[(-15, 52), (-18, 12)], [(15, 52), (18, 12)]],
        feet=[(-21, 7, 0), (21, 7, 0)],
    ),
    "wave": dict(
        arms=[[(-30, 96), (-44, 76), (-46, 58)], [(30, 96), (58, 116), (68, 150)]],
        legs=[[(-15, 52), (-18, 12)], [(15, 52), (18, 12)]],
        feet=[(-21, 7, 0), (21, 7, 0)],
    ),
    "tiptoe": dict(
        arms=[[(-30, 96), (-60, 100), (-50, 124)], [(30, 96), (60, 100), (50, 124)]],
        legs=[[(-15, 52), (-26, 32), (-24, 16)], [(15, 52), (28, 34), (34, 18)]],
        feet=[(-28, 10, -25), (38, 12, -25)],
    ),
    "crane": dict(
        arms=[[(-30, 96), (-62, 114), (-88, 132)], [(30, 96), (62, 114), (88, 132)]],
        legs=[[(-8, 52), (-6, 12)], [(14, 52), (46, 70), (28, 46)]],
        feet=[(-8, 7, 0), (24, 42, 20)],
    ),
    "kick": dict(
        arms=[[(-30, 96), (-58, 104), (-62, 126)], [(30, 96), (50, 84), (40, 72)]],
        legs=[[(-12, 52), (-26, 12)], [(14, 52), (60, 70), (100, 82)]],
        feet=[(-30, 7, 0), (110, 84, 80)],
    ),
    "cheer": dict(
        arms=[[(-30, 96), (-54, 126), (-52, 164)], [(30, 96), (54, 126), (52, 164)]],
        legs=[[(-15, 52), (-26, 12)], [(15, 52), (26, 12)]],
        feet=[(-29, 7, 0), (29, 7, 0)],
    ),
    "reach": dict(
        arms=[[(-30, 96), (-44, 76), (-46, 58)], [(30, 96), (42, 132), (46, 172)]],
        legs=[[(-15, 52), (-18, 12)], [(15, 52), (18, 12)]],
        feet=[(-21, 7, 0), (21, 7, 0)],
    ),
    "run": dict(
        arms=[[(-30, 96), (-52, 80), (-40, 62)], [(30, 96), (56, 112), (74, 104)]],
        legs=[[(-15, 52), (-40, 40), (-58, 24)], [(15, 52), (38, 32), (28, 12)]],
        feet=[(-64, 22, 40), (32, 7, 0)],
    ),
    "hold": dict(
        arms=[[(-30, 96), (-36, 72), (-12, 76)], [(30, 96), (36, 72), (12, 76)]],
        legs=[[(-15, 52), (-18, 12)], [(15, 52), (18, 12)]],
        feet=[(-21, 7, 0), (21, 7, 0)],
    ),
    "bow": dict(
        arms=[[(-30, 96), (-20, 80), (2, 86)], [(30, 96), (20, 80), (-2, 86)]],
        legs=[[(-15, 52), (-18, 12)], [(15, 52), (18, 12)]],
        feet=[(-21, 7, 0), (21, 7, 0)],
    ),
    "push": dict(
        arms=[[(-30, 96), (14, 84), (58, 92)], [(30, 96), (54, 88), (66, 104)]],
        legs=[[(-15, 52), (-40, 14)], [(15, 52), (16, 12)]],
        feet=[(-44, 8, -20), (20, 7, 0)],
    ),
    "point": dict(
        arms=[[(-30, 96), (-44, 76), (-46, 58)], [(30, 96), (60, 126), (80, 156)]],
        legs=[[(-15, 52), (-18, 12)], [(15, 52), (18, 12)]],
        feet=[(-21, 7, 0), (21, 7, 0)],
    ),
    "sit": dict(
        arms=[[(-30, 96), (-48, 72), (-44, 56)], [(30, 96), (48, 72), (44, 56)]],
        legs=None,
        feet=None,
    ),
}


def ninja(a, x, y, s=1.0, gi=KAI_GI, band=KAI_BAND, pose="stand", flip=False,
          bun=False, face="happy", eyes_closed=False, blank_face=False, tilt=0):
    """A friendly little ninja.  Feet sit on (x, y); about 200*s tall."""
    P = POSES[pose]
    with a.at(x, y, s, flip=flip, rot=tilt):
        dy = 0
        if pose == "sit":
            dy = -34
            a.limb([(-50, 10), (50, 10)], 22, gi)
            a.limb([(-14, 22), (-58, 14)], 24, gi)
            a.limb([(14, 22), (58, 14)], 24, gi)
            a.ellipse(-62, 14, 12, 9, SHOE)
            a.ellipse(62, 14, 12, 9, SHOE)
        else:
            for leg in P["legs"]:
                a.limb(leg, 20, gi)
            for fx, fy, rot in P["feet"]:
                with a.at(fx, fy, 1, rot=rot):
                    a.ellipse(0, 0, 13, 8, SHOE)
        with a.at(0, dy):
            # torso
            a.poly([(-30, 102), (30, 102), (27, 50), (-27, 50)], gi)
            a.line([(-15, 102), (9, 64)])
            a.line([(15, 102), (2, 82)])
            # belt
            a.rrect(-29, 52, 58, 12, 4, band)
            a.limb([(6, 58), (12, 40)], 6, band)
            a.limb([(6, 58), (20, 44)], 6, band)
            a.circle(6, 58, 6, band)
            # arms + hands
            for arm in P["arms"]:
                a.limb(arm, 16, gi)
                hx, hy = arm[-1]
                a.circle(hx, hy, 9, SKIN)
            ninja_head(a, gi, band, bun, face, eyes_closed, blank_face, s)


def ninja_head(a, gi, band, bun, face, eyes_closed, blank_face, s):
    """Head in ninja-local units (center at 0, 148)."""
    if bun:
        a.circle(0, 198, 16, gi)
        a.limb([(-10, 190), (10, 190)], 7, band)
    # headband tails (behind head)
    a.limb([(40, 170), (64, 184), (82, 172)], 9, band)
    a.limb([(40, 166), (62, 160), (76, 146)], 9, band)
    a.circle(0, 148, 48, gi)
    a.ellipse(0, 143, 35, 25, SKIN)
    a.limb([(-44, 174), (-20, 181), (20, 181), (44, 174)], 11, band)
    a.circle(44, 172, 6, band)
    if not blank_face:
        if eyes_closed:
            a.arc(-13, 148, 7, 200, 140, w=2.4 * s if a.color else 3 * s)
            a.arc(13, 148, 7, 200, 140, w=2.4 * s if a.color else 3 * s)
        else:
            for ex in (-13, 13):
                a.c.setFillColor(a.ink)
                a.c.ellipse(ex - 5.5, 140, ex + 5.5, 155, stroke=0, fill=1)
                a.c.setFillColor(white)
                a.c.circle(ex + 2, 151, 2.2, stroke=0, fill=1)
        if a.color:
            a.c.setFillColor(HexColor("#f29a9a"))
            a.c.circle(-24, 134, 5, stroke=0, fill=1)
            a.c.circle(24, 134, 5, stroke=0, fill=1)
        if face == "happy":
            a.arc(0, 137, 8, 200, 140)
        elif face == "o":
            a.ellipse(0, 130, 4, 5, "#c0504d")
        elif face == "brave":
            a.line([(-6, 129), (6, 129)])


def sleepy_head(a, x, y, s=1.0, gi=KAI_GI, band=KAI_BAND, rot=0, face="happy", eyes_closed=False):
    """Just a ninja head (for a ninja tucked into bed)."""
    with a.at(x, y, s, rot=rot):
        with a.at(0, -148):
            ninja_head(a, gi, band, False, face, eyes_closed, False, s)


def owl(a, x, y, s=1.0, flip=False, stick=True, eyes_closed=False):
    """Sensei Owl, the wise teacher.  About 180*s tall."""
    BR, BELLY, FACE = "#9c6b43", "#f3dfb8", "#fff3da"
    with a.at(x, y, s, flip=flip):
        if stick:
            a.limb([(78, 0), (82, 150)], 9, "#7fb24a")
            for yy in (40, 80, 120):
                a.line([(75, yy), (86, yy + 1)])
            a.ellipse(96, 140, 14, 6, "#7fb24a")
        a.ellipse(-12, 10, 13, 7, "#f2a33a")
        a.ellipse(12, 10, 13, 7, "#f2a33a")
        # ear tufts
        a.poly([(-46, 124), (-56, 168), (-22, 140)], BR)
        a.poly([(46, 124), (56, 168), (22, 140)], BR)
        a.ellipse(0, 80, 58, 74, BR)
        a.ellipse(0, 64, 38, 48, BELLY)
        for row, yy in enumerate((82, 64, 46)):
            for xx in ((-14, 0, 14) if row != 1 else (-22, -7, 8, 23)):
                a.arc(xx, yy, 7, 200, 140)
        # wings
        with a.at(-56, 74, 1, rot=-12):
            a.ellipse(0, 0, 14, 40, BR)
        with a.at(56, 74, 1, rot=12):
            a.ellipse(0, 0, 14, 40, BR)
        # face
        a.circle(-22, 116, 24, FACE)
        a.circle(22, 116, 24, FACE)
        if eyes_closed:
            a.arc(-22, 118, 9, 200, 140, w=2.6 * s)
            a.arc(22, 118, 9, 200, 140, w=2.6 * s)
        else:
            for ex in (-22, 22):
                a.dot(ex, 116, 10)
                a.c.setFillColor(white)
                a.c.circle(ex + 3, 120, 3.2, stroke=0, fill=1)
        # bushy wise eyebrows
        a.limb([(-40, 142), (-26, 146), (-10, 140)], 6, "#f7f2e8")
        a.limb([(40, 142), (26, 146), (10, 140)], 6, "#f7f2e8")
        a.poly([(-8, 104), (8, 104), (0, 90)], "#f2a33a")
        # green sensei belt
        a.limb([(-50, 30), (0, 24), (50, 30)], 8, "#2f8f5b")


def cat(a, x, y, s=1.0, flip=False, sleeping=False):
    """Pip the orange cat, sitting.  About 115*s tall."""
    OR, PINK = "#f29b38", "#f5a8b8"
    with a.at(x, y, s, flip=flip):
        a.limb([(24, 10), (56, 18), (62, 48), (50, 66)], 11, OR)
        a.ellipse(0, 36, 32, 36, OR)
        a.ellipse(0, 30, 17, 22, "#fbd9a8")
        a.ellipse(-14, 4, 11, 7, OR)
        a.ellipse(14, 4, 11, 7, OR)
        a.poly([(-28, 92), (-24, 122), (-6, 104)], OR)
        a.poly([(28, 92), (24, 122), (6, 104)], OR)
        a.poly([(-23, 98), (-21, 114), (-11, 104)], PINK)
        a.poly([(23, 98), (21, 114), (11, 104)], PINK)
        a.circle(0, 86, 30, OR)
        a.line([(-6, 115), (-4, 104)])
        a.line([(0, 116), (0, 105)])
        a.line([(6, 115), (4, 104)])
        if sleeping:
            a.arc(-11, 89, 6, 200, 140)
            a.arc(11, 89, 6, 200, 140)
        else:
            for ex in (-11, 11):
                a.dot(ex, 88, 4.5)
                a.c.setFillColor(white)
                a.c.circle(ex + 1.5, 90, 1.5, stroke=0, fill=1)
        a.poly([(-4, 80), (4, 80), (0, 75)], PINK)
        a.arc(-4, 75, 4, 200, 120)
        a.arc(4, 75, 4, 220, 120)
        for d in (-1, 1):
            a.line([(d * 14, 80), (d * 38, 84)])
            a.line([(d * 14, 76), (d * 38, 72)])


def bird(a, x, y, s=1.0, flip=False, col="#5ab3e8"):
    with a.at(x, y, s, flip=flip):
        a.poly([(-16, 4), (-34, 14), (-32, -4)], col)
        a.circle(0, 0, 18, col)
        a.ellipse(2, -6, 11, 7, "#fff1c9")
        with a.at(-4, 2, 1, rot=-20):
            a.ellipse(0, 0, 10, 6, col)
        a.poly([(16, 4), (28, 0), (16, -3)], "#f2a33a")
        a.dot(8, 6, 3)


def turtle(a, x, y, s=1.0, flip=False):
    with a.at(x, y, s, flip=flip):
        G, SH = "#8cc65a", "#4f9a4a"
        a.ellipse(-26, 6, 10, 7, G)
        a.ellipse(24, 6, 10, 7, G)
        a.circle(54, 26, 14, G)
        a.dot(58, 30, 2.5)
        a.arc(56, 24, 5, 220, 100)
        a.poly([(-44, 14), (-56, 10), (-44, 20)], G)
        a.poly([(-46, 12), (-40, 46, -10, 58, 0, 58), (10, 58, 40, 46, 46, 12)], SH)
        a.line([(-22, 14), (-14, 40), (14, 40), (22, 14)])
        a.line([(-14, 40), (0, 56)])
        a.line([(14, 40), (0, 56)])


def butterfly(a, x, y, s=1.0, col="#f7a531"):
    with a.at(x, y, s):
        for d in (-1, 1):
            a.ellipse(d * 14, 10, 14, 16, col)
            a.ellipse(d * 11, -10, 10, 11, col)
            a.circle(d * 14, 12, 4, "#ffffff")
        a.ellipse(0, 0, 4, 20, "#3d3550")
        a.line([(0, 18), (-8, 30)])
        a.line([(0, 18), (8, 30)])


# =====================================================================
# Scenery
# =====================================================================
def sky(a, top, bottom, w=600, h=600):
    if not a.color:
        return
    c = a.c
    t, b = HexColor(top), HexColor(bottom)
    n = 40
    for i in range(n):
        f = i / (n - 1)
        col = HexColor(0)
        col.red = b.red + (t.red - b.red) * f
        col.green = b.green + (t.green - b.green) * f
        col.blue = b.blue + (t.blue - b.blue) * f
        c.setFillColor(col)
        c.rect(0, h * i / n, w, h / n + 1, stroke=0, fill=1)


def hill(a, y, f, amp=18, w=600, phase=0.0, waves=1.5):
    pts = [(-10, -10), (-10, y)]
    for i in range(0, 61):
        xx = -10 + (w + 20) * i / 60
        pts.append((xx, y + amp * math.sin(phase + waves * math.pi * i / 60)))
    pts += [(w + 10, -10)]
    a.poly(pts, f)


def mountain(a, x, y, w, h, f="#8a9cc7", snow="#ffffff"):
    a.poly([(x - w / 2, y), (x, y + h), (x + w / 2, y)], f)
    cap = h * 0.28
    sw = w / 2 * 0.28
    a.poly([(x - sw, y + h - cap), (x, y + h), (x + sw, y + h - cap),
            (x + sw * 0.45, y + h - cap * 0.7), (x, y + h - cap * 1.05),
            (x - sw * 0.45, y + h - cap * 0.7)], snow)


def moon(a, x, y, r):
    a.circle(x, y, r, "#fbe9a6")
    a.circle(x - r * 0.3, y + r * 0.2, r * 0.18, "#f1d77f")
    a.circle(x + r * 0.35, y - r * 0.25, r * 0.13, "#f1d77f")
    a.circle(x + r * 0.1, y + r * 0.5, r * 0.09, "#f1d77f")


def star(a, x, y, r, f="#ffd84a", rot=0):
    pts = []
    for i in range(10):
        ang = math.radians(90 + rot + i * 36)
        rr = r if i % 2 == 0 else r * 0.48
        pts.append((x + rr * math.cos(ang), y + rr * math.sin(ang)))
    a.poly(pts, f)


def sun(a, x, y, r, smile=True):
    for i in range(10):
        ang = math.radians(i * 36 + 18)
        a.limb([(x + (r + 10) * math.cos(ang), y + (r + 10) * math.sin(ang)),
                (x + (r + 26) * math.cos(ang), y + (r + 26) * math.sin(ang))], 8, "#ffc93c")
    a.circle(x, y, r, "#ffd84a")
    if smile:
        a.dot(x - r * 0.3, y + r * 0.15, r * 0.08)
        a.dot(x + r * 0.3, y + r * 0.15, r * 0.08)
        a.arc(x, y - r * 0.05, r * 0.35, 210, 120)


def cloud(a, x, y, s=1.0, f="#ffffff"):
    with a.at(x, y, s):
        a.blob([(-40, 0, 24), (-14, 14, 30), (18, 10, 26), (42, 0, 20), (0, -6, 24), (-28, -8, 18), (26, -8, 18)], f)


def rain_cloud(a, x, y, s=1.0):
    cloud(a, x, y, s, "#a7b3c9")


def tree(a, x, y, s=1.0, kind="round"):
    with a.at(x, y, s):
        a.poly([(-12, 0), (-8, 90), (8, 90), (12, 0)], "#9a6a3e")
        a.limb([(0, 70), (-28, 100)], 8, "#9a6a3e")
        if kind == "blossom":
            circ = [(-50, 130, 34), (-10, 155, 40), (36, 135, 36), (0, 115, 34), (-40, 100, 22), (44, 102, 22)]
            a.blob(circ, "#f8b8cf")
            for fx, fy in [(-50, 140), (-20, 165), (10, 150), (40, 140), (-5, 120), (30, 110), (-35, 110), (-60, 120), (55, 125)]:
                flower_tiny(a, fx, fy, 6)
        else:
            circ = [(-46, 128, 34), (-6, 156, 40), (40, 130, 36), (0, 112, 34), (-36, 98, 22), (42, 100, 22)]
            a.blob(circ, "#6dbb5b")
            a.arc(-30, 130, 14, 30, 120)
            a.arc(24, 148, 14, 30, 120)


def flower_tiny(a, x, y, r):
    for i in range(5):
        ang = math.radians(90 + i * 72)
        a.circle(x + r * math.cos(ang), y + r * math.sin(ang), r * 0.7, "#ffffff")
    a.circle(x, y, r * 0.55, "#f5d64e")


def flower(a, x, y, s=1.0, petal="#f26b8a", stem=True):
    with a.at(x, y, s):
        if stem:
            a.limb([(0, 0), (0, 44)], 5, "#5fae4f")
            with a.at(8, 18, 1, rot=30):
                a.ellipse(0, 0, 11, 5, "#6dbb5b")
        circ = []
        for i in range(5):
            ang = math.radians(90 + i * 72)
            circ.append((12 * math.cos(ang), 56 + 12 * math.sin(ang), 10))
        a.blob(circ, petal)
        a.circle(0, 56, 7, "#ffd84a")


def bamboo(a, x, y, h, s=1.0):
    with a.at(x, y, s):
        n = int(h // 50)
        for i in range(n):
            a.rrect(-9, i * 50, 18, 50, 4, "#8cc65a")
        for i, d in enumerate((1, -1, 1)):
            yy = 70 + i * 90
            if yy < h - 20:
                with a.at(d * 26, yy, 1, rot=d * 20):
                    a.ellipse(0, 0, 22, 6, "#5fae4f")


def house(a, x, y, s=1.0, door="#c0504d", lit=False):
    with a.at(x, y, s):
        a.rect(-70, 0, 140, 90, "#f7e3c0")
        a.rrect(-18, 0, 36, 56, 6, door)
        a.circle(10, 28, 3, "#ffd84a")
        win = "#ffd84a" if lit else "#bfe3f2"
        a.rect(-56, 40, 26, 26, win)
        a.line([(-43, 40), (-43, 66)])
        a.line([(-56, 53), (-30, 53)])
        a.rect(30, 40, 26, 26, win)
        a.line([(43, 40), (43, 66)])
        a.line([(30, 53), (56, 53)])
        roof = [(-100, 82), (-86, 96, -80, 100, -70, 104), (-40, 140), (40, 140),
                (70, 104), (80, 100, 86, 96, 100, 82)]
        a.poly(roof, "#3a8d7a")
        a.rect(-46, 138, 92, 10, "#2f7363")
        # lantern
        a.line([(80, 96), (80, 84)])
        a.ellipse(80, 72, 10, 13, "#e8423a")
        a.line([(72, 72), (88, 72)])


def bridge(a, x0, x1, y, sag=40):
    pts = []
    n = 12
    for i in range(n + 1):
        t = i / n
        xx = x0 + (x1 - x0) * t
        yy = y - sag * 4 * t * (1 - t)
        pts.append((xx, yy))
    for xx in (x0, x1):
        a.rrect(xx - 8, y - 70, 16, 130, 4, "#9a6a3e")
    for i in range(n):
        (xa, ya), (xb, yb) = pts[i], pts[i + 1]
        mx, my = (xa + xb) / 2, (ya + yb) / 2
        ang = math.degrees(math.atan2(yb - ya, xb - xa))
        with a.at(mx, my, 1, rot=ang):
            a.rect(-(xb - xa) / 2 + 2, -6, (xb - xa) - 4, 12, "#c99a5c")
    rope = [(p[0], p[1] + 48) for p in pts]
    a.line(rope, w=3)
    for (px, py), (rx, ry) in zip(pts[1:-1:2], rope[1:-1:2]):
        a.line([(px, py + 6), (rx, ry)], w=2)


def river(a, y0, y1, w=600):
    pts = [(-10, y0)]
    for i in range(31):
        xx = -10 + (w + 20) * i / 30
        pts.append((xx, y1 + 6 * math.sin(i * 0.8)))
    pts.append((w + 10, y0))
    a.poly(pts, "#79c3ea")
    for i, (wx, wy) in enumerate([(80, y0 + 20), (220, y0 + 36), (380, y0 + 18), (520, y0 + 34), (300, y0 + 6)]):
        if wy < y1 - 6:
            a.arc(wx, wy, 12, 20, 140)
            a.arc(wx + 24, wy, 12, 20, 140)


def rock(a, x, y, w, h, f="#b9b2a8"):
    a.poly([(x - w / 2, y), (x - w / 2 + 6, y + h * 0.7), (x - w * 0.15, y + h),
            (x + w * 0.25, y + h * 0.92), (x + w / 2, y + h * 0.4), (x + w / 2 - 4, y)], f)


def kite(a, x, y, s=1.0, string_to=None):
    with a.at(x, y, s):
        if string_to:
            sx, sy = string_to
            a.line([(0, -60), ((sx - x) / s * 0.5, (sy - y) / s * 0.6), ((sx - x) / s, (sy - y) / s)], w=1.5)
        a.poly([(0, 60), (40, 0), (0, -60), (-40, 0)], "#f7c531")
        a.poly([(0, 60), (40, 0), (0, 0)], "#e8423a")
        a.poly([(0, -60), (-40, 0), (0, 0)], "#e8423a")
        a.line([(0, 60), (0, -60)])
        a.line([(-40, 0), (40, 0)])
        tail = [(0, -60), (-10, -90), (8, -120), (-6, -150)]
        a.line(tail)
        for tx, ty in tail[1:]:
            a.poly([(tx - 10, ty + 6), (tx + 10, ty - 6), (tx + 10, ty + 6), (tx - 10, ty - 6)], "#3a6fd6")


def lantern(a, x, y, s=1.0, f="#e8423a"):
    with a.at(x, y, s):
        a.rect(-8, 34, 16, 6, "#3d3550")
        a.ellipse(0, 12, 22, 24, f)
        for d in (-12, 0, 12):
            a.arc(d * 1.0, 12, 22 if d == 0 else 26, 240 if d < 0 else (300 if d > 0 else 270), 0.01)
        a.line([(-18, 22), (18, 22)])
        a.line([(-20, 4), (20, 4)])
        a.rect(-8, -16, 16, 6, "#3d3550")
        if a.color:
            a.c.setFillColor(HexColor("#fff3a6"))
            a.c.circle(0, 12, 6, stroke=0, fill=1)


def heart(a, x, y, s=1.0, f="#e8423a"):
    with a.at(x, y, s):
        a.poly([(0, -40), (-30, -10, -60, 20, -40, 40), (-24, 56, -4, 46, 0, 30),
                (4, 46, 24, 56, 40, 40), (60, 20, 30, -10, 0, -40)], f)


def nest(a, x, y, s=1.0):
    with a.at(x, y, s):
        a.poly([(-46, 10), (-36, -14, 36, -14, 46, 10)], "#b9844f")
        for i in range(5):
            a.arc(-30 + i * 15, 4, 10, 200, 140)


def grass(a, x, y, s=1.0):
    with a.at(x, y, s):
        a.poly([(-14, 0), (-10, 22), (-4, 4), (0, 28), (4, 4), (10, 22), (14, 0)], "#5fae4f")


def zzz(a, x, y, s=1.0):
    for i, (dx, dy, sz) in enumerate([(0, 0, 22), (22, 26, 28), (50, 58, 34)]):
        a.text(x + dx * s, y + dy * s, "z", sz * s, fill="#ffffff")


# =====================================================================
# Props for "Little Ninja and the Dark Night" and "The Ninja Team"
# =====================================================================
def frog(a, x, y, s=1.0, flip=False, singing=False):
    G, B = "#7cc95a", "#d8f0b0"
    with a.at(x, y, s, flip=flip):
        a.ellipse(-26, 4, 16, 8, G)
        a.ellipse(26, 4, 16, 8, G)
        a.ellipse(0, 26, 38, 28, G)
        a.ellipse(0, 20, 22, 16, B)
        a.circle(-18, 52, 12, G)
        a.circle(18, 52, 12, G)
        a.circle(-18, 54, 7, "#ffffff")
        a.circle(18, 54, 7, "#ffffff")
        a.dot(-17, 54, 3.5)
        a.dot(19, 54, 3.5)
        if singing:
            a.ellipse(0, 34, 9, 6, "#c0504d")
        else:
            a.arc(0, 40, 14, 220, 100)


def lily_pad(a, x, y, s=1.0):
    with a.at(x, y, s):
        a.poly([(0, 0), (40, 6, 40, 30, 0, 30), (-40, 30, -40, 6, -6, 2), (0, 15)], "#5fae4f")


def pond(a, x, y, rx, ry):
    a.ellipse(x, y, rx, ry, "#79c3ea")
    a.arc(x - rx * 0.4, y, 14, 20, 140)
    a.arc(x + rx * 0.3, y - ry * 0.3, 14, 20, 140)


def firefly(a, x, y, s=1.0):
    if a.color:
        a.c.saveState()
        a.c.setFillColor(HexColor("#fff6a0"))
        a.c.setFillAlpha(0.35)
        a.c.circle(x, y, 18 * s, stroke=0, fill=1)
        a.c.restoreState()
    with a.at(x, y, s):
        a.ellipse(-6, 8, 7, 5, "#ffffff")
        a.ellipse(6, 8, 7, 5, "#ffffff")
        a.ellipse(0, 0, 6, 10, "#ffe45c")
        a.circle(0, 12, 4, "#3d3550")


def peach(a, x, y, s=1.0, rot=0):
    with a.at(x, y, s, rot=rot):
        a.limb([(0, 96), (4, 112)], 6, "#9a6a3e")
        with a.at(26, 110, 1, rot=20):
            a.ellipse(0, 0, 22, 9, "#6dbb5b")
        a.poly([(0, 96), (-40, 112, -70, 80, -66, 46), (-62, 0, -26, -4, 0, 0),
                (26, -4, 62, 0, 66, 46), (70, 80, 40, 112, 0, 96)], "#ffab7a")
        a.line([(0, 94), (-14, 60, -12, 24, -6, 4)])
        if a.color:
            a.c.setFillColor(HexColor("#ff8a6e"))
            a.c.circle(30, 40, 18, stroke=0, fill=1)


def peach_slice(a, x, y, s=1.0, rot=0):
    with a.at(x, y, s, rot=rot):
        a.poly([(0, 0), (30, 0), (30, 26, 10, 34, 0, 0)], "#ffcf9a")
        a.limb([(30, 0), (30, 22)], 3, "#ff8a6e")


def blanket(a, x, y, w, h):
    sk = 40
    a.poly([(x, y), (x + w, y), (x + w - sk, y + h), (x + sk, y + h)], "#e8423a")
    for i in range(1, 6):
        t = i / 6
        a.line([(x + w * t, y), (x + sk + (w - 2 * sk) * t, y + h)], w=2)
    for i in range(1, 3):
        t = i / 3
        a.line([(x + sk * t, y + h * t), (x + w - sk * t, y + h * t)], w=2)


def basket(a, x, y, s=1.0):
    with a.at(x, y, s):
        a.arc(0, 40, 30, 0, 180, w=7 * s)
        a.poly([(-42, 40), (42, 40), (34, 0), (-34, 0)], "#d6a25e")
        a.line([(-38, 26), (38, 26)])
        a.line([(-36, 12), (36, 12)])


def scroll(a, x, y, s=1.0):
    with a.at(x, y, s):
        a.rect(-34, -24, 68, 48, "#fbf1d6")
        a.circle(-36, 0, 6, "#c0504d")
        a.limb([(-38, -26), (-38, 26)], 8, "#9a6a3e")
        a.limb([(38, -26), (38, 26)], 8, "#9a6a3e")
        for yy in (12, 0, -12):
            a.line([(-22, yy), (22, yy)], w=1.5)


def window(a, x, y, w, h, night=True, moon_in=True):
    """A window frame with a view of the night sky."""
    a.rect(x - 10, y - 10, w + 20, h + 20, "#9a6a3e")
    a.rect(x, y, w, h, "#2c3a75" if night else "#bfe3f2")
    if moon_in:
        moon(a, x + w * 0.65, y + h * 0.65, min(w, h) * 0.18)
        star(a, x + w * 0.25, y + h * 0.75, 8)
        star(a, x + w * 0.35, y + h * 0.35, 6)
    a.rect(x + w / 2 - 4, y, 8, h, "#9a6a3e")
    a.rect(x, y + h / 2 - 4, w, 8, "#9a6a3e")
    a.rect(x - 16, y - 18, w + 32, 12, "#9a6a3e")


def bed(a, x, y, s=1.0, who=None, eyes_closed=False, face="happy", peeking=False):
    """A bed (side view) with a ninja tucked in. who = (gi, band) or None."""
    with a.at(x, y, s):
        a.rrect(-150, 0, 20, 130, 6, "#9a6a3e")
        a.rrect(130, 0, 20, 90, 6, "#9a6a3e")
        a.rect(-140, 30, 280, 40, "#c99a5c")
        a.ellipse(-90, 90, 50, 24, "#ffffff")
        if who:
            gi, band = who
            sleepy_head(a, -88, 124, 0.85, gi, band, rot=0 if peeking else 12, face=face, eyes_closed=eyes_closed)
        a.poly([(-128, 66), (-128, 90, -100, 94, -60, 92), (40, 100, 110, 100, 140, 90), (140, 66)], "#7ed0f5")
        a.line([(-60, 72), (130, 72)], w=2)
        if who:
            a.circle(-112, 92, 9, SKIN)
            a.circle(-64, 93, 9, SKIN)


def lamp(a, x, y, s=1.0, on=True):
    with a.at(x, y, s):
        if on and a.color:
            a.c.saveState()
            a.c.setFillColor(HexColor("#fff3a6"))
            a.c.setFillAlpha(0.35)
            a.c.circle(0, 60, 70, stroke=0, fill=1)
            a.c.restoreState()
        a.ellipse(0, 4, 26, 6, "#9a6a3e")
        a.rect(-4, 4, 8, 50, "#9a6a3e")
        a.poly([(-30, 50), (30, 50), (18, 86), (-18, 86)], "#ffd84a")


def motion_lines(a, x, y, n=3, gap=22, length=50, w=3):
    for i in range(n):
        a.line([(x, y + i * gap), (x + length, y + i * gap)], w=w)
