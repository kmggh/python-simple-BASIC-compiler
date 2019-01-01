# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""Test the statement parser module."""

import unittest

from basic_lang import parser
from basic_lang import statement_parser

PRINT_WORDS = ['X', '+', 'Y']
STATEMENT_WORDS = ['PRINT', 'X', '+', 'Y']

LET_WORDS = ['X', '=', '10']
LET_STATEMENT_WORDS = ['LET', 'X', '=', '10']

GOTO_WORDS = ['10']
GOTO_STATEMENT_WORDS = ['GOTO', '10']

FOR_WORDS = ['I', '=', '1', 'TO', '10']
FOR_STATEMENT_WORDS = ['FOR', 'I', '=', '1', 'TO', '10']

NEXT_WORDS = ['I']
NEXT_STATEMENT_WORDS = ['NEXT', 'I']

IFTHEN_WORDS = ['X', '=', '2', 'THEN', '20']
IFTHEN_STATEMENT_WORDS = ['IF', 'X', '=', '2', 'THEN', '20']

END_STATEMENT_WORDS = ['END']

REM_STATEMENT_WORDS = ['REM', 'THIS', 'IS', 'A', 'COMMENT.']


class TestStatementParser(unittest.TestCase):
    """Test Parser."""

    def setUp(self):
        """Set up a parser."""

        self.parser = statement_parser.StatementParser()

    def test_create(self):
        """Test creation to the parser."""

        self.assertTrue(self.parser is not None)

    def test_parse_print(self):
        """Test the PRINT statement parser."""

        print_obj = self.parser.parse_print(PRINT_WORDS)

        self.assertTrue(isinstance(print_obj.arg,
                                   parser.ArithmeticExpression))

    def test_parse_let(self):
        """Test the LET statement parser."""

        let_obj = self.parser.parse_let(LET_WORDS)

        self.assertTrue(isinstance(let_obj.var, parser.Variable))
        self.assertTrue(isinstance(let_obj.value, parser.Number))
        self.assertEqual(let_obj.var.name, 'X')
        self.assertEqual(let_obj.value.value, 10)

    def test_parse_goto(self):
        """Test the GOTO statement parser."""

        goto_obj = self.parser.parse_goto(GOTO_WORDS)

        self.assertTrue(isinstance(goto_obj.label, parser.Number))
        self.assertEqual(goto_obj.label.value, 10)

    def test_parse_print_statement(self):
        """Test parsing the PRINT statement."""

        print_obj = self.parser.parse_statement(STATEMENT_WORDS)

        self.assertTrue(isinstance(print_obj, statement_parser.Print))

    def test_parse_let_statement(self):
        """Test parsing a LET statement."""

        let_obj = self.parser.parse_statement(LET_STATEMENT_WORDS)

        self.assertTrue(isinstance(let_obj, statement_parser.Let))

    def test_parse_goto_statement(self):
        """Test parsing a GOTO statement."""

        goto_obj = self.parser.parse_statement(GOTO_STATEMENT_WORDS)

        self.assertTrue(isinstance(goto_obj, statement_parser.Goto))

    def test_parse_for_statement(self):
        """Test parsing the FOR statement."""

        for_obj = self.parser.parse_statement(FOR_STATEMENT_WORDS)

        self.assertTrue(isinstance(for_obj, statement_parser.For))

    def test_parse_next_statement(self):
        """Test parsing the NEXT statement."""

        next_obj = self.parser.parse_statement(NEXT_STATEMENT_WORDS)

        self.assertTrue(isinstance(next_obj, statement_parser.Next))

    def test_parse_ifthen_statement(self):
        """Test parsing the IF THEN statement."""

        ifthen_obj = self.parser.parse_statement(IFTHEN_STATEMENT_WORDS)

        self.assertTrue(isinstance(ifthen_obj, statement_parser.IfThen))

    def test_parse_end_statement(self):
        """Test parsing the END statement."""

        end_obj = self.parser.parse_statement(END_STATEMENT_WORDS)

        self.assertTrue(isinstance(end_obj, statement_parser.End))

    def test_parse_rem_statement(self):
        """Test parsing the REM statement."""

        rem_obj = self.parser.parse_statement(REM_STATEMENT_WORDS)

        self.assertTrue(isinstance(rem_obj, statement_parser.Rem))


class TestPrint(unittest.TestCase):
    """Test the Print statement object."""

    def setUp(self):
        """Set up a print statement with an argument."""

        self.parser_obj = statement_parser.StatementParser()
        self.print_obj = self.parser_obj.parse_print(PRINT_WORDS)

        self.num10 = parser.Number('10')
        self.num15 = parser.Number('15')
        self.symbol_table = {'X': self.num10, 'Y': self.num15}

    def test_execute(self):
        """Test executing the print statement."""

        self.print_obj.execute(self.symbol_table, test_mode=True)

        self.assertEqual(self.print_obj.output, 25)

    def test_execute_str(self):
        """Test printing a string."""

        print_obj = self.parser_obj.parse_print(['"Hello,World!"'])
        print_obj.execute(self.symbol_table, test_mode=True)

        self.assertEqual(print_obj.output, 'Hello,World!')

    def test_execute_str_space(self):
        """Test printing a string."""

        print_obj = self.parser_obj.parse_print(['"Hello, World!"'])
        print_obj.execute(self.symbol_table, test_mode=True)

        self.assertEqual(print_obj.output, 'Hello, World!')


