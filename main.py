import modules.pgn2mp4 as pgn2mp4
import modules.input_specs as input_specs
import sys
import os

import argparse
from pathlib import Path
project_path =str(Path.cwd()) + "/" 

def main():
    #parser = argparse.ArgumentParser()
    #parser.add_argument(
    #    'path', nargs='+', help='Path to the pgn file(s)')
    #parser.add_argument(
    #    '-d', '--duration', help='Duration between moves in seconds', default=0.4)
    #parser.add_argument(
    #    '-o', '--out', help='Name of the output folder', default=Path.cwd())
    #parser.add_argument(
    #    '-r', '--reverse', help='Reverse board', action='store_true')
    #parser.add_argument(
    #    '--black-square-color',
    #    help='Color of black squares in hex or string',
    #    default='y')
    #parser.add_argument(
    #    '--white-square-color',
    #    help='Color of white squares in hex or string',
    #    default='#E6E6E6')
    #args = parser.parse_args()
    if (len(sys.argv) > 1):         #arguemnt was given
        pgn_database = sys.argv[1] + "/"
    else:                           #argument wasnt given
        pgn_database = input_specs.get_pgn_database()
    is_reverse = input_specs.get_reverse()
    duration_between_moves = input_specs.get_duration()
    ws_color, bs_color, piece_set, sound = input_specs.get_theme()
    output_folder = input_specs.get_output_folder(pgn_database, is_reverse, piece_set)
    #print(pgn_database)
    #print(is_reverse)
    #print(duration_between_moves)
    print(ws_color + bs_color + piece_set + sound)



    creator = pgn2mp4.PgnTomp4Creator(
        is_reverse, duration_between_moves, ws_color, bs_color, piece_set, sound)
    #print(pgns_folder)
    for pgn in os.listdir(project_path + "input_pgns/" + pgn_database):
        if pgn.endswith('.pgn'):
            f = Path(pgn).stem + '.mp4'
            print(pgn)
            print(project_path + f)
            creator.create_mp4(project_path + "input_pgns/" + pgn_database+ "/"+pgn, project_path + "output/"+output_folder+"/", f)


if __name__ == '__main__':
    main()