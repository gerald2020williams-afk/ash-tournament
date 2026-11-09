# The Way of the Ninja: book set (ages 3+)

| File | What it is |
|---|---|
| `The-Way-of-the-Ninja-Story-Book.pdf` | 16-page color picture book (8.5" x 8.5") |
| `Coloring-Book-1-Meet-the-Ninjas.pdf` | Coloring pages of Kai, Miko, Sensei Owl, Pip and their world |
| `Coloring-Book-2-Ninja-Training.pdf` | The five ninja secrets: quiet, patient, strong, kind, brave (ends with a Ninja Promise certificate) |
| `Coloring-Book-3-Ninja-Adventures.pdf` | Scenes from the story: the storm, the lost bird, kite day, lantern night |

The coloring books are US Letter pages that print at home. Each one has a color cover, a "This book belongs to" page, and big, thick-lined pictures with one short sentence under each.

The illustrations are drawn in code, so the story book and the coloring books use the same characters. To change text or pictures, edit `source/build.py` (text and page order) or `source/scenes.py` (pictures), then run:

```
python3 books/source/build.py
```

Requires Python 3 with `reportlab` and the DejaVu fonts.
