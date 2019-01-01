# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""Hello, World program."""

from basic_lang import program

PROGRAM = ['10 PRINT "HELLO, WORLD!"']


def main():
    """Set up and run the program."""

    line_parser = program.LineParser()
    line_parser.parse_lines(PROGRAM)

    engine = program.ExecutionEngine(line_parser.program)
    engine.run()


if __name__ == '__main__':
    main()

