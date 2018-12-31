"""
"""

import os
import unittest

import watch_diff


smtp_host = os.environ.get('SMTP_HOST')
smtp_port = os.environ.get('SMTP_PORT')
smtp_user = os.environ.get('SMTP_USER')
smtp_pass = os.environ.get('SMTP_PASS')


class TestWatchDiff(unittest.TestCase):

    def test_api_available(self):
        self.assertTrue(watch_diff.Command)
        self.assertTrue(watch_diff.Diff)
        self.assertTrue(watch_diff.Email)
        self.assertTrue(watch_diff.DefaultFormatter)
        self.assertTrue(watch_diff.ConsoleFormatter)
        self.assertTrue(watch_diff.HTMLFormatter)
        self.assertTrue(watch_diff.OutputFormatting)

    def test_command(self):
        c = watch_diff.Command('date')
        self.assertFalse(c)
        d = c.run()
        self.assertTrue(c)
        self.assertTrue(d)

    @unittest.skipIf(not smtp_host, 'SMTP_HOST is not available')
    @unittest.skipIf(not smtp_port, 'SMTP_PORT is not available')
    @unittest.skipIf(not smtp_user, 'SMTP_USER is not available')
    @unittest.skipIf(not smtp_pass, 'SMTP_PASS is not available')
    def test_email(self):
        e = watch_diff.Email(smtp_host, smtp_port, smtp_user, smtp_pass, 'watch-diff-tests', smtp_user)
        e.send_email('watch diff tests', 'text', 'html')
