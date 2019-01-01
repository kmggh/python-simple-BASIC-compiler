# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""Load, compile and run a BASIC program."""

import argparse
import pickle
from basic_lang import program

BASIC = program.Basic()


def get_args():
    """Get the program arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--basic_file', help='The input file name.')
    parser.add_argument('-o', '--write_obj_file',
                        help='The output object file name.')
    parser.add_argument('-l', '--load_obj_file',
                        help='Load a compiled object file.')
    parser.add_argument('-r', '--run', action='store_true', default=False,
                        help='Run the file.')

    return parser.parse_args()


def main():
    """Load, compile and run the program."""

    opts = get_args()

    if opts.basic_file:
        with open(opts.basic_file, 'r') as in_file:
            raw_lines = in_file.readlines()

        lines = [r.strip() for r in raw_lines]
        BASIC.compile_program(lines)

    if opts.write_obj_file:
        with open(opts.write_obj_file, 'wb') as out_file:
            pickle.dump(BASIC.program, out_file)

    if opts.load_obj_file:
        with open(opts.load_obj_file, 'rb') as in_obj_file:
            BASIC.program = pickle.load(in_obj_file)

    if opts.run:
        BASIC.run_obj()


if __name__ == '__main__':
    main()
