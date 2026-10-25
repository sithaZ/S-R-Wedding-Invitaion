# Somaly & Monyroath wedding invitation

Open `index.html` for the cover; its button opens `invitation.html`. No build is required. Keep both HTML files and the `assets` directory together when hosting.

## Current layout

The supplied `Wedding_invi.pdf` is the current artwork source. Page 1 provides the cover. Its button artwork is separated into a transparent image so the visible button and clickable area bounce together. No extra background is added behind the cover.

The second page starts with `assets/video/save-the-date.mp4` in place of the PDF's gray placeholder. The original video is 1080 x 1920 and is displayed at its natural aspect ratio so nothing is cropped or stretched. This makes the video section taller than the PDF's placeholder. The video attempts muted, inline autoplay and loops continuously. Native controls remain available.

The remaining content follows the PDF in order:

| Asset in `assets/images/` | Content |
| --- | --- |
| `CoverImage.png` | PDF cover background; button displayed separately |
| `WeddingInfo.webp` | Families, invitation, date, and venue |
| `WeddingPic.webp` | Complete photo collage |
| `WeddingDetail.webp` | Khmer ceremony schedule |
| `EventColors.webp` | Dress colors |
| `Map.webp` | Venue map background; button displayed separately |
| `Footer.webp` | With Love, Somaly & Monyroath |

Only the printed location button below the map links to the existing Google Maps venue search. The map and surrounding artwork are not clickable. PNG versions of the six content sections are lossless crops of the PDF rendering. `invitation-sections.json` records their coordinates and dimensions. `OpenButton.png` and `LocationButton.png` contain the separate button artwork. Both buttons use a repeating double bounce and gold glow, with hover and press feedback; reduced-motion settings disable the bounce.

## Audio

The video loops silently: its mute state and zero volume are enforced during playback and volume changes. The supplied `assets/audio/blue.mp3` is the only soundtrack. Music loops from 0:03 to 0:58 continuously, giving a 55-second segment. The video is only 9.2092 seconds long, so its silent loop runs from 0:03 to the end. Both use segment looping that respects pause and playback rate. There is no floating music icon. Music attempts to start when the invitation opens; if blocked, the first tap or keypress starts it. No reading timer is configured.

## Recreate artwork

With Pillow and pypdfium2 installed:

```text
python scripts/extract_pdf_invitation.py path/to/Wedding_invi.pdf
python scripts/separate_buttons.py path/to/Wedding_invi.pdf
```

`scripts/slice_invitation.py` is the earlier PNG-based workflow and would restore the earlier artwork. Use the PDF script for the current layout.

## Verification

Checked both pages' local links, asset paths, and image dimensions. Verified the PDF section boundaries and visually inspected the rendered artwork; the button graphics are now separate from their cover/map backgrounds. The MP4 copy matches the supplied file byte for byte and contains H.264/AAC track markers. The video is configured for muted, looping autoplay, and the background music points to the supplied `blue.mp3` file.

Browser preview permission was previously declined. Actual browser layout, video decoding/playback, and audio playback remain unverified.
