try:
    from . import chess
except ImportError:
    import chess

import argparse
from pathlib import Path

from PIL import Image
from moviepy.editor import *
import numpy as np

project_path =str(Path.cwd()) + "/" 

class PgnTomp4Creator:
    '''
    PGN to mp4 creator class
    Parameters
    ----------
    reverse : bool, optional
        Whether to reverse board or not
    duration : float, optional
        Duration between moves in seconds
    ws_color : str, optional
        Color of white squares in hex or string
    bs_color : str, optional
        Color of black squares in hex or string
    '''

    _BOARD_SIZE = 1080
    _SQ_SIZE = _BOARD_SIZE // 8

    def __init__(self, reverse=False, duration=0.4, ws_color='#E6E6E6', bs_color='#E600E6', piece_set="", sound=""):
        self.duration = duration

        self._pieces = {}
        self._reverse = reverse
        self._ws_color = ws_color
        self._bs_color = bs_color
        self._piece_set = piece_set
        self._sound = sound
        self._should_redraw = True

    def _draw_board(self):
        if not self._pieces:
            for asset in (Path(project_path + 'assets/pieces/pngs/' + self._piece_set)).iterdir():
                self._pieces[asset.stem] = Image.open(asset)

        self._ws = Image.new('RGBA', (self._SQ_SIZE, self._SQ_SIZE),
                             self._ws_color)
        self._bs = Image.new('RGBA', (self._SQ_SIZE, self._SQ_SIZE),
                             self._bs_color)

        self._initial_board = Image.new(
            'RGBA', (self._BOARD_SIZE, self._BOARD_SIZE))
        self._update_board_image(self._initial_board, chess.INITIAL_STATE,
                                 list(chess.INITIAL_STATE.keys()))

        self._should_redraw = False
        print(self._ws_color + self._bs_color)

    def _coordinates_of_square(self, square):
        c = ord(square[0]) - 97
        r = int(square[1]) - 1

        if self._reverse:
            return ((7 - c) * self._SQ_SIZE, r * self._SQ_SIZE)
        else:
            return (c * self._SQ_SIZE, (7 - r) * self._SQ_SIZE)

    def _update_board_image(self, board_image, game_state, changed_squares):
        for square in changed_squares:
            crd = self._coordinates_of_square(square)

            if sum(crd) % (self._SQ_SIZE * 2) == 0:
                board_image.paste(self._ws, crd)
            else:
                board_image.paste(self._bs, crd)

            piece = game_state[square]
            if piece:
                img = self._pieces[piece]
                board_image.paste(img, crd, img)

    def create_mp4(self, pgn, out_path=None, game_name=None):
        '''
        Creates mp4 of pgn with same name.
        player1-player2.pgn -> player1-player2.mp4 (or as out_path)
        PARAMETERS
        -----------
        pgn : str
            Path of pgn file
        out_path : str, optional
            Output path of mp4 
        '''
        if self._should_redraw:
            self._draw_board()

        board_image = self._initial_board.copy()
        frames = [board_image.copy()]

        game = chess.ChessGame(pgn)

        while not game.is_finished:
            previous = game.state.copy()
            game.next()
            changed_sqares2 = []
            for s in game.state.keys():
                if (game.state[s] != previous[s]):
                    changed_sqares2.append(s)
            self._update_board_image(board_image, game.state,changed_sqares2)
            frames.append(board_image.copy())

        last = frames[len(frames) - 1]
        for _ in range(3):
            frames.append(last)

        if not out_path:
            out_path = Path(pgn).stem + '.mp4'
        frames_np = []
        for frame in frames:
            frames_np.append(np.array(frame)) 
        print(type(frames_np[1]))
        clip = ImageSequenceClip(frames_np, fps=1)
        sound = AudioFileClip(project_path + "assets/sounds/" + self._sound)
        duration_of_sound = sound.duration
        pause_duration = 1.0 - duration_of_sound  # duration of the pause in seconds
        small_pause_audio_clip = AudioClip(lambda t: [0], duration=0.15)
        pause_audio_clip = AudioClip(lambda t: [0], duration=pause_duration)
        num_of_moves = len(frames)-5
        sounds = []
        sounds.append(small_pause_audio_clip)
        for i in range(num_of_moves):
            sounds.append(pause_audio_clip)
            sounds.append(sound)
        concatenated_audio = concatenate_audioclips(sounds)
        clip.audio = concatenated_audio
        os.makedirs(out_path)
        clip.write_videofile(out_path+game_name)
        print(concatenated_audio.duration)
        print(clip.duration)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path', nargs='+', help='Path to the pgn file(s)')
    parser.add_argument(
        '-d', '--duration', help='Duration between moves in seconds', default=0.4)
    parser.add_argument(
        '-o', '--out', help='Name of the output folder', default=Path.cwd())
    parser.add_argument(
        '-r', '--reverse', help='Reverse board', action='store_true')
    parser.add_argument(
        '--black-square-color',
        help='Color of black squares in hex or string',
        default='#E600E6')
    parser.add_argument(
        '--white-square-color',
        help='Color of white squares in hex or string',
        default='#E6E6E6')
    args = parser.parse_args()

    creator = PgnTomp4Creator(
        args.reverse, float(args.duration), args.white_square_color, args.black_square_color)
    for pgn in args.path:
        f = Path(pgn).stem + '.mp4'
        creator.create_mp4(pgn, Path(args.out) / f)


if __name__ == '__main__':
    main()
