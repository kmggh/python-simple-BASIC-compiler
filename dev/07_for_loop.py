# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""Hello, Loop."""

from basic_lang import program

PROGRAM = ['10 FOR I = 1 TO 10',
           '20 PRINT I',
           '30 NEXT I']

BASIC = program.Basic()


def main():
    """Set up and run the program."""

    BASIC.run(PROGRAM)


if __name__ == '__main__':
    main()

