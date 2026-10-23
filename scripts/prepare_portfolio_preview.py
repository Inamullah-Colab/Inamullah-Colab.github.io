"""Create an isolated static homepage preview without requiring Ruby/Jekyll.

This previews the portfolio layout only; use Jekyll to validate the complete site.
Run from the repository root, then serve local/portfolio-preview.
"""
from pathlib import Path
from html import escape
import base64
import re
import shutil
import yaml
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
output = ROOT / "local" / "portfolio-preview"
output.mkdir(parents=True, exist_ok=True)
source = (ROOT / "_pages/about.md").read_text(encoding="utf-8")
metadata = yaml.safe_load(source.split("---", 2)[1])
html = (ROOT / "_layouts/portfolio.html").read_text(encoding="utf-8")
html = html.replace("{{ content }}", (ROOT / "_includes/portfolio-home.html").read_text(encoding="utf-8"))
news = (ROOT / "_includes/portfolio-news.html").read_text(encoding="utf-8")
news = re.sub(r'{% assign news_items = .*? %}', '', news)
loop = re.search(r'{% for item in news_items limit:4 %}(.*?){% endfor %}', news, re.S)
items = sorted(yaml.safe_load((ROOT / "_data/news.yml").read_text(encoding="utf-8")), key=lambda item: str(item['date']), reverse=True)[:4]
rows = []
for item in items:
    row = loop.group(1)
    row = row.replace('{{ item.date | date: "%d %b %Y" }}', date.fromisoformat(str(item['date'])).strftime('%d %b %Y'))
    for key, value in item.items():
        row = row.replace('{{ item.' + key + ' | escape }}', escape(str(value), quote=True))
        row = row.replace('{{ item.' + key + ' }}', escape(str(value), quote=True))
    rows.append(row)
news = news[:loop.start()] + ''.join(rows) + news[loop.end():]
html = html.replace('{% include portfolio-news.html %}', news)
for key in ("title", "description"):
    html = html.replace("{{ page." + key + " | escape }}", escape(metadata[key], quote=True))
html = html.replace("{{ page.url | absolute_url }}", "https://inamullah-colab.github.io/")
html = html.replace("{{ '/images/Profile_pic.jpg' | absolute_url }}", "https://inamullah-colab.github.io/images/Profile_pic.jpg")
assert not re.search(r"{{|{%", html), "Unresolved template in preview"
(output / "index.html").write_text(html, encoding="utf-8")
(output / "assets/css").mkdir(parents=True, exist_ok=True)
for name in ("portfolio.css",):
    shutil.copy2(ROOT / "assets/css" / name, output / "assets/css" / name)
(output / "images").mkdir(exist_ok=True)
for name in ("Profile_pic.jpg", "favicon.svg"):
    shutil.copy2(ROOT / "images" / name, output / "images" / name)

# A portable copy can be opened directly without a running preview server.
portable = html
for name in ("portfolio.css",):
    portable = portable.replace('<link rel="stylesheet" href="/assets/css/' + name + '">',
                                '<style>' + (ROOT / "assets/css" / name).read_text(encoding="utf-8") + '</style>')
for name, mime in (("Profile_pic.jpg", "image/jpeg"), ("favicon.svg", "image/svg+xml")):
    data = base64.b64encode((ROOT / "images" / name).read_bytes()).decode("ascii")
    portable = portable.replace('"/images/' + name + '"', '"data:' + mime + ';base64,' + data + '"')
# Keep section navigation within the portable preview; other pages use the live domain.
portable = re.sub(r'href="/#([^"]+)"', r'href="#\1"', portable)
portable = re.sub(r'href="/(?!/)([^"]*)"', r'href="https://inamullah-colab.github.io/\1"', portable)
(output / "portfolio-draft.html").write_text(portable, encoding="utf-8")
print(output / "index.html")
