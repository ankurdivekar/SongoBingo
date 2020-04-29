import os
from pathlib import Path
import pandas as pd
from tkinter import *


def get_game_prize():
    available_prizes = [
        ['top line', 1],
        ['bottom line', 1],
        ['first column', 1],
        ['last column', 1],
        ['center four', 1],
        ['love line', 1],
        ['four corners', 1],
        ['tracks', 1],
        ['hurdles_1_3', 1],
        ['hurdles_2_4', 1],
        ['L2R diagonal', 1],
        ['R2L diagonal', 1],
        ['double diagonal', 1],
        ['fastest 7', 1],
        ['fastest 5', 1],
        ['full house', 1]
    ]

    game_prizes = []
    for p in available_prizes:
        prize_spec = {
            'prize_type': p[0],
            'tiles': get_prize_tiles(p[0]),
            'max_count': p[1],
            'current_count': 0,
            'winners': []
        }
        game_prizes.append(prize_spec)

    return game_prizes


def get_prize_tiles(prize_type):

    if prize_type == 'top line':
        return [0, 1, 2, 3]
    elif prize_type == 'bottom line':
        return [12, 13, 14, 15]
    elif prize_type == 'first column':
        return [0, 4, 8, 12]
    elif prize_type == 'last column':
        return [3, 7, 11, 15]
    elif prize_type == 'center four':
        return [5, 6, 9, 10]
    elif prize_type == 'love line':
        return [0, 12, 13, 14, 15]
    elif prize_type == 'four corners':
        return [0, 3, 12, 15]
    elif prize_type == 'tracks':
        return [1, 2, 5, 6, 9, 10, 13, 14]
    elif prize_type == 'L2R diagonal':
        return [0, 5, 10, 15]
    elif prize_type == 'R2L diagonal':
        return [3, 6, 9, 12]
    elif prize_type == 'double diagonal':
        return [0, 3, 5, 6, 9, 10, 12, 15]
    elif prize_type == 'hurdles_1_3':
        return [0, 1, 2, 3, 8, 9, 10, 11]
    elif prize_type == 'hurdles_2_4':
        return [4, 5, 6, 7, 12, 13, 14, 15]
    elif prize_type == 'fastest 7':
        return 7
    elif prize_type == 'fastest 5':
        return 5
    elif prize_type == 'full house':
        return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    else:
        raise RuntimeError(f'Unknown prize type: {prize_type}')


def card_is_winner(card, tiles):
    if type(tiles) is list:
        subset = [card[i] for i in tiles]
        return not any(subset)
    elif type(tiles) is int:
        # Check for no of tiles scratched
        return sum(1 for i in card if i is None) >= tiles

    else:
        raise RuntimeError('Unknown tiles definition')


def check_winners(prize, cards, logger):
    if prize['current_count'] < prize['max_count']:
        prize_type = prize['prize_type'].upper()
        for idx, card in enumerate(cards):
            # If card has not already won that prize
            if idx not in prize['winners']:
                # Check if card has won
                if card_is_winner(card, prize['tiles']):
                    logger.insert(END, f'\n~~~~~~~ Card {idx + 1:02} has won {prize_type} ~~~~~~~\n')
                    logger.yview(END)
                    prize['current_count'] += 1
                    prize['winners'].append(idx)

    return prize


class GameTracker:

    # Constructor
    def __init__(self, game_dir):
        self.game_dir = Path(game_dir)

        # Generate path for songs folder
        self.songs_dir = self.game_dir / f'Songs'

        # Get list of all songs
        self.playlist = [song.replace('.mp3', '') for song in os.listdir(self.songs_dir.absolute())]

        # Generate path for cards folder
        cards_dir = self.game_dir / f'Cards'

        self.card_idxs = []
        df = pd.read_excel(self.game_dir / 'CardsInfo.xlsx')
        n_cards = df.shape[1]

        card_name = cards_dir.parents[0].name.replace('Game_', 'Card_')

        for i in range(n_cards):
            songs = df[f'{card_name}_{i + 1}'].tolist()
            song_idxs = [self.playlist.index(s.title().replace('\n', '')) for s in songs]
            self. card_idxs.append(song_idxs)

        # Get game prizes
        self.game_prizes = get_game_prize()

    def song_played(self, song, logger):
        # Get index of song played
        song_idx = self.playlist.index(song.replace('.mp3', ''))

        # Scratch the current song on applicable cards
        for card in self.card_idxs:
            if song_idx in card:
                card[card.index(song_idx)] = None

        # Check if any new winners have happened
        for prize in self.game_prizes:
            prize = check_winners(prize, self.card_idxs, logger)
