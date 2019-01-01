# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""Using LET.."""

from basic_lang import program

PROGRAM = ['10 LET X = "HELLO"',
           '20 LET Y = "WORLD!"',
           '30 PRINT X',
           '40 PRINT Y']

BASIC = program.Basic()


def main():
    """Set up and run the program."""

    BASIC.run(PROGRAM)


if __name__ == '__main__':
    main()

