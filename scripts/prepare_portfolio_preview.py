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
for name in ("story-path.html", "research-lens.html"):
    html = html.replace("{% include " + name + " %}", (ROOT / "_includes" / name).read_text(encoding="utf-8"))
for key in ("title", "description"):
    html = html.replace("{{ page." + key + " | escape }}", escape(metadata[key], quote=True))
html = html.replace("{{ page.url | absolute_url }}", "https://inamullah-colab.github.io/")
html = html.replace("{{ '/images/Profile_pic.jpg' | absolute_url }}", "https://inamullah-colab.github.io/images/Profile_pic.jpg")
assert not re.search(r"{{|{%", html), "Unresolved template in preview"
(output / "index.html").write_text(html, encoding="utf-8")
(output / "assets/css").mkdir(parents=True, exist_ok=True)
for name in ("portfolio.css", "research-visuals.css"):
    shutil.copy2(ROOT / "assets/css" / name, output / "assets/css" / name)
(output / "images").mkdir(exist_ok=True)
for name in ("Profile_pic.jpg", "favicon.svg"):
    shutil.copy2(ROOT / "images" / name, output / "images" / name)
shutil.copytree(ROOT / "images/icons", output / "images/icons", dirs_exist_ok=True)

# A portable copy can be opened directly without a running preview server.
portable = html
for name in ("portfolio.css", "research-visuals.css"):
    portable = portable.replace('<link rel="stylesheet" href="/assets/css/' + name + '">',
                                '<style>' + (ROOT / "assets/css" / name).read_text(encoding="utf-8") + '</style>')
for name, mime in (("Profile_pic.jpg", "image/jpeg"), ("favicon.svg", "image/svg+xml")):
    data = base64.b64encode((ROOT / "images" / name).read_bytes()).decode("ascii")
    portable = portable.replace('"/images/' + name + '"', '"data:' + mime + ';base64,' + data + '"')
for icon in (ROOT / "images/icons").glob("*.svg"):
    data = base64.b64encode(icon.read_bytes()).decode("ascii")
    portable = portable.replace('"/images/icons/' + icon.name + '"', '"data:image/svg+xml;base64,' + data + '"')
# Keep section navigation within the portable preview; other pages use the live domain.
portable = portable.replace('href="/#research"', 'href="#research"')
portable = re.sub(r'href="/(?!/)([^"]*)"', r'href="https://inamullah-colab.github.io/\1"', portable)
(output / "portfolio-draft.html").write_text(portable, encoding="utf-8")
print(output / "index.html")
