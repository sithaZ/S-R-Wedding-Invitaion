"""Cut the supplied invitation into lossless masters and web-ready sections.

Usage: python scripts/slice_invitation.py path/to/Wedding_invi-02.png
Requires Pillow. Coordinates refer to the original 2250 x 16698 artwork.
"""
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = [
    ("WeddingInfo", 0, 3270),
    ("WeddingPic", 3270, 10010),
    ("WeddingDetail", 10010, 13241),
    ("EventColors", 13241, 13830),
    ("Map", 13830, 15632),
    ("Footer", 15632, 16698),
]


def main():
    source = Image.open(sys.argv[1])
    if source.size != (2250, 16698):
        raise ValueError(f"Expected 2250 x 16698 artwork, received {source.size}")
    # Composite onto white if the source contains transparent pixels.
    image = Image.new("RGB", source.size, "white")
    if source.mode == "RGBA":
        image.paste(source, mask=source.getchannel("A"))
    else:
        image.paste(source.convert("RGB"))
    output = ROOT / "assets" / "images"
    manifest = []
    for name, top, bottom in SECTIONS:
        crop = image.crop((0, top, image.width, bottom))
        crop.save(output / f"{name}.png", optimize=True)
        web = crop.resize((1125, (bottom - top) // 2), Image.Resampling.LANCZOS)
        web.save(output / f"{name}.webp", quality=95, method=6)
        manifest.append({"name": name, "box": [0, top, image.width, bottom],
                         "master": f"assets/images/{name}.png",
                         "web": f"assets/images/{name}.webp",
                         "width": web.width, "height": web.height})
    (output / "invitation-sections.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("Created six lossless PNG masters and six optimized WebP sections.")


if __name__ == "__main__":
    main()
