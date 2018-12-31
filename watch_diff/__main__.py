"""
"""

import argparse
import datetime
import getpass
import logging
import os
import time

from email.utils import make_msgid

from . import command
from . import email


logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Watch command output and get notified on changes')
logging_group = parser.add_argument_group('logging level').add_mutually_exclusive_group()
logging_group.add_argument('-v', '--verbose', action='store_const',
                           const=logging.INFO, default=logging.CRITICAL,
                           dest='loglevel', help='enable verbose output')
logging_group.add_argument('-d', '--debug', action='store_const',
                           const=logging.DEBUG, dest='loglevel',
                           help='show debugging statements')
parser.add_argument('-i', '--interval', type=int, default=5, metavar='SECONDS', help='number of seconds between executions')
parser.add_argument('-r', '--recipient', help='send email to recipient')
parser.add_argument('command', help='the command to watch')


def _main():
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    e = None

    if args.recipient:
        smtp_host = os.environ.get('SMTP_HOST') or input('SMTP_HOST: ')
        smtp_port = os.environ.get('SMTP_PORT') or input('SMTP_PORT: ')
        smtp_user = os.environ.get('SMTP_USER') or input('SMTP_USER: ')
        smtp_pass = os.environ.get('SMTP_PASS') or getpass.getpass('SMTP_PASS: ')
        e = email.Email(smtp_host, smtp_port, smtp_user, smtp_pass, 'watch-diff', args.recipient)

    first_run = True
    c = command.Command(args.command)
    previous_msg_id = None

    while True:
        now = str(datetime.datetime.now())
        logger.info('executing command with time {}'.format(now))
        diff = c.run(now)

        if first_run:
            print('[{}] first_run:'.format(now))
            print(c.to_console())
            subject = 'watch-diff first_run: {}'.format(args.command)
            if e:
                logger.info('sending first_run email to {}'.format(args.recipient))
                msg_id = make_msgid()
                e.send_email(subject, str(c), c.to_html(full_html=True), msg_id)
                previous_msg_id = msg_id
        elif diff:
            print('[{}] diff:'.format(now))
            print(diff.to_console())
            subject = 'watch-diff diff: {}'.format(args.command)
            if e:
                logger.info('sending diff email to {}'.format(args.recipient))
                msg_id = make_msgid()
                e.send_email(subject, str(diff), diff.to_html(full_html=True), msg_id, previous_msg_id)
                previous_msg_id = msg_id
        else:
            print('[{}] no diff'.format(now))

        logger.info('sleeping for {} seconds'.format(args.interval))
        time.sleep(args.interval)
        first_run = False


def main():
    try:
        _main()
    except KeyboardInterrupt:
        pass
