# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""Using LET.."""

from basic_lang import program

PROGRAM = ['10 LET X = 10',
           '20 LET Y = 15',
           '30 LET Z = X + Y',
           '40 PRINT "ANSWER = "',
           '50 PRINT Z']

BASIC = program.Basic()


def main():
    """Set up and run the program."""

    BASIC.run(PROGRAM)


if __name__ == '__main__':
    main()

