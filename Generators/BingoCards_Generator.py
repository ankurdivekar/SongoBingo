import os
import random
from pathlib import Path
from PIL import Image
from Generators.GraphicTools import get_tile


def generate_cards(params):
    # assign params
    game_code = params['game_code']
    n_cards = params['n_cards']
    n_cols = params['cols_per_card']
    n_rows = params['rows_per_card']
    music_dir = params['music_dir']
    card_dir = params['card_dir']
    template_path = params['template_path']
    fill_dark = params['fill_dark']
    fill_light = params['fill_light']
    text_size = params['text_size']

    fill_avg = tuple([int((l+d)/2) for (l, d) in zip(fill_light, fill_dark)])

    # Calculate the dimensions of the grid
    [top_left_x, top_left_y] = (35, 149)
    [bottom_right_x, bottom_right_y] = (927, 637)
    grid_width = bottom_right_x - top_left_x
    grid_height = bottom_right_y - top_left_y

    tile_width = int(grid_width/n_cols)
    tile_height = int(grid_height/n_rows)

    master_code_height = 25
    master_code_width = 85

    branding_height = 30
    branding_width = 335 + 80
    branding_text = "Generated through SongoBingo by DJ AV"
    promo_text = 'Order a home version by calling up +91 98301 72572'

    # print('Grid width:', grid_width, '\nGrid height:', grid_height)
    # print('Tile width:', tile_width, '\nTile height:', tile_height)

    # Get template
    template = Image.open(template_path)

    all_songs = []
    # Get list of all music files
    for track in os.listdir(music_dir):
        [song_name, artist_name] = track.replace('.mp3', '').replace('.m4a', '').split(' - ')
        tmp = song_name + '\n----------\n' + artist_name.upper()
        all_songs.append(tmp)

    for idx in range(n_cards):
        # print('Generating card no', idx+1)

        # Create a copy of template
        card = template.copy()

        # Get a random selection of songs
        random_songs = random.sample(all_songs, n_rows*n_cols)

        # Generate the grid
        for row in range(n_rows):
            for col in range(n_cols):
                # Generate tile origin
                tile_x = top_left_x + col*tile_width
                tile_y = top_left_y + row*tile_height

                # Calculate the fill for the tile
                if row % 2 == col % 2:
                    fill = fill_dark
                else:
                    fill = fill_light

                tile_song = random_songs.pop()
                # Generate tile
                tile = get_tile(tile_width, tile_height, tile_song, fill, text_size)
                card.paste(tile, (tile_x, tile_y))

        # Insert game code
        code_tile = get_tile(master_code_width, master_code_height, game_code, (255, 255, 255, 0), text_size - 1)
        card.paste(code_tile, (850, 125))

        # Insert branding
        branding_tile = get_tile(branding_width, branding_height, branding_text, (255, 255, 255, 0), text_size,
                             text_width=75)
        card.paste(branding_tile, (555, 650))

        # Insert promo msg
        promo_tile = get_tile(branding_width, branding_height, promo_text, (255, 255, 255, 0), text_size,
                             text_width=75)
        card.paste(promo_tile, (30, 650))

        # Save card to disk
        card_path = Path.joinpath(card_dir, f'Card_{game_code}_{str(idx+1)}.png')
        card.save(card_path)
