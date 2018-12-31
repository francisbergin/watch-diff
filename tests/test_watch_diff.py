"""
"""

import unittest

import watch_diff


class TestWatchDiff(unittest.TestCase):

    def test_api_available(self):

        self.assertTrue(watch_diff.Command)
        self.assertTrue(watch_diff.Diff)
        self.assertTrue(watch_diff.Email)
        self.assertTrue(watch_diff.DefaultFormatter)
        self.assertTrue(watch_diff.ConsoleFormatter)
        self.assertTrue(watch_diff.HTMLFormatter)
        self.assertTrue(watch_diff.OutputFormatting)
