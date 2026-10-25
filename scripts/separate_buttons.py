"""Separate PDF button graphics from their backgrounds for CSS animation.

Usage: python scripts/separate_buttons.py path/to/Wedding_invi.pdf
Run after extract_pdf_invitation.py. Requires pypdf, pypdfium2 and Pillow.
"""
from io import BytesIO
from pathlib import Path
import sys

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ContentStream, NameObject
import pypdfium2 as pdfium
from PIL import Image, ImageChops, ImageDraw

OUT = Path(__file__).resolve().parents[1] / 'assets' / 'images'


def main():
    reader = PdfReader(sys.argv[1])
    for index, first, last, name, top, bottom in [
        (0, '/Fm1', '/Fm4', 'OpenButton', 0, 2079),
        (1, '/Fm9', '/Fm12', 'LocationButton', 8350, 9270),
    ]:
        page = reader.pages[index]
        ops = page.get_contents().operations
        stack = []
        for i, (args, op) in enumerate(ops):
            if op == b'q':
                stack.append(i)
            if op == b'Do' and str(args[0]) == first:
                start = stack[0]
            if op == b'Do' and str(args[0]) == last:
                end = i + 2
                break
            if op == b'Q':
                stack.pop()
        block = ops[start:end]
        balance = sum(1 if op == b'q' else -1 if op == b'Q' else 0 for _, op in block)

        def render(selected, transparent=False):
            writer = PdfWriter()
            clone = writer.add_page(page)
            stream = ContentStream(None, writer)
            stream.operations = selected
            clone[NameObject('/Contents')] = writer._add_object(stream)
            buffer = BytesIO()
            writer.write(buffer)
            pdf = pdfium.PdfDocument(buffer.getvalue())
            return pdf[0].render(scale=1125 / float(page.mediabox.width),
                fill_color=(0, 0, 0, 0) if transparent else (255, 255, 255, 255)).to_pil()

        button = render(block + [([], b'Q')] * balance, True)
        bounds = button.getbbox()
        # Keep the physical pill; its large PDF shadow is replaced by CSS.
        size = (470, 155) if index == 0 else (326, 108)
        pill = button.crop(bounds).crop((0, 0, *size)).convert('RGBA')
        mask = Image.new('L', size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1),
                                               radius=size[1] / 2, fill=255)
        pill.putalpha(ImageChops.darker(pill.getchannel('A'), mask))
        pill.save(OUT / f'{name}.png')
        base = render(ops[:start] + [([], b'q')] * balance + ops[end:]).convert('RGB')
        base = base.crop((0, top, 1125, bottom))
        base_name = 'CoverImage' if index == 0 else 'Map'
        base.save(OUT / f'{base_name}.png', optimize=True)
        if index == 1:
            base.save(OUT / 'Map.webp', quality=95, method=6)
        print(name, bounds)


if __name__ == '__main__':
    main()
