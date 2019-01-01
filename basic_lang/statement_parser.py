# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""Parse BASIC statements."""

from basic_lang import error
from basic_lang import parser


class StatementParseError(error.Error):
    """There was an error parsing a statement."""


class StatementParseInvalidKeyword(error.Error):
    """An invalid keyword was found."""


class Print():
    """A PRINT statement object."""

    def __init__(self):
        """Initialize the arg attribute."""

        self.arg = None
        self.output = None

    def execute(self, symbol_table, test_mode=False):
        """Execute the print statement.

        Args:
          symbol_table: dict. A dict of variable names as keys and
              primative objects as values.
          test_mode: bool. If true, output goes into an output attribute
              for test verification.
        """

        parser_obj = parser.Parser()
        obj = self.arg
        while not parser_obj.is_num_str_primative(obj):
            obj = obj.eval(symbol_table)

        if test_mode:
            self.output = obj.value
        else:
            print(obj.value)


class Let():
    """The LET statement object."""

    def __init__(self):
        """Initialize the args."""

        self.var = None
        self.value = None

    def execute(self, symbol_table, test_mode=False):
        """Execute the LET statement.

        Args:
          symbol_table: dict. A dict of variable names as keys and
              primative objects as values.
          test_mode: bool. This arg has to be here for the API but
              isn't used in the LET statement.
        """

        parser_obj = parser.Parser()

        obj = self.value
        while not parser_obj.is_num_str_primative(obj):
            obj = obj.eval(symbol_table)

        symbol_table[self.var.name] = obj


class Goto():
    """The GOTO statement object."""

    def __init__(self):
        """Initialize the arg."""

        self.label = None

    def execute(self, symbol_table, test_mode=False):
        """Execute the GOTO statement.

        Args:
          symbol_table: dict. A dict of variable names as keys and
              primative objects as values.
          test_mode: bool. This arg has to be here for the API but
              isn't used in the LET statement.
        """

        obj = self.label
        while not isinstance(obj, parser.Number):
            obj = obj.eval(symbol_table)

        self.label = obj


class For():
    """The FOR statement object."""

    def __init__(self):
        """Initialize the counter variable, start and end values."""

        self.var = None
        self.start = None
        self.end = None

    def execute(self, symbol_table, test_mode=False):
        """Execute the FOR statement.

        Args:
          symbol_table: dict. A dict of variable names as keys and
              primative objects as values.
          test_mode: bool. This arg has to be here for the API but
              isn't used in the LET statement.
        """

        if not isinstance(self.var, parser.Variable):
            raise StatementParseError(
                'FOR var is not a Variable {0}'.format(self.start))
        if not isinstance(self.start, parser.Number):
            raise StatementParseError(
                'FOR start is not a Number {0}'.format(self.start))
        if not isinstance(self.end, parser.Number):
            raise StatementParseError(
                'FOR end is not a Number {0}'.format(self.end))

        symbol_table[self.var.name] = self.start


class Next():
    """The NEXT statement object."""

    def __init__(self):
        """Initialize the counter variable name."""

        self.var = None

    def execute(self, symbol_table, test_mode=False):
        """Execute the NEXT statement.

        Args:
          symbol_table: dict. A dict of variable names as keys and
              primative objects as values.
          test_mode: bool. This arg has to be here for the API but
              isn't used in the LET statement.
        """

        if not isinstance(self.var, parser.Variable):
            raise StatementParseError(
                'FOR var is not a Variable {0}'.format(self.var))

        num_obj = symbol_table[self.var.name]
        new_value = num_obj.value + 1

        symbol_table[self.var.name] = parser.Number(new_value)


