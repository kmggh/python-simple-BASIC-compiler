# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""Parse BASIC code."""

import re
from basic_lang import error

NUM_REGEX = re.compile('^[0-9]')
VAR_REGEX = re.compile('^[A-Z]')
STR_REGEX = re.compile('^"(.*)"$')


class ArithmeticOpError(error.Error):
    """The arithmetic operator error."""


class UndefinedVariableError(error.Error):
    """A variable was undefined.

    That means it was not bound to a value in the symbol table.
    """

class InvalidOperatorError(error.Error):
    """Invalid operator."""


class Parser():
    """A parser that can parse BASIC code."""

    def parse_primative_obj(self, input_str):
        """Parse an input str and return a primative object."""

        obj = self.parse_num(input_str)
        if obj:
            return obj
        obj = self.parse_var(input_str)
        if obj:
            return obj
        obj = self.parse_str(input_str)
        if obj:
            return obj

    def parse_num(self, input_str):
        """Parse a number."""

        return self.parse_primative(NUM_REGEX, Number, input_str)

    def parse_str(self, input_str):
        """Parse a string."""

        return self.parse_primative(STR_REGEX, String, input_str)

    def parse_var(self, input_str):
        """Parse a string."""

        return self.parse_primative(VAR_REGEX, Variable, input_str)

    def parse_primative(self, regex, prim_class, input_str):
        """Parse a primative object str."""

        match = regex.search(input_str)
        if match:
            result = prim_class(input_str)
        else:
            result = None

        return result

    def is_arith_primative(self, obj):
        """Return True if this obj is an arithmetic primative."""

        is_primative = isinstance(obj, (Number, Variable))

        return is_primative

    def is_num_str_primative(self, obj):
        """Return True if this obj is a value primative."""

        is_primative = isinstance(obj, (Number, String))

        return is_primative

    def parse_arith_expr(self, input_str):
        """Parse an arithmetic expression.

        Returns:
          A list of three objects, arith primatives with an arith operator
          in the middle.
        """

        words = input_str.split()
        if len(words) != 3:
            result = None
        else:
            arg1 = self.parse_primative_obj(words[0])
            arith_op = self.parse_arith_op(words[1])
            arg2 = self.parse_primative_obj(words[2])

            if arg1 and arith_op and arg2:
                result = ArithmeticExpression(arg1, arith_op, arg2)
            else:
                result = None

        return result

    def parse_arith_op(self, input_str):
        """Parse an arithmetic operator and return the object."""

        if input_str == '+':
            return ArithmeticAdd()
        elif input_str == '-':
            return ArithmeticSub()
        elif input_str == '*':
            return ArithmeticMul()
        elif input_str == '/':
            return ArithmeticDiv()
        else:
            return None

    def parse_bool_op(self, input_str):
        """Parse a boolean operator and return the object."""

        if input_str == '=':
            return BoolEqual()
        elif input_str == '<>':
            return BoolNotEqual()
        elif input_str == '<':
            return BoolLessThan()
        elif input_str == '<=':
            return BoolLessOrEqual()
        elif input_str == '>':
            return BoolGreaterThan()
        elif input_str == '=>':
            return BoolGreaterOrEqual()


class String():
    """A string primative object."""

    def __init__(self, input_str):
        """Create a number from a string."""

        match = STR_REGEX.search(input_str)
        self.value = match.group(1)

    def eval(self, symbol_table):
        """Evaluate a string."""

        return self.value


class Number():
    """A number primative object."""

    def __init__(self, input_str):
        """Create a number from a string."""

        self.value = int(input_str)

    def eval(self, symbol_table):
        """Evaluate a string."""

        return self.value


class Variable():
    """A variable object."""

    def __init__(self, input_str):
        """Create a variable object."""

        self.name = input_str
        self.value = None

    def eval(self, symbol_table):
        """Evaluate this variable."""

        if self.name in symbol_table:
            obj = symbol_table[self.name]
        else:
            raise UndefinedVariableError(
                'The variable {0} is undefined'.format(self.name))

        return obj


class ArithmeticOp():
    """An aorithmetic operator."""


class ArithmeticAdd(ArithmeticOp):
    """An addition operator."""

    def __init__(self):
        """Initialize the operator symbol."""

        self.symbol = '+'


class ArithmeticSub(ArithmeticOp):
    """An subtraction operator."""

    def __init__(self):
        """Initialize the operator symbol."""

        self.symbol = '-'


class ArithmeticMul(ArithmeticOp):
    """An multiplication operator."""

    def __init__(self):
        """Initialize the operator symbol."""

        self.symbol = '*'


class ArithmeticDiv(ArithmeticOp):
    """An division operator."""

    def __init__(self):
        """Initialize the operator symbol."""

        self.symbol = '/'


class ArithmeticExpression():
    """An arithmetic expression."""

    def __init__(self, arg1, arith_op, arg2):
        """Initialize with the three args.

        Args:
          arg1: Variable or Number.
          arith_op: ArithmeticOp.
          arg2: Variable or Number.
        """

        self.arg1 = arg1
        self.arith_op = arith_op
        self.arg2 = arg2

    def eval_num_arg(self, obj, symbol_table):
        """Evaluate an expression argument.

        We only allow for the object to be a Number or Variable.
        """

        if isinstance(obj, Variable):
            obj = obj.eval(symbol_table)
        if not isinstance(obj, Number):
            raise ArithmeticOpError(
                'Object {0} is not a Number.'.format(obj))

        return obj

    def eval(self, symbol_table):
        """Evaluate the expression."""

        obj1 = self.eval_num_arg(self.arg1, symbol_table)
        obj2 = self.eval_num_arg(self.arg2, symbol_table)

        op_symbol = self.arith_op.symbol

        if op_symbol == '+':
            value = obj1.value + obj2.value
        elif op_symbol == '-':
            value = obj1.value - obj2.value
        elif op_symbol == '*':
            value = obj1.value * obj2.value
        elif op_symbol == '/':
            value = obj1.value / obj2.value
        else:
            raise InvalidOperatorError(
                'Invalid Operator Error: {0}'.format(op_symbol))

        return Number(str(value))


class BooleanOp():
    """A boolean operator."""


class BoolEqual(BooleanOp):
    """Boolean equal."""

    def __init__(self):
        self.symbol = '='


class BoolNotEqual(BooleanOp):
    """Boolean equal."""

    def __init__(self):
        self.symbol = '<>'


class BoolLessThan(BooleanOp):
    """Boolean less than."""

    def __init__(self):
        self.symbol = '<'


class BoolLessOrEqual(BooleanOp):
    """Boolean less than or equal."""

    def __init__(self):
        self.symbol = '<='


class BoolGreaterThan(BooleanOp):
    """Boolean greater than."""

    def __init__(self):
        self.symbol = '>'


class BoolGreaterOrEqual(BooleanOp):
    """Boolean greater than or equal."""

    def __init__(self):
        self.symbol = '=>'
