import random
import textwrap
import seaborn as sns
from PIL import Image, ImageDraw, ImageFont


def get_color_palette(palette_type):

    color_list = [
        'pink',
        'light blue',
        'light green',
        'yellow',
        'sky blue',
        'lime green',
        'light purple',
        'lavender',
        'turquoise',
        'cyan',
        'aqua',
        'bright green',
        'salmon',
        'beige',
        'lilac',
        'hot pink',
        'pale green',
        'periwinkle',
        'sea green',
        'lime',
        'light pink',
        'neon green',
        'aquamarine',
        'pale blue',
        'baby blue',
    ]

    if palette_type == 'name':
        return color_list
    if palette_type == 'rgba':
        return [tuple([int(s*255) for s in c] + [0]) for c in sns.xkcd_palette(color_list)]


def get_color_pairs(n_pairs):

    palette = get_color_palette('rgba')
    pairs = [random.sample(palette, 2) for idx in range(n_pairs)]
    return pairs


def get_tile(width, height, text, fill, text_size, text_width=21, alignment='center'):
    # Create blank rectangle to write on
    image = Image.new('RGB', (width, height), fill)
    draw = ImageDraw.Draw(image)

    # message = text.replace
    message = text.split('\n')
    msg_para = []
    for m in message:
        para = textwrap.wrap(m, width=text_width)
        msg_para += para
    message = '\n'.join(msg_para)

    x1, y1, x2, y2 = 0, 0, width, height

    font = ImageFont.truetype("Assets/CenturyGothicBold.ttf", size=text_size)

    # Calculate the width and height of the text to be drawn, given font size
    w, h = draw.textsize(message, font=font)

    # Calculate the mid points and offset by the upper left corner of the bounding box
    x = (x2 - x1 - w) / 2 + x1
    y = (y2 - y1 - h) / 2 + y1

    # Write the text to the image, where (x,y) is the top left corner of the text
    draw.text((x, y), message, font=font, fill='black', align=alignment)

    # Draw the bounding box
    draw.rectangle([x1, y1, x2, y2], outline='white', width=1)

    return image