class IfThen():
    """The IF THEN statement object."""

    def __init__(self):
        """Initialize the tokens."""

        self.arg1 = None
        self.bool_op = None
        self.arg2 = None
        self.label = None
        self.bool_result = None

    def execute(self, symbol_table, test_mode=False):
        """Evaluate the args and then the boolean conditional.

        Args:
          symbol_table: dict. A dict of variable names as keys and
              primative objects as values.
          test_mode: bool. This arg has to be here for the API but
              isn't used in the LET statement.
        """

        parser_obj = parser.Parser()

        arg1_obj = self.arg1
        while not parser_obj.is_num_str_primative(arg1_obj):
            arg1_obj = arg1_obj.eval(symbol_table)

        arg2_obj = self.arg2
        while not parser_obj.is_num_str_primative(arg2_obj):
            arg2_obj = arg2_obj.eval(symbol_table)

        bool_obj = self.bool_op

        if isinstance(bool_obj, parser.BoolEqual):
            self.bool_result = arg1_obj.value == arg2_obj.value
        elif isinstance(bool_obj, parser.BoolNotEqual):
            self.bool_result = arg1_obj.value != arg2_obj.value
        elif isinstance(bool_obj, parser.BoolLessThan):
            self.bool_result = arg1_obj.value < arg2_obj.value
        elif isinstance(bool_obj, parser.BoolLessOrEqual):
            self.bool_result = arg1_obj.value <= arg2_obj.value
        elif isinstance(bool_obj, parser.BoolGreaterThan):
            self.bool_result = arg1_obj.value > arg2_obj.value
        elif isinstance(bool_obj, parser.BoolGreaterOrEqual):
            self.bool_result = arg1_obj.value >= arg2_obj.value
        else:
            raise StatementParseError(
                'Invalue Boolean operator {0}'.format(bool_obj))


class End():
    """The END statement."""

    def execute(self, symbol_table, test_mode=False):
        """Execute on END does nothing.

        Args:
          symbol_table: dict. A dict of variable names as keys and
              primative objects as values.
          test_mode: bool. This arg has to be here for the API but
              isn't used in the LET statement.
        """


class Rem():
    """The REM statement."""

    def execute(self, symbol_table, test_mode=False):
        """Execute on REM does nothing.

        Args:
          symbol_table: dict. A dict of variable names as keys and
              primative objects as values.
          test_mode: bool. This arg has to be here for the API but
              isn't used in the LET statement.
        """


