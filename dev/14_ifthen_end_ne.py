# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""If Then Equal with end."""

from basic_lang import program

PROGRAM = ['10 LET X = 3',
           '20 IF X = 2 THEN 50',
           '30 PRINT "THEY ARE **NOT** EQUAL."',
           '40 END',
           '50 PRINT "THEY **ARE** EQUAL."']

BASIC = program.Basic()


def main():
    """Set up and run the program."""

    BASIC.run(PROGRAM)


if __name__ == '__main__':
    main()

