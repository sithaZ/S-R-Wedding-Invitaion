"""Render the supplied two-page PDF into the website's image sections.

Usage: python scripts/extract_pdf_invitation.py path/to/Wedding_invi.pdf
Requires pypdfium2 and Pillow. The gray video placeholder is omitted.
"""
import json
import sys
from pathlib import Path

import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'assets' / 'images'
SECTIONS = [
    ('WeddingInfo', 1454, 3100),
    ('WeddingPic', 3100, 6460),
    ('WeddingDetail', 6460, 7888),
    ('EventColors', 7888, 8350),
    ('Map', 8350, 9270),
    ('Footer', 9270, 9802),
]


def main():
    pdf = pdfium.PdfDocument(sys.argv[1])
    if len(pdf) != 2:
        raise ValueError('Expected the supplied two-page invitation PDF.')
    cover = pdf[0].render(scale=1125 / pdf[0].get_width()).to_pil().convert('RGB')
    cover.save(OUTPUT / 'CoverImage.png', optimize=True)
    detail = pdf[1].render(scale=1125 / pdf[1].get_width()).to_pil().convert('RGB')
    if detail.size != (1125, 9802):
        raise ValueError(f'Unexpected PDF dimensions: {detail.size}')
    manifest = []
    for name, top, bottom in SECTIONS:
        crop = detail.crop((0, top, 1125, bottom))
        crop.save(OUTPUT / f'{name}.png', optimize=True)
        crop.save(OUTPUT / f'{name}.webp', quality=95, method=6)
        manifest.append({'name': name, 'source': 'Wedding_invi.pdf, page 2',
                         'box': [0, top, 1125, bottom],
                         'master': f'assets/images/{name}.png',
                         'web': f'assets/images/{name}.webp',
                         'width': 1125, 'height': bottom - top})
    (OUTPUT / 'invitation-sections.json').write_text(
        json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(f'PDF cover: {cover.size}; six invitation sections saved.')


if __name__ == '__main__':
    main()
