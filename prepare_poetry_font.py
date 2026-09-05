import html
import re
import sys
from pathlib import Path
from urllib.request import urlretrieve

from fontTools import subset
from fontTools.ttLib import TTFont


if len(sys.argv) != 2:
    raise SystemExit("Usage: python prepare_poetry_font.py <site-directory>")

site = Path(sys.argv[1]).resolve()

if not site.exists():
    raise SystemExit(f"Site directory does not exist: {site}")

# ------------------------------------------------------------
# 修正文中的已知错字
# ------------------------------------------------------------

page = site / "chapter-1.html"

old_text = '据考证，现代意义上的“遥感”一次'
new_text = '据考证，现代意义上的“遥感”一词'

source = page.read_text(encoding="utf-8")

count = source.count(old_text)

if count == 1:
    page.write_text(
        source.replace(old_text, new_text, 1),
        encoding="utf-8"
    )
    print("Corrected typo in chapter-1.html: 一次 -> 一词")
elif count == 0:
    print("Typo text not found in chapter-1.html; no replacement made.")
else:
    raise SystemExit(
        f"Found {count} matching passages in chapter-1.html; "
        "refusing automatic replacement."
    )

# ------------------------------------------------------------
# 1. 找出所有 class="poetry" 中实际使用的文字
# ------------------------------------------------------------

span_pattern = re.compile(
    r"<span\b([^>]*)>(.*?)</span>",
    re.IGNORECASE | re.DOTALL,
)

class_pattern = re.compile(
    r'class\s*=\s*["\']([^"\']*)["\']',
    re.IGNORECASE,
)

tag_pattern = re.compile(r"<[^>]+>")

characters = set()
poetry_spans = 0

for page in site.rglob("*.html"):
    source = page.read_text(encoding="utf-8")

    for attrs, content in span_pattern.findall(source):
        class_match = class_pattern.search(attrs)

        if not class_match:
            continue

        classes = class_match.group(1).split()

        if "poetry" not in classes:
            continue

        poetry_spans += 1

        text = tag_pattern.sub("", content)
        text = html.unescape(text)

        for char in text:
            if not char.isspace():
                characters.add(char)


if not characters:
    raise SystemExit(
        'No text with class="poetry" was found. '
        "The font was not generated."
    )

print(f"Found {poetry_spans} poetry spans.")
print(f"Found {len(characters)} unique poetry characters.")


# ------------------------------------------------------------
# 2. 下载霞鹜文楷 Lite 官方 TTF
# ------------------------------------------------------------

font_dir = site / "assets" / "fonts"
font_dir.mkdir(parents=True, exist_ok=True)

source_ttf = Path("/tmp/LXGWWenKaiLite-Regular.ttf")

font_url = (
    "https://raw.githubusercontent.com/"
    "lxgw/LxgwWenKai-Lite/main/fonts/TTF/"
    "LXGWWenKaiLite-Regular.ttf"
)

license_url = (
    "https://raw.githubusercontent.com/"
    "lxgw/LxgwWenKai-Lite/main/OFL.txt"
)

print("Downloading LXGW WenKai Lite...")
urlretrieve(font_url, source_ttf)

license_path = font_dir / "OFL-LXGW-WenKai-Lite.txt"
urlretrieve(license_url, license_path)


# ------------------------------------------------------------
# 3. 只保留诗句实际出现的字符，并转换成 WOFF2
# ------------------------------------------------------------

output_font = font_dir / "poetry-kai.woff2"

font = TTFont(str(source_ttf))

options = subset.Options()
options.layout_features = ["*"]

subsetter = subset.Subsetter(options=options)
subsetter.populate(text="".join(sorted(characters)))
subsetter.subset(font)

font.flavor = "woff2"
font.save(str(output_font))

print(
    f"Generated {output_font.name}: "
    f"{output_font.stat().st_size / 1024:.1f} KB"
)


# ------------------------------------------------------------
# 4. 强制所有 .poetry 文字使用这个网页字体
# ------------------------------------------------------------

css_path = site / "assets" / "style.css"

if not css_path.exists():
    raise SystemExit(f"CSS file not found: {css_path}")

extra_css = r'''

/* Self-hosted poetry font */
@font-face {
    font-family: "PoetryKaiWeb";
    src: url("./fonts/poetry-kai.woff2?v=3") format("woff2");
    font-style: normal;
    font-weight: 400;
    font-display: swap;
}

.poetry,
.poetry * {
    font-family: "PoetryKaiWeb", serif !important;
    font-style: normal;
}

'''

with css_path.open("a", encoding="utf-8") as f:
    f.write(extra_css)

print("Poetry web font CSS added successfully.")
