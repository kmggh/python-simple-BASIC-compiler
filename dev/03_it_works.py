# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""It works! program."""

from basic_lang import program

PROGRAM = ['10 PRINT "HELLO, WORLD!"',
           '20 PRINT "HEY, IT WORKS!"']

BASIC = program.Basic()


def main():
    """Set up and run the program."""

    BASIC.run(PROGRAM)


if __name__ == '__main__':
    main()

