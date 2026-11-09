"""Builds the story book and the three coloring books as printable PDFs.

    python3 books/source/build.py
"""
import os
import sys

from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

sys.path.insert(0, os.path.dirname(__file__))
from art import Art, star, INK_COLOR  # noqa: E402
import scenes as S  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
pdfmetrics.registerFont(TTFont("Kid", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("KidReg", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))

INK = HexColor(INK_COLOR)
TITLE = "The Way of the Ninja"


def wrap(text, font, size, width):
    lines = []
    for para in text.split("\n"):
        cur = ""
        for word in para.split():
            trial = (cur + " " + word).strip()
            if pdfmetrics.stringWidth(trial, font, size) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_scene(c, scene, x, y, size, color, frame=True, radius=18):
    c.saveState()
    p = c.beginPath()
    p.roundRect(x, y, size, size, radius)
    c.clipPath(p, stroke=0, fill=0)
    c.setFillColor(white)
    c.rect(x, y, size, size, stroke=0, fill=1)
    a = Art(c, color=color)
    with a.at(x, y, size / 600.0):
        scene(a)
    c.restoreState()
    if frame:
        c.setStrokeColor(INK if color else black)
        c.setLineWidth(4)
        c.roundRect(x, y, size, size, radius, stroke=1, fill=0)


def text_panel(c, text, x, y, w, size=23, top=True, alpha=0.9):
    lines = wrap(text, "Kid", size, w - 40)
    lh = size * 1.3
    h = lh * len(lines) + 30
    py = y - h if top else y
    c.saveState()
    c.setFillColor(white)
    c.setFillAlpha(alpha)
    c.setStrokeColor(INK)
    c.setLineWidth(2.5)
    c.roundRect(x, py, w, h, 18, stroke=1, fill=1)
    c.restoreState()
    c.setFillColor(INK)
    c.setFont("Kid", size)
    ty = py + h - 15 - size
    for ln in lines:
        c.drawCentredString(x + w / 2, ty, ln)
        ty -= lh


# =====================================================================
# Story book (8.5 x 8.5 in)
# =====================================================================
STORY = [
    (S.village, "In a little village by the big mountains lived a little ninja named Kai.", "top"),
    (S.meet_sensei, "Kai wanted to be a GREAT ninja. So Kai bowed to Sensei Owl and asked, “Will you teach me?”", "top"),
    (S.five_secrets, "“The Way of the Ninja has five secrets,” said Sensei Owl. “Let’s learn them one by one.”", "top"),
    (S.quiet, "Secret number one: Be QUIET.\nKai tiptoed past sleepy Pip. Tip… tip… toe. Shhh!", "top"),
    (S.patient, "Secret number two: Be PATIENT.\nKai sat very still. Breathe in… breathe out. Slow, like a turtle.", "top"),
    (S.strong, "Secret number three: Be STRONG.\nKai stood on one foot like a crane. Miko practiced her kicks. Hi-YA!", "top"),
    (S.kind, "Secret number four: Be KIND.\nOh no! Pip was stuck up in a tree. Kai reached up and helped Pip down.", "top"),
    (S.brave, "Secret number five: Be BRAVE.\nThe bridge was wobbly. Kai felt scared… but took one step, then another!", "top"),
    (S.storm, "One stormy night, Kai heard a tiny “peep!” A little bird was lost. Kai stayed calm and held up a light.", "top"),
    (S.home_nest, "Kai gently carried the bird home to its nest. “Hooray!” cheered Miko. The bird family sang a happy song.", "top"),
    (S.big_heart, "“You found the Way of the Ninja,” said Sensei Owl. “A true ninja has a BIG, kind heart.”", "top"),
    (S.goodnight, "Goodnight, little ninja. Goodnight, Pip. Tomorrow, the Ninja Way begins again.", "top"),
]


def build_story(path):
    W = 8.5 * inch
    c = canvas.Canvas(path, pagesize=(W, W))
    c.setTitle(TITLE)
    c.setAuthor("Ninja Books")

    # Cover
    draw_scene(c, S.cover, 0, 0, W, True, frame=False, radius=0)
    c.setFont("Kid", 54)
    for line, y in (("The Way of", 530), ("the Ninja", 468)):
        c.setFillColor(HexColor("#120d24"))
        c.drawCentredString(W / 2 + 3, y - 3, line)
        c.setFillColor(HexColor("#ffd84a"))
        c.drawCentredString(W / 2, y, line)
    c.setFont("Kid", 15)
    c.setFillColor(white)
    c.drawCentredString(W / 2, 430, "A story about being quiet, patient, strong, kind and brave")
    c.showPage()

    # Title page
    c.setFillColor(HexColor("#fff8ec"))
    c.rect(0, 0, W, W, stroke=0, fill=1)
    a = Art(c, True)
    for i, (x, y) in enumerate([(206, 300), (256, 330), (306, 345), (356, 330), (406, 300)]):
        star(a, x, y, 24, ["#ffd84a", "#7ed0f5", "#9ad46b", "#f58fb0", "#ffa94d"][i])
    c.setFillColor(INK)
    c.setFont("Kid", 40)
    c.drawCentredString(W / 2, 420, TITLE)
    c.setFont("KidReg", 18)
    c.drawCentredString(W / 2, 240, "For brave little ninjas, ages 3 and up")
    c.showPage()

    for scene, text, pos in STORY:
        draw_scene(c, scene, 0, 0, W, True, frame=False, radius=0)
        if pos == "top":
            text_panel(c, text, 40, W - 30, W - 80)
        else:
            text_panel(c, text, 40, 30, W - 80, top=False)
        c.showPage()

    # The Ninja Promise
    c.setFillColor(HexColor("#fff8ec"))
    c.rect(0, 0, W, W, stroke=0, fill=1)
    c.setFillColor(INK)
    c.setFont("Kid", 34)
    c.drawCentredString(W / 2, 535, "The Ninja Promise")
    c.setFont("KidReg", 15)
    c.drawCentredString(W / 2, 505, "Say it out loud with a grown-up!")
    a = Art(c, True)
    promise = [("I am QUIET.", "#ffd84a"), ("I am PATIENT.", "#7ed0f5"), ("I am STRONG.", "#9ad46b"),
               ("I am KIND.", "#f58fb0"), ("I am BRAVE.", "#ffa94d")]
    y = 440
    for words, col in promise:
        star(a, 170, y + 10, 22, col)
        c.setFillColor(INK)
        c.setFont("Kid", 30)
        c.drawString(210, y, words)
        y -= 66
    c.setFont("Kid", 32)
    c.setFillColor(HexColor("#e8423a"))
    c.drawCentredString(W / 2, 80, "I am a NINJA!")
    c.showPage()

    # The End
    draw_scene(c, S.big_heart, 0, 0, W, True, frame=False, radius=0)
    text_panel(c, "The End", W / 2 - 130, W - 60, 260, size=40)
    c.showPage()
    c.save()


# =====================================================================
# Coloring books (US Letter, portrait)
# =====================================================================
LW, LH = 8.5 * inch, 11 * inch

BOOKS = [
    dict(
        file="Coloring-Book-1-Meet-the-Ninjas.pdf",
        num=1, name="Meet the Ninjas", cover=S.friends,
        pages=[
            (S.solo_kai, "This is Kai, a little ninja."),
            (S.solo_miko, "This is Miko, Kai’s best friend."),
            (S.solo_owl, "This is Sensei Owl, the wise teacher."),
            (S.solo_cat, "This is Pip, Kai’s silly cat."),
            (S.kai_and_pip, "Kai and Pip are always together."),
            (S.dojo, "This is the little ninja house."),
            (S.blossom, "Miko loves the pink blossom tree."),
            (S.night_mountains, "Ninjas love the moon and stars."),
            (S.big_bird, "Peep, peep! A little bird."),
            (S.friends, "Ninja friends forever!"),
        ],
        last=(S.draw_your_face, "Draw YOUR face. Now you are a ninja too!"),
    ),
    dict(
        file="Coloring-Book-2-Ninja-Training.pdf",
        num=2, name="Ninja Training", cover=S.strong,
        pages=[
            (S.five_secrets, "Sensei Owl teaches the five secrets."),
            (S.quiet, "Secret 1: Be QUIET. Tip, tip, toe!"),
            (S.patient, "Secret 2: Be PATIENT. Breathe in, breathe out."),
            (S.crane_solo, "Secret 3: Be STRONG. Stand like a crane!"),
            (S.kick_practice, "Miko practices her kicks. Hi-YA!"),
            (S.kind, "Secret 4: Be KIND. Help a friend."),
            (S.brave, "Secret 5: Be BRAVE. One step at a time."),
            (S.run_with_pip, "Ninjas run fast, fast, fast!"),
            (S.stretch, "Reach up high to the sun!"),
            (S.breathing, "Rest time. Slow, quiet breaths."),
        ],
        last=(S.star_badge, "You finished Ninja Training!"),
        certificate=True,
    ),
    dict(
        file="Coloring-Book-3-Ninja-Adventures.pdf",
        num=3, name="Ninja Adventures", cover=S.home_nest,
        pages=[
            (S.village, "Kai’s village by the mountains."),
            (S.meet_sensei, "Kai bows to Sensei Owl."),
            (S.kite_day, "Kite day with Miko!"),
            (S.friends_bridge, "Friends cross the bridge together."),
            (S.storm, "A stormy night. Who said “peep”?"),
            (S.home_nest, "Home to the nest! Hooray!"),
            (S.lantern_night, "Lantern night under the moon."),
            (S.big_heart, "A true ninja has a big, kind heart."),
            (S.goodnight, "Goodnight, little ninja."),
        ],
        last=(S.empty, "Draw your own ninja adventure!"),
    ),
]


def color_header(c, book):
    c.setFillColor(INK)
    c.setFont("KidReg", 11)
    c.drawCentredString(LW / 2, LH - 34, f"{TITLE}  •  Coloring Book {book['num']}: {book['name']}")


def coloring_page(c, book, scene, caption, n):
    color_header(c, book)
    size = 540
    x, y = (LW - size) / 2, 170
    draw_scene(c, scene, x, y, size, False)
    lines = wrap(caption, "Kid", 26, LW - 90)
    yy = 128
    c.setFillColor(black)
    c.setFont("Kid", 26)
    for ln in lines:
        c.drawCentredString(LW / 2, yy, ln)
        yy -= 32
    c.setFont("KidReg", 10)
    c.drawCentredString(LW / 2, 26, str(n))
    c.showPage()


def build_coloring(book, path):
    c = canvas.Canvas(path, pagesize=(LW, LH))
    c.setTitle(f"{TITLE} - Coloring Book {book['num']}: {book['name']}")
    c.setAuthor("Ninja Books")

    # Cover (in color, so kids can see the characters' colors)
    c.setFillColor(HexColor("#fff8ec"))
    c.rect(0, 0, LW, LH, stroke=0, fill=1)
    c.setFillColor(INK)
    c.setFont("Kid", 40)
    c.drawCentredString(LW / 2, LH - 100, TITLE)
    c.setFont("Kid", 26)
    c.setFillColor(HexColor("#e8423a"))
    c.drawCentredString(LW / 2, LH - 142, f"Coloring Book {book['num']}: {book['name']}")
    draw_scene(c, book["cover"], (LW - 480) / 2, 150, 480, True)
    c.setFillColor(INK)
    c.setFont("KidReg", 16)
    c.drawCentredString(LW / 2, 100, "Big pictures for little hands • Ages 3 and up")
    c.showPage()

    # This book belongs to
    color_header(c, book)
    a = Art(c, False)
    star(a, LW / 2, 520, 160, "#ffffff")
    c.setFillColor(black)
    c.setFont("Kid", 34)
    c.drawCentredString(LW / 2, 300, "This ninja book")
    c.drawCentredString(LW / 2, 258, "belongs to:")
    c.setLineWidth(3)
    c.line(110, 175, LW - 110, 175)
    c.setFont("KidReg", 13)
    c.drawCentredString(LW / 2, 110, "Tip for grown-ups: big crayons and chunky markers work best for small hands.")
    c.showPage()

    n = 1
    for scene, caption in book["pages"]:
        coloring_page(c, book, scene, caption, n)
        n += 1
    coloring_page(c, book, *book["last"], n)
    n += 1

    if book.get("certificate"):
        color_header(c, book)
        c.setStrokeColor(black)
        c.setLineWidth(5)
        c.roundRect(40, 60, LW - 80, LH - 130, 24, stroke=1, fill=0)
        c.setLineWidth(2)
        c.roundRect(52, 72, LW - 104, LH - 154, 18, stroke=1, fill=0)
        c.setFillColor(black)
        c.setFont("Kid", 36)
        c.drawCentredString(LW / 2, LH - 150, "Ninja Promise")
        c.setFont("Kid", 22)
        c.drawCentredString(LW / 2, LH - 190, "This little ninja is:")
        a = Art(c, False)
        y = LH - 250
        for w in ("QUIET", "PATIENT", "STRONG", "KIND", "BRAVE"):
            star(a, 200, y + 10, 22, "#ffffff")
            c.setFillColor(black)
            c.setFont("Kid", 30)
            c.drawString(240, y, w)
            y -= 62
        c.setLineWidth(3)
        c.line(120, 190, LW - 120, 190)
        c.setFont("Kid", 18)
        c.drawCentredString(LW / 2, 162, "Ninja name")
        c.setFont("KidReg", 14)
        c.drawCentredString(LW / 2, 110, "Color a star each time you keep a ninja secret!")
        c.showPage()
    c.save()


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    build_story(os.path.join(OUT, "The-Way-of-the-Ninja-Story-Book.pdf"))
    for b in BOOKS:
        build_coloring(b, os.path.join(OUT, b["file"]))
    print("done ->", OUT)
