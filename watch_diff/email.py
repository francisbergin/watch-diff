"""
"""

import functools
import getpass
import json
import logging
import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid


logger = logging.getLogger(__name__)


config_filename = '.watch-diff.json'
global_filename = os.path.join(os.path.expanduser('~'), config_filename)


if os.path.isfile(config_filename):
    with open(config_filename) as f:
        config = json.loads(f.read())
elif os.path.isfile(global_filename):
    with open(global_filename) as f:
        config = json.loads(f.read())
else:
    config = {}


smtp_host = config.get('SMTP_HOST', os.environ.get('SMTP_HOST')) or input('SMTP_HOST: ')
smtp_port = config.get('SMTP_PORT', os.environ.get('SMTP_PORT')) or input('SMTP_PORT: ')
smtp_user = config.get('SMTP_USER', os.environ.get('SMTP_USER')) or input('SMTP_USER: ')
smtp_pass = config.get('SMTP_PASS', os.environ.get('SMTP_PASS')) or getpass.getpass('SMTP_PASS: ')

smtp_port = int(smtp_port)


def _repeat_on_exception(num_times=3, exception=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            count = 0
            while True:
                try:
                    logger.info(f'running func: "{func.__name__}", count: {count}')
                    return func(*args, **kwargs)
                except Exception as e:
                    if (not exception or e.__class__ == exception) and count < num_times:
                        count += 1
                        continue
                    else:
                        raise
        return wrapper
    return decorator


@_repeat_on_exception(3, smtplib.SMTPServerDisconnected)
def _smtp_connect(smtp_host, smtp_port):
    return smtplib.SMTP(host=smtp_host, port=smtp_port)


@_repeat_on_exception(3, smtplib.SMTPAuthenticationError)
def _smtp_login(session, smtp_user, smtp_pass):
    session.login(smtp_user, smtp_pass)


def send_email(recipient, subject, text, html, msg_id=None, previous_msg_id=None):
    logger.info('sending email')

    msg = MIMEMultipart('alternative')

    msg['From'] = f'watch-diff <{smtp_user}>'
    msg['To'] = recipient
    msg['Subject'] = subject
    msg['Message-ID'] = msg_id or make_msgid()

    if previous_msg_id:
        msg['In-Reply-To'] = previous_msg_id

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    s = _smtp_connect(smtp_host, smtp_port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    _smtp_login(s, smtp_user, smtp_pass)
    s.sendmail(smtp_user, recipient, msg.as_string())
    s.quit()

    logger.info('email sent successfully')