class TestLet(unittest.TestCase):
    """Test the LET statement."""

    def setUp(self):
        """Set up a print statement with an argument."""

        self.parser_obj = statement_parser.StatementParser()
        self.let_obj = self.parser_obj.parse_let(LET_WORDS)

        self.symbol_table = {}

    def test_create(self):
        """Test that Let object works."""

        self.assertTrue(self.let_obj is not None)

    def test_execute_num(self):
        """Test execute with a number."""

        self.let_obj.execute(self.symbol_table)

        value_obj = self.symbol_table['X']
        self.assertTrue(isinstance(value_obj, parser.Number))
        self.assertTrue(value_obj.value, 10)


class TestGoto(unittest.TestCase):
    """Test the GOTO statement."""

    def setUp(self):
        """Set up a goto statement with an argument."""

        self.parser_obj = statement_parser.StatementParser()
        self.goto_obj = self.parser_obj.parse_goto(GOTO_WORDS)

        self.symbol_table = {}

    def test_create(self):
        """Test that Goto object works."""

        self.assertTrue(self.goto_obj is not None)

    def test_execute(self):
        """Test the execute method."""

        self.goto_obj.execute(self.symbol_table, test_mode=True)


class TestFor(unittest.TestCase):
    """Test the FOR statement."""

    def setUp(self):
        """Set up a for statement."""

        self.parser_obj = statement_parser.StatementParser()
        self.for_obj = self.parser_obj.parse_for(FOR_WORDS)

        self.symbol_table = {}

    def test_create(self):
        """Test that For object works."""

        self.assertTrue(self.for_obj is not None)

    def test_execute(self):
        """Test the execute method."""

        self.for_obj.execute(self.symbol_table)

        value_obj = self.symbol_table['I']
        self.assertTrue(value_obj.value, 1)


class TestNext(unittest.TestCase):
    """Test the NEXT statement."""

    def setUp(self):
        """Set up a next statement."""

        self.parser_obj = statement_parser.StatementParser()
        self.next_obj = self.parser_obj.parse_next(NEXT_WORDS)

        self.symbol_table = {}

    def test_create(self):
        """Test that Next object works."""

        self.assertTrue(self.next_obj is not None)

    def test_execute(self):
        """Test execute."""

        orig_num = parser.Number(1)
        self.symbol_table['I'] = orig_num

        self.next_obj.execute(self.symbol_table)

        value_obj = self.symbol_table['I']
        self.assertTrue(value_obj.value, 2)


class TestIfthen(unittest.TestCase):
    """Test the IF THEN statement."""

    def setUp(self):
        """Set up a next statement."""

        self.parser_obj = statement_parser.StatementParser()
        self.ifthen_obj = self.parser_obj.parse_ifthen(IFTHEN_WORDS)

        self.symbol_table = {}

    def test_create(self):
        """Test that Next object works."""

        self.assertTrue(self.ifthen_obj is not None)

    def test_execute(self):
        """Test the ifthen execute."""

        orig_num = parser.Number(2)
        self.symbol_table['X'] = orig_num

        self.ifthen_obj.execute(self.symbol_table)

        self.assertTrue(self.ifthen_obj.bool_result)

    def test_execute_not_eq_value(self):
        """Test a not equal ifthen object.

        The boolean operator is = but the args are not equal.
        """

        orig_num = parser.Number(3)
        self.symbol_table['X'] = orig_num

        self.ifthen_obj.execute(self.symbol_table)

        self.assertFalse(self.ifthen_obj.bool_result)

    def test_execute_not_eq_op(self):
        """Test a not equal ifthen object.

        The args are equal but the boolean operator is <>.
        """

        orig_num = parser.Number(2)
        self.symbol_table['X'] = orig_num
        self.ifthen_obj.bool_op = parser.BoolNotEqual()

        self.ifthen_obj.execute(self.symbol_table)

        self.assertFalse(self.ifthen_obj.bool_result)

    def test_execute_greater_than(self):
        """Test a not equal ifthen object."""

        orig_num = parser.Number(3)
        self.symbol_table['X'] = orig_num
        self.ifthen_obj.bool_op = parser.BoolGreaterThan()

        self.ifthen_obj.execute(self.symbol_table)

        self.assertTrue(self.ifthen_obj.bool_result)

    def test_execute_less_than(self):
        """Test a not equal ifthen object."""

        orig_num = parser.Number(3)
        self.symbol_table['X'] = orig_num
        self.ifthen_obj.bool_op = parser.BoolLessThan()

        self.ifthen_obj.execute(self.symbol_table)

        self.assertFalse(self.ifthen_obj.bool_result)


if __name__ == '__main__':
    unittest.main()
