import random
import textwrap
import seaborn as sns
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def get_color_palette(palette_type):

    dark_color_list = [
        'bright red',
        'bright purple',
        'bright pink',
        'bright blue',
        'bright blue',
        'bright purple',
        'bright pink',
        'bright red',
        'khaki green',
        'bright orange',
        'bordeaux',
        'russet',
        'vermillion',
        'brown orange',
        'bright magenta',
        'cherry red',
        'mulberry',
        'muted purple',
        'camouflage green',
        'lipstick',
        'rich purple'
        ]
    light_color_list = [
        'light blue',
        'light green',
        'light purple',
        'light pink',
        'light orange',
        'light teal',
        'light grey',
        'light yellow',
        'light violet',
        'light turquoise',
        'light aqua',
        'light tan',
        'ice blue',
        'light sky blue',
        'tiffany blue',
        'light bluish green',
        'light light green',
        'really light blue',
        'greenish turquoise',
        'bright cyan',
        'very light pink',
        'banana',
        'pale lime',
        'light beige',
        'butter yellow'
    ]

    color_list = dark_color_list + light_color_list

    if palette_type == 'name':
        return color_list
    if palette_type == 'rgba':
        return [tuple([int(s*255) for s in c] + [0]) for c in sns.xkcd_palette(color_list)]
    if palette_type == 'lightdark':
        dark_palette = [tuple([int(s*255) for s in c] + [0]) for c in sns.xkcd_palette(dark_color_list)]
        light_palette = [tuple([int(s * 255) for s in c] + [0]) for c in sns.xkcd_palette(light_color_list)]
        return dark_palette, light_palette


def get_color_pairs(n_pairs):

    # palette = get_color_palette('rgba')
    # pairs = [random.sample(palette, 2) for idx in range(n_pairs)]

    palette_dark, palette_light = get_color_palette('lightdark')
    pairs = [[random.choice(palette_dark), random.choice(palette_light)] for idx in range(n_pairs)]
    return pairs


def get_tile(width, height, text, fill, text_size, text_color='black', text_width=21, alignment='center', add_tickbox=False):
    # Create blank rectangle to write on
    image = Image.new('RGB', (width, height), fill)
    draw = ImageDraw.Draw(image)

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

    if alignment == 'center':
        # Calculate the mid points and offset by the upper left corner of the bounding box
        x = (x2 - x1 - w) / 2 + x1
        y = (y2 - y1 - h) / 2 + y1

    elif alignment == 'right':
        x = x2 - w + x1
        y = (y2 - y1 - h) / 2 + y1

    elif alignment == 'left':
        x = x1
        y = (y2 - y1 - h) / 2 + y1

    # Write the text to the image, where (x,y) is the top left corner of the text
    draw.text((x, y), message, font=font, fill=text_color, align=alignment)

    # Draw the bounding box
    draw.rectangle([x1, y1, x2, y2], outline='white', width=1)

    # Draw the tick box
    if add_tickbox:
        tickbox_size = int(np.ceil(width/15))
        tickbox_black = Image.new('RGB', (tickbox_size, tickbox_size), 'black')
        tickbox_white = Image.new('RGB', (tickbox_size-2, tickbox_size-2), 'white')
        image.paste(tickbox_black, (width-5-tickbox_size+1, 5))
        image.paste(tickbox_white, (width-5-tickbox_size+2, 5+1))

    return image
