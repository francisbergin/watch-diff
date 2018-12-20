"""
"""

import argparse
import datetime
import logging
import time

from email.utils import make_msgid

from . import command


logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Watch command output and get notified on changes')
parser.add_argument('-v', '--verbose', action='store_true', help='enable program verbosity')
parser.add_argument('-i', '--interval', type=int, default=5, metavar='SECONDS', help='number of seconds between executions')
parser.add_argument('-e', '--email', type=str, metavar='RECIPIENT', dest='recipient', help='send email to recipient')
parser.add_argument('command', help='the command to watch')


def _main():
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    if args.recipient:
        from . import email

    first_run = True
    c = command.Command(args.command)
    previous_msg_id = None

    while True:
        now = str(datetime.datetime.now())
        logger.info(f'executing command with time {now}')
        diff = c.run(now)

        if first_run:
            print(f'[{now}] first_run:')
            print(c.to_console())
            subject = f'watch-diff first_run: {args.command}'
            if args.recipient:
                logger.info(f'sending first_run email to {args.recipient}')
                msg_id = make_msgid()
                email.send_email(args.recipient, subject, str(c), c.to_html(full_html=True), msg_id)
                previous_msg_id = msg_id
        elif diff:
            print(f'[{now}] diff:')
            print(diff.to_console())
            subject = f'watch-diff diff: {args.command}'
            if args.recipient:
                logger.info(f'sending diff email to {args.recipient}')
                msg_id = make_msgid()
                email.send_email(args.recipient, subject, str(diff), diff.to_html(full_html=True), msg_id, previous_msg_id)
                previous_msg_id = msg_id
        else:
            print(f'[{now}] no diff')

        logger.info(f'sleeping for {args.interval} seconds')
        time.sleep(args.interval)
        first_run = False


def main():
    try:
        _main()
    except KeyboardInterrupt:
        pass
