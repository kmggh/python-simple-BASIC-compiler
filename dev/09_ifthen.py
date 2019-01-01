# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""If Then hack because no END statement."""

from basic_lang import program

PROGRAM = ['10 LET X = 2',
           '20 IF X <> 2 THEN 40',
           '30 PRINT "THEY ARE EQUAL."',
           '40 IF X = 2 THEN 60',
           '50 PRINT "THEY ARE NOT EQUAL."',
           '60 PRINT "DONE."']

BASIC = program.Basic()


def main():
    """Set up and run the program."""

    BASIC.run(PROGRAM)


if __name__ == '__main__':
    main()

