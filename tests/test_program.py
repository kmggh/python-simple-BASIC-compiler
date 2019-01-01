# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""Test the parser module."""

import unittest

from basic_lang import program
from basic_lang import statement_parser

HELLO_INPUT = '"Hello."'

LINE_INPUT = '10 PRINT "HELLO"'
LINE_INPUT2 = '20 PRINT "IT WORKED!"'

LINES_INPUT = [LINE_INPUT, LINE_INPUT2]

FOR_LINES = ['10 FOR I = 1 TO 2']


class TestLineParser(unittest.TestCase):
    """Test the line parser."""

    def setUp(self):
        """Create the line parser."""

        self.line_parser = program.LineParser()

    def test_create(self):
        """Test creation."""

        self.assertTrue(self.line_parser is not None)

    def test_parse_line(self):
        """Test parsing a line."""

        self.line_parser.parse_line(LINE_INPUT)

        label = self.line_parser.program.first_line()
        statement_obj = self.line_parser.program.current_statement()
        self.assertEqual(label, '10')
        self.assertTrue(isinstance(statement_obj, statement_parser.Print))

    def test_parse_lines(self):
        """Test parse multiple lines."""

        self.line_parser.parse_lines(LINES_INPUT)

        label = self.line_parser.program.first_line()
        statement_obj = self.line_parser.program.current_statement()
        label2 = self.line_parser.program.next_line()
        statement_obj2 = self.line_parser.program.current_statement()

        self.assertEqual(label, '10')
        self.assertEqual(label2, '20')
        self.assertTrue(isinstance(statement_obj, statement_parser.Print))
        self.assertTrue(isinstance(statement_obj2, statement_parser.Print))


class TestProgram(unittest.TestCase):
    """Test a program object."""

    def setUp(self):
        """Set up the line list."""

        self.program = program.Program()
        self.statement_parser = statement_parser.StatementParser()
        self.print_obj = self.statement_parser.parse_print(HELLO_INPUT)

    def test_create(self):
        """Test creation."""

        self.assertTrue(self.program is not None)

    def test_add_line(self):
        """Add a parsed line."""

        self.program.add_line('10', self.print_obj)
        label = self.program.first_line()
        statement_obj = self.program.current_statement()

        self.assertEqual(label, '10')
        self.assertTrue(isinstance(statement_obj, statement_parser.Print))

    def test_first_line(self):
        """Test getting the first line."""

        self.program.add_line('10', self.print_obj)

        label = self.program.first_line()

        self.assertEqual(label, '10')

    def test_next_line(self):
        """Test getting the next line."""

        self.program.add_line('10', self.print_obj)
        self.program.add_line('20', self.print_obj)

        self.program.first_line()
        next_line = self.program.next_line()
        last_line = self.program.next_line()

        self.assertEqual(next_line, '20')
        self.assertEqual(last_line, None)


class TestExecutionEngine(unittest.TestCase):
    """Test the execution engine object."""

    def setUp(self):
        """Set up the line list."""

        self.line_parser = program.LineParser()
        self.line_parser.parse_line(LINE_INPUT)
        self.program = self.line_parser.program
        self.exec_eng = program.ExecutionEngine(self.program, test_mode=True)

    def test_create(self):
        """Test creation."""

        self.assertTrue(self.exec_eng is not None)

    def test_run(self):
        """Test running the program."""

        self.exec_eng.run()

        statement_obj = self.program.current_statement()
        self.assertTrue(statement_obj is None)

        print_obj = self.program.statement_at_label('10')
        self.assertEqual(print_obj.output, 'HELLO')


class TestBasic(unittest.TestCase):
    """Test the Basic program running object."""

    def setUp(self):
        """Set up the line list."""

        self.basic = program.Basic()

    def test_create(self):
        """Test creation."""

        self.assertTrue(self.basic is not None)

    def test_run(self):
        """Test running a program."""

        self.basic.run(LINES_INPUT, test_mode=True)

        obj = self.basic.program.statement_at_label('10')
        self.assertEqual(obj.output, 'HELLO')

    def test_run_for(self):
        """Test running a single FOR statement."""

        self.basic.run(FOR_LINES, test_mode=True)

        line_index, end_value = self.basic.engine.for_loops['I']
        # Line 1 is the loop-back-to line after the FOR even though
        # it doesn't exist in this single-line program.
        self.assertEqual(line_index, 1)
        self.assertEqual(end_value, 2)


if __name__ == '__main__':
    unittest.main()
