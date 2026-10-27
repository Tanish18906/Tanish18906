"""Build a small looping GIF for the GitHub profile README.

This is intentionally rendered to raster frames: GIF animation works in GitHub
README images without CSS, JavaScript, or hosted animation services.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "build-loop.gif"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W, H = 1000, 132
INK = (22, 22, 22)
CREAM = (247, 245, 238)
YELLOW = (250, 204, 0)
WHITE = (255, 255, 255)


def create() -> None:
    bold = ImageFont.truetype(FONT, 30)
    label = ImageFont.truetype(FONT, 14)
    small = ImageFont.truetype(FONT, 12)
    words = ["AI WORKFLOWS", "WEB APPS", "SECURITY TOOLS", "GAME DESIGN"]

    # The repeated strip loops perfectly across the last and first frame.
    token_widths = [int(ImageDraw.Draw(Image.new("RGB", (1, 1))).textbbox(
        (0, 0), word, font=bold)[2]) + 84 for word in words]
    track_width = sum(token_widths)
    frames = []

    for i in range(28):
        canvas = Image.new("RGB", (W, H), CREAM)
        d = ImageDraw.Draw(canvas)
        d.rectangle((0, 0, W - 1, H - 1), outline=INK, width=3)
        d.rectangle((0, 0, 247, H - 1), fill=INK)
        d.text((23, 20), "IN MOTION", font=bold, fill=WHITE)
        d.rectangle((23, 81, 37, 95), fill=YELLOW)
        d.text((47, 81), "TM / FIELD NOTES", font=small, fill=WHITE)

        # Clip the marquee to the content region.
        marquee = Image.new("RGB", (W - 250, H - 6), CREAM)
        md = ImageDraw.Draw(marquee)
        offset = int(track_width * i / 28)
        for repeat in range(-1, 3):
            xpos = 30 - offset + repeat * track_width
            for word, step in zip(words, token_widths):
                md.rectangle((xpos, 46, xpos + 16, 62), fill=YELLOW, outline=INK, width=1)
                md.text((xpos + 29, 35), word, font=bold, fill=INK)
                xpos += step
        canvas.paste(marquee, (250, 3))
        d = ImageDraw.Draw(canvas)
        d.line((248, 2, 248, H - 3), fill=INK, width=2)
        d.line((0, H - 3, W, H - 3), fill=INK, width=3)
        frames.append(canvas.quantize(colors=4, dither=Image.Dither.NONE))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=190,
        loop=0,
        optimize=True,
        disposal=1,
    )
    print(f"Created {OUTPUT} ({OUTPUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    create()
