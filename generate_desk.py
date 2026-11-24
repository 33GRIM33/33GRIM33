"""Render the profile's pixel-art banner with Pillow."""

from pathlib import Path
from random import Random

from PIL import Image, ImageDraw


def render(frame):
    image = Image.new("RGB", (360, 120), "#17242b")
    draw = ImageDraw.Draw(image)
    box = draw.rectangle
    line = draw.line
    poly = draw.polygon

    # Rainy skyline beyond the workshop window.
    box((12, 8, 204, 103), fill="#10191f")
    for y in range(13, 94):
        line((17, y, 199, y), fill=(30 + y // 3, 48 + y // 3, 63 + y // 4))
    rng = Random(18)
    for x in range(17, 198, 12):
        height = rng.randint(13, 49)
        roof = 93 - height
        box((x, roof, x + 10, 93), fill="#243e49")
        for y in range(roof + 4, 93, 6):
            for offset in (2, 6):
                if rng.random() < 0.34:
                    box((x + offset, y, x + offset + 1, y + 1), fill="#c6a26e")
    for _ in range(55):
        x = rng.randrange(3, 182)
        y = (rng.randrange(80) + frame * 4) % 80
        line((17 + x - y // 7, 13 + y, 16 + x - y // 7, 16 + y), fill="#678491")
    box((0, 0, 11, 103), fill="#17242b")
    box((12, 8, 16, 100), fill="#10191f")
    box((104, 9, 109, 98), fill="#10191f")
    box((11, 94, 205, 101), fill="#10191f")
    box((10, 100, 205, 103), fill="#38525a")

    # A CRT, a mug, and the little face on the screen.
    box((0, 105, 359, 119), fill="#986148")
    box((0, 108, 359, 119), fill="#503935")
    poly([(216, 99), (301, 99), (314, 111), (203, 111)], fill="#3a2a2a")
    box((246, 92, 269, 102), fill="#818d7c")
    box((232, 101, 284, 104), fill="#adab8f")
    poly([(213, 37), (292, 37), (302, 46), (302, 88), (295, 96),
          (210, 96), (206, 91), (206, 44)], fill="#c7c5a9")
    box((295, 48, 301, 89), fill="#8c9583")
    box((212, 43, 290, 88), fill="#737f73")
    draw.rounded_rectangle((216, 46, 286, 84), radius=5, fill="#213d37")
    for y in range(48, 85, 3):
        line((220, y, 282, y), fill="#294841")
    if frame in (12, 13):
        line((233, 61, 240, 61), fill="#bfeeaa", width=2)
        line((260, 61, 267, 61), fill="#bfeeaa", width=2)
    else:
        box((235, 57, 239, 64), fill="#bfeeaa")
        box((260, 57, 264, 64), fill="#bfeeaa")
    line([(244, 70), (247, 73), (252, 73), (255, 70)], fill="#bfeeaa", width=2)
    box((279, 91, 282, 92), fill="#39694d")
    poly([(218, 109), (279, 109), (288, 116), (209, 116)], fill="#c4bea0")
    for x in range(220, 281, 5):
        line((x, 111, x + 2, 111), fill="#777c72")
    box((318, 88, 333, 104), fill="#e3ac6a")
    box((318, 88, 333, 90), fill="#6c4b3b")
    box((334, 92, 338, 99), outline="#e3ac6a", width=2)
    for offset in (0, 4):
        rise = (frame + offset) % 10
        line((324 + offset // 2, 85 - rise, 325 + offset // 2, 83 - rise),
             fill="#8b9e98")

    return image.resize((1080, 360), Image.Resampling.NEAREST)


if __name__ == "__main__":
    frames = [render(frame) for frame in range(20)]
    assets = Path(__file__).parent / "assets"
    frames[0].save(assets / "rainy-desk.gif", save_all=True,
                   append_images=frames[1:], duration=140, loop=0)
