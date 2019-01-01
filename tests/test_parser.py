# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""Test the parser module."""

import unittest

from basic_lang import parser

NUM = '10'
VAR = 'X'
STR = '"Hello"'
STR_SPACE = '"Hello World"'

STR_VALUE = 'Hello'
STR_SPACE_VALUE = 'Hello World'

ARITH_EXPR = '2 + 3'
ARITH_VAR_NUM = 'X - 5'


class TestParser(unittest.TestCase):
    """Test Parser."""

    def setUp(self):
        """Set up a parser."""

        self.parser = parser.Parser()

    def test_create(self):
        """Test creation to the parser."""

        self.assertTrue(self.parser is not None)

    def test_parse_num(self):
        """Test parsing a number."""

        obj = self.parser.parse_num(NUM)
        self.assertTrue(isinstance(obj, parser.Number))
        self.assertEqual(obj.value, 10)

    def test_parse_str(self):
        """Test parsing a string."""

        obj = self.parser.parse_str(STR)
        self.assertTrue(isinstance(obj, parser.String))
        self.assertEqual(obj.value, STR_VALUE)

    def test_parse_str_space(self):
        """Test parsing a string."""

        obj = self.parser.parse_str(STR_SPACE)
        self.assertTrue(isinstance(obj, parser.String))
        self.assertEqual(obj.value, STR_SPACE_VALUE)

    def test_parse_var(self):
        """Test parsing a variable."""

        obj = self.parser.parse_var(VAR)
        self.assertTrue(isinstance(obj, parser.Variable))
        self.assertEqual(obj.name, VAR)
        self.assertTrue(obj.value is None)

    def test_parse_primative_obj(self):
        """Test parsing a primative."""

        obj = self.parser.parse_primative_obj(NUM)
        self.assertTrue(isinstance(obj, parser.Number))

        obj = self.parser.parse_primative_obj(STR)
        self.assertTrue(isinstance(obj, parser.String))

        obj = self.parser.parse_primative_obj(VAR)
        self.assertTrue(isinstance(obj, parser.Variable))

    def test_parse_arith_expr(self):
        """Test parsing an arithmetic expressions."""

        obj = self.parser.parse_arith_expr(ARITH_EXPR)
        self.assertTrue(isinstance(obj, parser.ArithmeticExpression))

        self.assertTrue(isinstance(obj.arg1, parser.Number))
        self.assertTrue(isinstance(obj.arith_op, parser.ArithmeticOp))
        self.assertTrue(isinstance(obj.arith_op, parser.ArithmeticAdd))
        self.assertTrue(isinstance(obj.arg2, parser.Number))

    def test_parse_arith_ops(self):
        """Test parsing arithmetic operators."""

        add_obj = self.parser.parse_arith_op('+')
        sub_obj = self.parser.parse_arith_op('-')
        mul_obj = self.parser.parse_arith_op('*')
        div_obj = self.parser.parse_arith_op('/')

        self.assertTrue(isinstance(add_obj, parser.ArithmeticAdd))
        self.assertTrue(isinstance(sub_obj, parser.ArithmeticSub))
        self.assertTrue(isinstance(mul_obj, parser.ArithmeticMul))
        self.assertTrue(isinstance(div_obj, parser.ArithmeticDiv))

    def test_parse_bool_op(self):
        """Test parsing bool comparison operators."""

        eq_obj = self.parser.parse_bool_op('=')
        ne_obj = self.parser.parse_bool_op('<>')
        lt_obj = self.parser.parse_bool_op('<')
        le_obj = self.parser.parse_bool_op('<=')
        gt_obj = self.parser.parse_bool_op('>')
        ge_obj = self.parser.parse_bool_op('=>')

        self.assertTrue(isinstance(eq_obj, parser.BoolEqual))
        self.assertTrue(isinstance(ne_obj, parser.BoolNotEqual))
        self.assertTrue(isinstance(lt_obj, parser.BoolLessThan))
        self.assertTrue(isinstance(le_obj, parser.BoolLessOrEqual))
        self.assertTrue(isinstance(gt_obj, parser.BoolGreaterThan))
        self.assertTrue(isinstance(ge_obj, parser.BoolGreaterOrEqual))


class TestString(unittest.TestCase):
    """Test a string object."""

    def test_eval(self):
        """Test evaluating a string."""

        symbol_table = {}

        obj = parser.String('"Hello"')
        value = obj.eval(symbol_table)

        self.assertEqual(value, 'Hello')


class TestNumber(unittest.TestCase):
    """Test a number object."""

    def test_eval(self):
        """Test evaluating a number."""

        symbol_table = {}

        obj = parser.Number('10')
        value = obj.eval(symbol_table)

        self.assertEqual(value, 10)


class TestVariable(unittest.TestCase):
    """Test a variable object."""

    def setUp(self):
        """Create a variable and symbol table."""

        self.num10 = parser.Number('10')
        self.num15 = parser.Number('15')
        self.symbol_table = {'X': self.num10, 'Y': self.num15}

        self.varx = parser.Variable('X')
        self.vary = parser.Variable('Y')

    def test_eval(self):
        """Test evaluating a variable."""

        obj_x = self.varx.eval(self.symbol_table)
        obj_y = self.vary.eval(self.symbol_table)

        self.assertEqual(obj_x.value, 10)
        self.assertEqual(obj_y.value, 15)


class TestArithmeticExpression(unittest.TestCase):
    """Test an arithmetic expression."""

    def setUp(self):
        """Create a variables, an expression, and the symbol table."""

        self.num10 = parser.Number('10')
        self.num15 = parser.Number('15')
        self.symbol_table = {'X': self.num10, 'Y': self.num15}

        self.varx = parser.Variable('X')
        self.vary = parser.Variable('Y')
        self.oper = parser.ArithmeticAdd()

        self.expr = parser.ArithmeticExpression(self.varx, self.oper,
                                                self.vary)

    def test_eval(self):
        """Test evaluating the arithemetic expression."""

        obj = self.expr.eval(self.symbol_table)

        self.assertEqual(obj.value, 25)


if __name__ == '__main__':
    unittest.main()
