"""
"""

import datetime
import subprocess

from . import diff
from . import format


class Command(format.OutputFormatting):

    def __init__(self, command):
        self._command = command

        self._previous_datetime = ''
        self._previous_result = ''

        self._current_datetime = ''
        self._current_result = ''

    def __bool__(self):
        return bool(self._current_result)

    def _format(self, formatter=format.DefaultFormatter):
        return self._current_result

    def _diff(self):
        return diff.Diff(self._previous_result, self._current_result, self._previous_datetime, self._current_datetime)

    def _run(self):
        return subprocess.getoutput(self._command)

    def run(self, now=None):
        self._previous_datetime = self._current_datetime
        self._previous_result = self._current_result

        self._current_datetime = now or str(datetime.datetime.now())
        self._current_result = self._run()

        return self._diff()
