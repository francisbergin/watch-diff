"""
"""

import difflib

from . import format


class Diff(format.OutputFormatting):

    def __init__(self, a, b, previous_datetime, current_datetime):
        self._a = a
        self._b = b
        self._diff = '\n'.join(difflib.unified_diff(a.splitlines(), b.splitlines(), 'Previous', 'Current', previous_datetime, current_datetime, lineterm='')) or None

    def __bool__(self):
        return bool(self._diff)

    def _format(self, formatter=format.DefaultFormatter):
        lines = self._diff.splitlines()
        output = []
        for line in lines[:2]:
            output.append('{}{}{}'.format(formatter.header_start, line, formatter.header_end))
        for line in lines[2:]:
            if line[0] == '+':
                output.append('{}{}{}'.format(formatter.addition_start, line, formatter.addition_end))
            elif line[0] == '-':
                output.append('{}{}{}'.format(formatter.subtraction_start, line, formatter.subtraction_end))
            else:
                output.append(line)
        return '\n'.join(output)
