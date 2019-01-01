# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""Counting Loop."""

from basic_lang import program

PROGRAM = ['10 LET I = 1',
           '20 PRINT I',
           '30 LET I = I + 1',
           '40 GOTO 20']

BASIC = program.Basic()


def main():
    """Set up and run the program."""

    BASIC.run(PROGRAM)


if __name__ == '__main__':
    main()

