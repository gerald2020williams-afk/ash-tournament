"""Builds the Little Ninja story books and their coloring books as printable PDFs.

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
import scenes2 as S2  # noqa: E402

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pdfmetrics.registerFont(TTFont("Kid", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("KidReg", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))

INK = HexColor(INK_COLOR)
CREAM = HexColor("#fff8ec")
RAINBOW = ["#ffd84a", "#7ed0f5", "#9ad46b", "#f58fb0", "#ffa94d"]


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


def cream_page(c, w, h):
    c.setFillColor(CREAM)
    c.rect(0, 0, w, h, stroke=0, fill=1)


# =====================================================================
# Stories
# =====================================================================
STORY1 = dict(
    folder="1-The-Way-of-the-Ninja",
    file="The-Way-of-the-Ninja-Story-Book.pdf",
    title="The Way of the Ninja",
    cover_lines=("The Way of", "the Ninja"),
    tagline="A story about being quiet, patient, strong, kind and brave",
    cover=S.cover,
    dedication="For brave little ninjas, ages 3 and up",
    pages=[
        (S.village, "In a little village by the big mountains lived a little ninja named Kai."),
        (S.meet_sensei, "Kai wanted to be a GREAT ninja. So Kai bowed to Sensei Owl and asked, “Will you teach me?”"),
        (S.five_secrets, "“The Way of the Ninja has five secrets,” said Sensei Owl. “Let’s learn them one by one.”"),
        (S.quiet, "Secret number one: Be QUIET.\nKai tiptoed past sleepy Pip. Tip… tip… toe. Shhh!"),
        (S.patient, "Secret number two: Be PATIENT.\nKai sat very still. Breathe in… breathe out. Slow, like a turtle."),
        (S.strong, "Secret number three: Be STRONG.\nKai stood on one foot like a crane. Miko practiced her kicks. Hi-YA!"),
        (S.kind, "Secret number four: Be KIND.\nOh no! Pip was stuck up in a tree. Kai reached up and helped Pip down."),
        (S.brave, "Secret number five: Be BRAVE.\nThe bridge was wobbly. Kai felt scared… but took one step, then another!"),
        (S.storm, "One stormy night, Kai heard a tiny “peep!” A little bird was lost. Kai stayed calm and held up a light."),
        (S.home_nest, "Kai gently carried the bird home to its nest. “Hooray!” cheered Miko. The bird family sang a happy song."),
        (S.big_heart, "“You found the Way of the Ninja,” said Sensei Owl. “A true ninja has a BIG, kind heart.”"),
        (S.goodnight, "Goodnight, little ninja. Goodnight, Pip. Tomorrow, the Ninja Way begins again."),
    ],
    list_page=dict(
        title="The Ninja Promise", sub="Say it out loud with a grown-up!",
        items=["I am QUIET.", "I am PATIENT.", "I am STRONG.", "I am KIND.", "I am BRAVE."],
        footer="I am a NINJA!", size=30,
    ),
    end=S.big_heart,
)

STORY2 = dict(
    folder="2-Little-Ninja-and-the-Dark-Night",
    file="Little-Ninja-and-the-Dark-Night-Story-Book.pdf",
    title="Little Ninja and the Dark Night",
    cover_lines=("Little Ninja and", "the Dark Night"),
    tagline="A bedtime story about finding friends in the dark",
    cover=S2.d_cover,
    dedication="For little ninjas who are learning to love the night",
    pages=[
        (S2.d_bedtime, "When the sun went down, it was time for bed. Kai snuggled under the blanket. But Kai could not sleep."),
        (S2.d_dark, "The room was very dark. “Creak!” went the floor. “Whoosh!” went the wind. Kai peeked out from the covers."),
        (S2.d_shadow, "On the wall was a BIG shadow with pointy ears! “Who… who is there?” Kai whispered."),
        (S2.d_only_pip, "“Meow!” It was only Pip, sitting by the lamp! Kai laughed and laughed. “Silly Pip!”"),
        (S2.d_owl_window, "“Tap, tap, tap.” Sensei Owl was at the window. “Come, little ninja. Let’s go and meet the night.”"),
        (S2.d_moon, "Outside, the moon was big and round. “The moon is a night-light for the whole world,” said Sensei Owl."),
        (S2.d_frogs, "“Ribbit! Ribbit!” The frogs were singing a night song by the pond. Kai listened very quietly."),
        (S2.d_fireflies, "Tiny lights danced in the grass. “Fireflies!” said Kai. “They look like little stars!”"),
        (S2.d_stars, "Kai and Sensei Owl counted the stars. One, two, three… so many stars!"),
        (S2.d_friends, "“The dark is not scary,” said Kai. “The dark is full of friends!”"),
        (S2.d_sleep, "Back in bed, Kai gave a big ninja yawn. Goodnight, moon. Goodnight, stars. Goodnight, little ninja."),
    ],
    list_page=dict(
        title="Night Ninja Tricks", sub="For when the dark feels a little scary",
        items=["Take a big ninja breath.", "Hug your favorite toy.", "Look for the moon.",
               "Listen for night sounds.", "Say: “The dark is full of friends!”"],
        footer="Sweet dreams, little ninja!", size=22,
    ),
    end=S2.d_sleep,
)

STORY3 = dict(
    folder="3-The-Ninja-Team",
    file="The-Ninja-Team-Story-Book.pdf",
    title="The Ninja Team",
    cover_lines=("The Ninja", "Team"),
    tagline="A story about teamwork and sharing",
    cover=S2.t_cover,
    dedication="For little ninjas and all their friends",
    pages=[
        (S2.t_challenge, "One sunny morning, Sensei Owl had a special ninja challenge for Kai and Miko."),
        (S2.t_hill, "“At the top of the hill is the biggest peach in the land. Bring it down to the picnic!”"),
        (S2.t_kai_push, "“I will do it all by MYSELF!” said Kai. He pushed and pushed. But the peach did not move."),
        (S2.t_miko_pull, "“No, I will do it all by MYSELF!” said Miko. She pulled and pulled. But the peach did not move."),
        (S2.t_grumpy, "Kai and Miko felt grumpy. They sat down back to back. Hmph!"),
        (S2.t_pip_idea, "Then Pip gave the peach a tiny push with a tiny paw. Kai and Miko looked at each other…"),
        (S2.t_team_push, "“Let’s be a ninja TEAM!” said Kai. “One, two, three… PUSH!”"),
        (S2.t_rolling, "The big peach rolled down, down, down the hill!"),
        (S2.t_picnic, "It landed right on the picnic blanket. PLOP! “Hooray!” everyone cheered."),
        (S2.t_share, "Kai and Miko shared the peach with all their friends. Sharing made it taste extra sweet!"),
        (S2.t_team, "“One ninja is strong,” said Sensei Owl. “But a ninja TEAM is even stronger!”"),
    ],
    list_page=dict(
        title="The Ninja Team Cheer", sub="Say it together with a friend!",
        items=["We help each other.", "We take turns.", "We share.", "We say thank you.", "We are a TEAM!"],
        footer="Together we are STRONGER!", size=26,
    ),
    end=S2.t_team,
)

STORIES = [STORY1, STORY2, STORY3]


def build_story(st, path):
    W = 8.5 * inch
    c = canvas.Canvas(path, pagesize=(W, W))
    c.setTitle(st["title"])
    c.setAuthor("Little Ninja Books")

    # Cover
    draw_scene(c, st["cover"], 0, 0, W, True, frame=False, radius=0)
    l1, l2 = st["cover_lines"]
    size = 54
    while max(pdfmetrics.stringWidth(l, "Kid", size) for l in (l1, l2)) > W - 60:
        size -= 2
    c.setFont("Kid", size)
    for line, y in ((l1, 530), (l2, 530 - size * 1.15)):
        c.setFillColor(HexColor("#120d24"))
        c.drawCentredString(W / 2 + 3, y - 3, line)
        c.setFillColor(HexColor("#ffd84a"))
        c.drawCentredString(W / 2, y, line)
    c.setFont("Kid", 15)
    c.setFillColor(white)
    c.drawCentredString(W / 2, 530 - size * 1.15 - 36, st["tagline"])
    c.showPage()

    # Title page
    cream_page(c, W, W)
    a = Art(c, True)
    for i, (x, y) in enumerate([(206, 300), (256, 330), (306, 345), (356, 330), (406, 300)]):
        star(a, x, y, 24, RAINBOW[i])
    c.setFillColor(INK)
    tsize = 40
    while pdfmetrics.stringWidth(st["title"], "Kid", tsize) > W - 60:
        tsize -= 2
    c.setFont("Kid", tsize)
    c.drawCentredString(W / 2, 420, st["title"])
    c.setFont("KidReg", 18)
    c.drawCentredString(W / 2, 240, st["dedication"])
    c.showPage()

    for scene, text in st["pages"]:
        draw_scene(c, scene, 0, 0, W, True, frame=False, radius=0)
        text_panel(c, text, 40, W - 30, W - 80)
        c.showPage()

    # List page (promise / tricks / cheer)
    lp = st["list_page"]
    cream_page(c, W, W)
    c.setFillColor(INK)
    c.setFont("Kid", 34)
    c.drawCentredString(W / 2, 535, lp["title"])
    c.setFont("KidReg", 15)
    c.drawCentredString(W / 2, 505, lp["sub"])
    a = Art(c, True)
    longest = max(pdfmetrics.stringWidth(t, "Kid", lp["size"]) for t in lp["items"])
    x0 = (W - longest - 50) / 2
    y = 440
    for words, col in zip(lp["items"], RAINBOW):
        star(a, x0 + 10, y + lp["size"] * 0.35, 22, col)
        c.setFillColor(INK)
        c.setFont("Kid", lp["size"])
        c.drawString(x0 + 50, y, words)
        y -= 66
    c.setFont("Kid", 32)
    c.setFillColor(HexColor("#e8423a"))
    c.drawCentredString(W / 2, 80, lp["footer"])
    c.showPage()

    # The End
    draw_scene(c, st["end"], 0, 0, W, True, frame=False, radius=0)
    text_panel(c, "The End", W / 2 - 130, W - 60, 260, size=40)
    c.showPage()
    c.save()


# =====================================================================
# Coloring books (US Letter, portrait)
# =====================================================================
LW, LH = 8.5 * inch, 11 * inch

COLORING = [
    dict(
        story=STORY1, file="Coloring-Book-1-Meet-the-Ninjas.pdf",
        name="Coloring Book 1: Meet the Ninjas", cover=S.friends,
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
        story=STORY1, file="Coloring-Book-2-Ninja-Training.pdf",
        name="Coloring Book 2: Ninja Training", cover=S.strong,
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
        certificate=dict(title="Ninja Promise", intro="This little ninja is:",
                         items=["QUIET", "PATIENT", "STRONG", "KIND", "BRAVE"],
                         names=["Ninja name"],
                         tip="Color a star each time you keep a ninja secret!"),
    ),
    dict(
        story=STORY1, file="Coloring-Book-3-Ninja-Adventures.pdf",
        name="Coloring Book 3: Ninja Adventures", cover=S.home_nest,
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
    dict(
        story=STORY2, file="Little-Ninja-and-the-Dark-Night-Coloring-Book.pdf",
        name="Coloring Book", cover=S2.d_friends,
        pages=[
            (S2.d_bedtime, "Bedtime for Kai."),
            (S2.d_shadow, "A big shadow on the wall!"),
            (S2.d_only_pip, "It was only Pip! Meow!"),
            (S2.d_owl_window, "Sensei Owl taps on the window."),
            (S2.d_moon_face, "Hello, moon! Our night-light."),
            (S2.d_moon, "A night walk with Sensei Owl."),
            (S2.d_frogs, "Ribbit! The frogs sing a night song."),
            (S2.d_big_frog, "Color the happy frog."),
            (S2.d_fireflies, "Fireflies dance in the grass."),
            (S2.d_big_fireflies, "Glow, little firefly, glow!"),
            (S2.d_stars, "Count the stars: one, two, three…"),
            (S2.d_friends, "The dark is full of friends!"),
            (S2.d_sleep, "Goodnight, little ninja."),
        ],
        last=(S2.d_draw_window, "Draw what YOU see out your window at night!"),
        certificate=dict(title="Night Ninja", intro="This brave night ninja can:",
                         items=["BREATHE BIG", "HUG A TOY", "FIND THE MOON", "LISTEN", "SLEEP TIGHT"],
                         names=["Night ninja name"],
                         tip="Color a star each night you try a night ninja trick!"),
    ),
    dict(
        story=STORY3, file="The-Ninja-Team-Coloring-Book.pdf",
        name="Coloring Book", cover=S2.t_team_push,
        pages=[
            (S2.t_challenge, "Sensei Owl has a challenge!"),
            (S2.t_hill, "The biggest peach is on top of the hill."),
            (S2.t_big_peach, "Color the giant peach!"),
            (S2.t_kai_push, "Kai pushes all by himself. Huff!"),
            (S2.t_miko_pull, "Miko pulls all by herself. Ugh!"),
            (S2.t_grumpy, "Grumpy ninjas. Hmph!"),
            (S2.t_pip_idea, "Pip has an idea!"),
            (S2.t_team_push, "Together: one, two, three, PUSH!"),
            (S2.t_rolling, "Roll, roll, roll down the hill!"),
            (S2.t_picnic, "PLOP! Right on the picnic blanket."),
            (S2.t_picnic_basket, "What is in the picnic basket?"),
            (S2.t_share, "Sharing is extra sweet."),
            (S2.t_high_five, "Ninja team high five!"),
            (S2.t_team, "Together we are stronger!"),
        ],
        last=(S.empty, "Draw YOUR ninja team!"),
        certificate=dict(title="Ninja Team", intro="This ninja team can:",
                         items=["HELP", "TAKE TURNS", "SHARE", "SAY THANK YOU", "WORK TOGETHER"],
                         names=["Ninja", "Ninja"],
                         tip="Color a star each time you work as a team!"),
    ),
]


def color_header(c, book):
    c.setFillColor(INK)
    c.setFont("KidReg", 11)
    c.drawCentredString(LW / 2, LH - 34, f"{book['story']['title']}  •  {book['name']}")


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


def certificate_page(c, book):
    cert = book["certificate"]
    color_header(c, book)
    c.setStrokeColor(black)
    c.setLineWidth(5)
    c.roundRect(40, 60, LW - 80, LH - 130, 24, stroke=1, fill=0)
    c.setLineWidth(2)
    c.roundRect(52, 72, LW - 104, LH - 154, 18, stroke=1, fill=0)
    c.setFillColor(black)
    c.setFont("Kid", 36)
    c.drawCentredString(LW / 2, LH - 150, cert["title"])
    c.setFont("Kid", 22)
    c.drawCentredString(LW / 2, LH - 190, cert["intro"])
    a = Art(c, False)
    longest = max(pdfmetrics.stringWidth(t, "Kid", 28) for t in cert["items"])
    x0 = (LW - longest - 50) / 2
    y = LH - 250
    for w in cert["items"]:
        star(a, x0 + 10, y + 10, 22, "#ffffff")
        c.setFillColor(black)
        c.setFont("Kid", 28)
        c.drawString(x0 + 50, y, w)
        y -= 60
    names = cert["names"]
    c.setLineWidth(3)
    if len(names) == 1:
        slots = [(120, LW - 120)]
    else:
        slots = [(90, LW / 2 - 20), (LW / 2 + 20, LW - 90)]
    for (xa, xb), label in zip(slots, names):
        c.line(xa, 190, xb, 190)
        c.setFont("Kid", 18)
        c.drawCentredString((xa + xb) / 2, 162, label)
    c.setFont("KidReg", 14)
    c.drawCentredString(LW / 2, 110, cert["tip"])
    c.showPage()


def build_coloring(book, path):
    st = book["story"]
    c = canvas.Canvas(path, pagesize=(LW, LH))
    c.setTitle(f"{st['title']} - {book['name']}")
    c.setAuthor("Little Ninja Books")

    # Cover (in color, so kids can see the characters' colors)
    cream_page(c, LW, LH)
    c.setFillColor(INK)
    tsize = 40
    while pdfmetrics.stringWidth(st["title"], "Kid", tsize) > LW - 60:
        tsize -= 2
    c.setFont("Kid", tsize)
    c.drawCentredString(LW / 2, LH - 100, st["title"])
    c.setFont("Kid", 26)
    c.setFillColor(HexColor("#e8423a"))
    c.drawCentredString(LW / 2, LH - 142, book["name"])
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
    for scene, caption in book["pages"] + [book["last"]]:
        coloring_page(c, book, scene, caption, n)
        n += 1
    if book.get("certificate"):
        certificate_page(c, book)
    c.save()


if __name__ == "__main__":
    for st in STORIES:
        d = os.path.join(OUT, st["folder"])
        os.makedirs(d, exist_ok=True)
        build_story(st, os.path.join(d, st["file"]))
    for b in COLORING:
        build_coloring(b, os.path.join(OUT, b["story"]["folder"], b["file"]))
    print("done ->", OUT)
