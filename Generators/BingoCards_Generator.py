import os
import numpy as np
import random
import pandas as pd
from pathlib import Path
from PIL import Image, ImageOps
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
    predict_results = params['predict_results']
    card_xlsx_path = params['card_xlsx_path']

    # Calculate the dimensions of the grid
    [top_left_x, top_left_y] = (35, 149)
    [bottom_right_x, bottom_right_y] = (927, 637)
    grid_width = bottom_right_x - top_left_x
    grid_height = bottom_right_y - top_left_y

    tile_width = int(np.ceil(grid_width/n_cols))
    tile_height = int(np.ceil(grid_height/n_rows))

    card_code_height = 25
    card_code_width = 225

    branding_height = 30
    branding_width = 390
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
        # tmp = song_name + '\n----------\n' + artist_name.upper()
        all_songs.append(f'{song_name} - {artist_name}')

    df = pd.DataFrame()
    for idx in range(n_cards):
        # print('Generating card no', idx+1)

        # Create a copy of template
        card = template.copy()

        # Get a random selection of songs
        random_songs = random.sample(all_songs, n_rows*n_cols)

        if predict_results:
            # Save card info to txt file
            col_name = f'Card_{game_code}_{str(idx + 1)}'
            # tmp_songs = [song.replace('\n----------\n', ' - ') for song in random_songs]
            # Reverse the list because songs are assigned to grid with pop()
            df[col_name] = random_songs[::-1]

        # Generate the grid
        for row in range(n_rows):
            for col in range(n_cols):
                # Generate tile origin
                tile_x = top_left_x + col*tile_width
                tile_y = top_left_y + row*tile_height

                text_color = 'black'
                # Calculate the fill for the tile
                if row % 2 == col % 2:
                    fill = fill_dark
                    text_color = 'white'
                else:
                    fill = fill_light
                    text_color = 'black'

                # Get one song
                tile_song = random_songs.pop()
                # Format the song name
                fragments = tile_song.split(' - ')
                tile_song = f'{fragments[0].title()}\n----------\n{fragments[1].upper()}'

                # Generate tile
                tile = get_tile(tile_width, tile_height, tile_song, fill, text_size, text_color=text_color, add_tickbox=True)
                card.paste(tile, (tile_x, tile_y))

        # Insert game and card code
        code_tile = get_tile(card_code_width, card_code_height, f'{game_code}_{idx+1:02}',
                             (255, 255, 255, 0), text_size, alignment='right')
        code_tile = code_tile.rotate(90, Image.NEAREST, expand=1)
        card.paste(code_tile, (10, 150))

        # Insert branding
        branding_tile = get_tile(branding_width, branding_height, branding_text, (255, 255, 255, 0), text_size,
                                 alignment='right', text_width=75)
        card.paste(branding_tile, (535, 650))

        # Insert promo msg
        promo_tile = get_tile(tile_width*2, branding_height, promo_text, (255, 255, 255, 0), text_size,
                             alignment='left', text_width=75)
        card.paste(promo_tile, (35, 650))

        # Add border if needed
        # card = ImageOps.expand(card, border=3, fill='black')

        # Save card to disk
        card_path = Path.joinpath(card_dir, f'Card_{game_code}_{idx+1:02}.png')
        card.save(card_path)

    if predict_results:
        df.to_excel(card_xlsx_path, sheet_name='Cards Info', index=False)