class StatementParser():
    """A parser to parse the BASIC staements.

    Generally a statement is a keyword, after the line number,
    followed by additional words to be parsed.  The statement dictates
    what the expected words are so the particular primative parsers
    are called.

    The argument to the parser will be list of words after the statment
    key word.
    """

    def __init__(self):
        """Initialize a primative parser."""

        self.prim_parser = parser.Parser()

    def parse_print(self, words):
        """Parse the PRINT statement.

        The arguments of print can be a primative or arithmetic expression.
        """

        print_obj = Print()
        input_str = ' '.join(words)

        obj = self.prim_parser.parse_arith_expr(input_str)
        if obj:
            print_obj.arg = obj
        else:
            obj = self.prim_parser.parse_primative_obj(input_str)
            if obj:
                print_obj.arg = obj
            else:
                raise StatementParseError(
                    'No valid print args: {0}.'.format(words))

        return print_obj

    def parse_let(self, words):
        """Parse the LET statement args.

        The arguments are a variable, "=", and an expression.
        """

        let_obj = Let()
        obj_var = self.prim_parser.parse_var(words[0])
        if obj_var:
            let_obj.var = obj_var
            if words[1] == '=':
                rest = words[2:]
                rest_str = ' '.join(words[2:])
                arith_expr_obj = self.prim_parser.parse_arith_expr(rest_str)
                prim_obj = self.prim_parser.parse_primative_obj(rest_str)

                if arith_expr_obj:
                    let_obj.value = arith_expr_obj
                elif prim_obj:
                    let_obj.value = prim_obj
                else:
                    raise StatementParseError(
                        'Invalid args for LET {0} = {1}'.format(
                            words[0], rest))
            else:
                raise StatementParseError(
                    'Invalid syntax for LET: {0}'.format(' '.join(words)))
        else:
            raise StatementParseError(
                'Invalid syntax for LET: {0} not variable.'.format(words[0]))

        return let_obj

    def parse_goto(self, words):
        """Parse the GOTO statement.

        The argument can be anything that evaluates to a number label.
        """

        goto_obj = Goto()
        input_str = ' '.join(words)

        obj = self.prim_parser.parse_arith_expr(input_str)
        if obj:
            goto_obj.label = obj
        else:
            obj = self.prim_parser.parse_num(input_str)
            if obj:
                goto_obj.label = obj
            else:
                raise StatementParseError(
                    'No valid print args: {0}.'.format(words))

        return goto_obj

    def parse_for(self, words):
        """Parse the FOR statement."""

        for_obj = For()

        if len(words) == 5:
            var_obj = self.prim_parser.parse_var(words[0])
            equal_flag = words[1] == '='
            start_obj = self.prim_parser.parse_num(words[2])
            to_flag = words[3] == 'TO'
            end_obj = self.prim_parser.parse_num(words[4])

        if all([for_obj, var_obj, equal_flag, start_obj, to_flag, end_obj]):
            for_obj.var = var_obj
            for_obj.start = start_obj
            for_obj.end = end_obj
        else:
            raise StatementParseError('Invalid FOR statement')

        return for_obj

    def parse_next(self, words):
        """Parse the NEXT statement."""

        next_obj = Next()

        if len(words) == 1:
            var_obj = self.prim_parser.parse_var(words[0])
            if var_obj:
                next_obj.var = var_obj
            else:
                raise StatementParseError(
                    'Invalid NEXT statement var {0}.'.format(words[0]))
        else:
            raise StatementParseError(
                'Invalid NEXT statement. Words: {0}.'.format(words))

        return next_obj

    def parse_ifthen(self, words):
        """Parse the IFTHEN statement."""

        ifthen_obj = IfThen()
        if len(words) == 5:
            arg1_obj = self.prim_parser.parse_primative_obj(words[0])
            bool_op_obj = self.prim_parser.parse_bool_op(words[1])
            arg2_obj = self.prim_parser.parse_primative_obj(words[2])
            then_flag = words[3] == 'THEN'
            label_obj = self.prim_parser.parse_num(words[4])

        if all([arg1_obj, bool_op_obj, arg2_obj, then_flag, label_obj]):
            ifthen_obj.arg1 = arg1_obj
            ifthen_obj.bool_op = bool_op_obj
            ifthen_obj.arg2 = arg2_obj
            ifthen_obj.label = label_obj
        else:
            raise StatementParseError(
                'Invalid IF THEN statement: {0}'.format(words))

        return ifthen_obj

    def parse_end(self, words):
        """Parse the END statement."""

        end_obj = End()

        if words:
            raise StatementParseError(
                'The END statement should have no extra words: {0}.'.format(
                    words))

        return end_obj

    def parse_rem(self, words):
        """Parse the REM statement."""

        rem_obj = Rem()

        return rem_obj

    def parse_statement(self, words):
        """Parse a set of statement words.

        The label line number has already been removed and the first
        word is the statement keyword.  The rest of the words are the
        statement arguments.

        Args:
            words: list of str.
        """

        keyword = words[0]
        rest = words[1:]

        if keyword == 'PRINT':
            obj = self.parse_print(rest)
        elif keyword == 'LET':
            obj = self.parse_let(rest)
        elif keyword == 'GOTO':
            obj = self.parse_goto(rest)
        elif keyword == 'FOR':
            obj = self.parse_for(rest)
        elif keyword == 'NEXT':
            obj = self.parse_next(rest)
        elif keyword == 'IF':
            obj = self.parse_ifthen(rest)
        elif keyword == 'END':
            obj = self.parse_end(rest)
        elif keyword == 'REM':
            obj = self.parse_rem(rest)
        else:
            raise StatementParseInvalidKeyword(
                'Invalid keyword: {0}.'.format(keyword))

        return obj
