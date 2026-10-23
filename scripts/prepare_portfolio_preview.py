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

ROOT = Path(__file__).resolve().parents[1]
output = ROOT / "local" / "portfolio-preview"
output.mkdir(parents=True, exist_ok=True)
source = (ROOT / "_pages/about.md").read_text(encoding="utf-8")
metadata = yaml.safe_load(source.split("---", 2)[1])
html = (ROOT / "_layouts/portfolio.html").read_text(encoding="utf-8")
html = html.replace("{{ content }}", (ROOT / "_includes/portfolio-home.html").read_text(encoding="utf-8"))
for key in ("title", "description"):
    html = html.replace("{{ page." + key + " | escape }}", escape(metadata[key], quote=True))
html = html.replace("{{ page.url | absolute_url }}", "https://inamullah-colab.github.io/")
html = html.replace("{{ '/images/Profile_pic.jpg' | absolute_url }}", "https://inamullah-colab.github.io/images/Profile_pic.jpg")
assert not re.search(r"{{|{%", html), "Unresolved template in preview"
(output / "index.html").write_text(html, encoding="utf-8")
(output / "assets/css").mkdir(parents=True, exist_ok=True)
shutil.copy2(ROOT / "assets/css/portfolio.css", output / "assets/css/portfolio.css")
(output / "images").mkdir(exist_ok=True)
for name in ("Profile_pic.jpg", "favicon.svg"):
    shutil.copy2(ROOT / "images" / name, output / "images" / name)

# A portable copy can be opened directly without a running preview server.
portable = html.replace('<link rel="stylesheet" href="/assets/css/portfolio.css">',
                        '<style>' + (ROOT / "assets/css/portfolio.css").read_text(encoding="utf-8") + '</style>')
for name, mime in (("Profile_pic.jpg", "image/jpeg"), ("favicon.svg", "image/svg+xml")):
    data = base64.b64encode((ROOT / "images" / name).read_bytes()).decode("ascii")
    portable = portable.replace('"/images/' + name + '"', '"data:' + mime + ';base64,' + data + '"')
# Keep section navigation within the portable preview; other pages use the live domain.
portable = portable.replace('href="/#research"', 'href="#research"')
portable = re.sub(r'href="/(?!/)([^"]*)"', r'href="https://inamullah-colab.github.io/\1"', portable)
(output / "portfolio-draft.html").write_text(portable, encoding="utf-8")
print(output / "index.html")
