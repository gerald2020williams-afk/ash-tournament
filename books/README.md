# Little Ninja books (ages 3+)

Three picture books about Kai the little ninja, his best friend Miko, wise Sensei Owl and Pip the cat, each with matching coloring books.

| Folder | Story book | Coloring book(s) |
|---|---|---|
| `1-The-Way-of-the-Ninja/` | *The Way of the Ninja*: Kai learns the five ninja secrets (quiet, patient, strong, kind, brave) | Book 1: Meet the Ninjas • Book 2: Ninja Training • Book 3: Ninja Adventures |
| `2-Little-Ninja-and-the-Dark-Night/` | *Little Ninja and the Dark Night*: a bedtime story where Kai learns the dark is full of friends | Little Ninja and the Dark Night Coloring Book |
| `3-The-Ninja-Team/` | *The Ninja Team*: Kai and Miko learn teamwork and sharing with a giant peach | The Ninja Team Coloring Book |

Story books are 8.5" x 8.5" in full color. Coloring books are US Letter pages that print at home. Each one has a color cover, a "This book belongs to" page, big thick-lined pictures with one short sentence each, and a "draw your own" page. Most also end with a certificate the child can color in.

The illustrations are drawn in code, so every book uses the same characters. To change the text or page order, edit `source/build.py`. To change pictures, edit `source/scenes.py` (story 1) or `source/scenes2.py` (stories 2 and 3). Then run:

```
python3 books/source/build.py
```

Requires Python 3 with `reportlab` and the DejaVu fonts.
