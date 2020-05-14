import os
import shutil
import random
import pandas as pd
from pathlib import Path
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
    countdown_path = params['countdown_sample_path']

    # Create new directory for the generated games
    game_set_dir = 'Games_' + str(master_code)
    games_dir = games_master_dir / game_set_dir

    # Delete games_dir if it exists
    if Path.exists(games_dir):
        shutil.rmtree(games_dir, ignore_errors=True)
    # Create fresh games_dir
    # games_dir.mkdir(parents=True, exist_ok=True)

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
        playlist_xlsx_path = game_dir / 'SongList.xlsx'
        card_xlsx_path = game_dir / 'CardsInfo.xlsx'
        
        # Create directories if they dont exist
        cards_dir.mkdir(parents=True, exist_ok=True)
        songs_dir.mkdir(parents=True, exist_ok=True)

        # Get a random selection of songs
        random_songs = random.sample(master_song_list, songs_per_game)

        # Fix the case
        random_songs = [s.title().replace('Mp3', 'mp3') for s in random_songs]

        # Shuffle the list
        random.shuffle(random_songs)

        # Write playlist to xlsx
        df = pd.DataFrame.from_dict({'Song Sequence': random_songs})
        df.to_excel(playlist_xlsx_path, header=True, index=False)

        random_songs_paths = []
        # Copy files to generated game folder
        for song in random_songs:
            # Copy to songs folder
            old_path = clipped_music_dir / song
            new_path = songs_dir / song
            shutil.copy(old_path, new_path)
            random_songs_paths.append(new_path)

        # Write list to .m3u playlist
        playlist_name = f'Playlist_{game_code}.m3u'
        playlist_path = game_dir / f'Playlist_{game_code}.m3u'
        create_m3u_playlist(playlist_path, random_songs_paths, game_dir, countdown_path)

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
            'text_size': 16,
            'card_xlsx_path': card_xlsx_path,
        }
        generate_cards(card_params)


def create_m3u_playlist(playlist, songs, game_dir, countdown_path=None):
    FORMAT_DESCRIPTOR = "#EXTM3U"
    RECORD_MARKER = "#EXTINF"

    fp = open(playlist, "w")
    fp.write(FORMAT_DESCRIPTOR + "\n")

    if countdown_path:
        fp.write(f'{RECORD_MARKER}:30,{countdown_path.stem}\n')
        fp.write(f'{countdown_path}\n')

    for song in songs:
        song_name = song.stem
        song_path = str(song.relative_to(game_dir))
        fp.write(f'{RECORD_MARKER}:00,{song_name}\n')
        fp.write(f'{song_path}\n')
    fp.close()
