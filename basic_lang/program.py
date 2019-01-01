# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""Parse and execute a program."""

from basic_lang import error
from basic_lang import statement_parser


class LineLabelParseError(error.Error):
    """An illegal line number label."""


class LineParser():
    """A line parser.

    This object parses lines of input into program line tuples of a
    line label and a statement object.
    """

    def __init__(self):
        """Set up the statement parser and the program."""

        self.statement_parser = statement_parser.StatementParser()
        self.program = Program()

    def parse_line(self, line_input):
        """Parse the line.

        Args:
            line_input: str. A line of BASIC code.
        """

        words = line_input.split()
        label = words[0]
        rest = words[1:]

        try:
            int(label)
        except ValueError:
            raise LineLabelParseError(
                'Invalid line number: {0}'.format(label))

        statement_obj = self.statement_parser.parse_statement(rest)

        self.program.add_line(label, statement_obj)

    def parse_lines(self, lines):
        """Parse a list of text lines."""

        for line in lines:
            self.parse_line(line)


class Program():
    """A parsed and executable BASIC program."""

    def __init__(self):
        """Initialize the lines list.

        The lines list is a list of tuple pairs of a label and statement
        object.  The label index is a dict whith labels as keys and
        lines indices as values.  To go to a label you retrieve that
        index from the label index list.
        """

        self.lines = []
        self.label_index = {}
        self.current_line = None

    def add_line(self, line_label, statement_obj):
        """Add a line label and statement obj.

        Args:
            line_label: str.  A str form of a line number such as "10."
            statement_obj: A statement object.
        """

        self.lines.append((line_label, statement_obj))

    def first_line(self):
        """Rebuild the label lindex and Return the first line label."""

        self.label_index = {}
        for index, pair in enumerate(self.lines):
            self.label_index[pair[0]] = index

        if self.lines:
            label = self.lines[0][0]
            self.current_line = 0
        else:
            label = None

        return label

    def next_line(self):
        """Return the next line label."""

        self.current_line += 1

        return self.current_label()

    def goto_label(self, label):
        """Set the current line to a label."""

        self.current_line = self.label_index[label]
        label = self.current_label()

        return label

    def current_statement(self):
        """Return the current statement."""

        if self.current_line == len(self.lines):
            statement = None
        else:
            statement = self.lines[self.current_line][1]

        return statement

    def current_label(self):
        """Return the current label."""

        if self.current_line == len(self.lines):
            label = None
        else:
            label = self.lines[self.current_line][0]

        return label

    def statement_at_label(self, label):
        """Retrieve a statement from a given label.

        This is for program examination purposes.
        """

        line_index = self.label_index[label]
        statement_obj = self.lines[line_index][1]

        return statement_obj


class ExecutionEngine():
    """The program execution engine."""

    def __init__(self, program_obj, test_mode=False):
        """Initialize the engine."""

        self.program = program_obj
        self.symbol_table = {}
        self.test_mode = test_mode
        self.for_loops = {}

    def run(self):
        """Run the program."""

        next_line = self.program.first_line()

        while next_line:
            statement_obj = self.program.current_statement()
            statement_obj.execute(self.symbol_table, self.test_mode)

            if isinstance(statement_obj, statement_parser.Goto):
                goto_label = str(statement_obj.label.value)
                next_line = self.program.goto_label(goto_label)
            elif isinstance(statement_obj, statement_parser.For):
                var_name = statement_obj.var.name
                next_line_index = self.program.current_line + 1
                end_value = statement_obj.end.value
                self.for_loops[var_name] = (next_line_index, end_value)
                next_line = self.program.next_line()
            elif isinstance(statement_obj, statement_parser.Next):
                var_name = statement_obj.var.name
                next_line_index, end_value = self.for_loops[var_name]
                current_value = self.symbol_table[var_name].value

                if current_value > end_value:
                    next_line = self.program.next_line()
                else:
                    self.program.current_line = next_line_index
                    next_line = self.program.current_label()
            elif isinstance(statement_obj, statement_parser.IfThen):
                goto_label = str(statement_obj.label.value)
                if statement_obj.bool_result:
                    next_line = self.program.goto_label(goto_label)
                else:
                    next_line = self.program.next_line()
            elif isinstance(statement_obj, statement_parser.End):
                next_line = None
            else:
                next_line = self.program.next_line()


class Basic():
    """The main basic object to parse and run a program."""

    def __init__(self):
        """Initialize the program attributes."""

        self.program = None
        self.engine = None

    def compile_program(self, lines):
        """Compile the program."""

        line_parser = LineParser()
        line_parser.parse_lines(lines)

        self.program = line_parser.program

    def run_obj(self, test_mode=False):
        """Run a compiled program object."""

        self.engine = ExecutionEngine(self.program, test_mode=test_mode)
        self.engine.run()

    def run(self, lines, test_mode=False):
        """Run the program lines."""

        self.compile_program(lines)
        self.run_obj(test_mode=test_mode)
