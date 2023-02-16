"""
Make image module
"""

from io import BytesIO
from aiohttp import ClientSession

from PIL import Image, ImageDraw, ImageFont

from objects import Data


async def make_image(session: ClientSession, data: Data):
    """
    Generate a Discord Badge as an Image.
    """

    async with session.get(data.avatar_url) as response:

        avatar_bytes = BytesIO()

        while True:
            chunk = await response.content.read(100)
            if not chunk:
                break
            avatar_bytes.write(chunk)

        avatar = Image.open(avatar_bytes)

    image_size = (1150, 375)
    canvas = Image.new("RGB", image_size, (47, 49, 54))

    avatar.thumbnail((canvas.width - 75, canvas.height - 75))

    mask = Image.new("L", avatar.size)
    mask_draw = ImageDraw.Draw(mask)
    width, height = avatar.size
    mask_draw.ellipse((0, 0, width, height), fill=255)

    avatar_spacing = 75
    position = (avatar_spacing, (canvas.height // 2 - avatar.height // 2))

    canvas.paste(avatar, position, mask)

    status_icon_size = (125, 125)

    status_overlay = Image.new("RGB", status_icon_size, (47, 49, 54))

    color_map = {
        "online": (87, 242, 135),
        "idle": (254, 231, 92),
        "dnd": (237, 66, 69),
        "offline": (116, 127, 141),
    }

    color = color_map[data.status]

    status_color_width, status_color_height = status_icon_size
    status_border_thickness = 22
    status_draw = ImageDraw.Draw(status_overlay)
    status_draw.ellipse(
        (
            (
                status_overlay.width // 2
                - (status_color_width // 2 - status_border_thickness)
            ),
            (
                status_overlay.height // 2
                - (status_color_height // 2 - status_border_thickness)
            ),
            status_color_width - status_border_thickness,
            status_color_height - status_border_thickness,
        ),
        fill=color,
    )

    status_mask = Image.new("L", status_icon_size)
    status_mask_draw = ImageDraw.Draw(status_mask)
    width, height = status_icon_size
    status_mask_draw.ellipse((0, 0, width, height), fill=255)

    status_height, status_width = avatar.size

    canvas.paste(
        status_overlay,
        (
            (status_width - status_overlay.width // 2),
            (status_height - status_overlay.height // 2),
        ),
        status_mask,
    )

    font_size = 85
    font = ImageFont.truetype("fonts/Montserrat-Medium.ttf", font_size)

    text_spacing = 50

    canvas_name_text = ImageDraw.Draw(canvas)
    canvas_name_text.text(
        (
            (avatar.width + avatar_spacing + text_spacing),
            (canvas.height // 2 - font_size // 2),
        ),
        data.name,
        (150, 152, 157),
        font=font,
    )

    output = BytesIO()
    canvas.save(output, format="png")
    output.seek(0)
    return output
