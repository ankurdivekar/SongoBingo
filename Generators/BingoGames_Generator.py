import os
import shutil
import random
import pandas as pd
from Generators.BingoCards_Generator import generate_cards
from Generators.GraphicTools import get_color_pairs


def generate_bingo_games(params):

    master_code = params['master_code']
    games_master_dir = params['games_master_dir']
    games_to_generate = params['games_to_generate']
    clipped_music_dir = params['clipped_music_dir']
    songs_per_game = params['songs_per_game']
    cards_per_game = params['cards_per_game']
    n_rows = params['rows_per_card']
    n_cols = params['cols_per_card']
    template_path = params['template_path']

    # Create new directory for the generated games
    game_set_dir = 'Games_' + str(master_code)
    games_dir = games_master_dir / game_set_dir
    games_dir.mkdir(parents=True, exist_ok=True)

    # Get random color fills
    color_fills = get_color_pairs(games_to_generate)

    # Get master list of all songs
    master_song_list = os.listdir(clipped_music_dir)

    for idx in range(games_to_generate):

        print(f'Generating game {idx+1}')
        game_code = f'{master_code}_{idx + 1}'
        game_dir = games_dir / f'Game_{game_code}'
        cards_dir = game_dir / 'Cards'
        songs_dir = game_dir / 'Songs'
        xls_path = game_dir / 'SongList.xlsx'

        # Create directories if they dont exist
        cards_dir.mkdir(parents=True, exist_ok=True)
        songs_dir.mkdir(parents=True, exist_ok=True)

        # Get a random selection of songs
        random_songs = random.sample(master_song_list, songs_per_game)

        # Shuffle the list and write to xlsx
        random.shuffle(random_songs)
        df = pd.DataFrame.from_dict({'Song Sequence': random_songs})
        df.to_excel(xls_path, header=True, index=False)

        for song in random_songs:
            # Copy to songs folder
            old_path = clipped_music_dir / song
            new_path = songs_dir / song
            shutil.copy(old_path, new_path)

        # Create cards
        card_params = {
            'game_code': game_code,
            'n_cards': int(cards_per_game),
            'rows_per_card': int(n_rows),
            'cols_per_card': int(n_cols),
            'music_dir': songs_dir,
            'card_dir': cards_dir,
            'template_path': template_path,
            'fill_light': color_fills[idx][1],
            'fill_dark': color_fills[idx][0],
            'text_size': 16
        }

        generate_cards(card_params)
