"""Package text pages for Read the Docs without replacing the image archives."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"


def main() -> None:
    pages = sorted(SITE.glob("*.html"))
    if not pages or not (SITE / "chen-preface.html").is_file():
        raise RuntimeError("Run generate_site.py before packaging the pages")
    files = pages + [SITE / "assets" / "style.css", SITE / "assets" / "site.js"]
    output = ROOT / "site-pages.zip"
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for file in files:
            archive.write(file, file.relative_to(ROOT).as_posix())
    print(f"{output}: {len(files)} files, {output.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
