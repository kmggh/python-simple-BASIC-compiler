# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""Hello, Loop."""

from basic_lang import program

PROGRAM = ['10 FOR I = 1 TO 10',
           '20 PRINT "HELLO"',
           '30 NEXT I',
           '40 PRINT "FINAL VALUE OF I"',
           '50 PRINT I']

BASIC = program.Basic()


def main():
    """Set up and run the program."""

    BASIC.run(PROGRAM)


if __name__ == '__main__':
    main()

