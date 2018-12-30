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
from email.utils import make_msgid, formatdate


logger = logging.getLogger(__name__)


smtp_host = os.environ.get('SMTP_HOST') or input('SMTP_HOST: ')
smtp_port = os.environ.get('SMTP_PORT') or input('SMTP_PORT: ')
smtp_user = os.environ.get('SMTP_USER') or input('SMTP_USER: ')
smtp_pass = os.environ.get('SMTP_PASS') or getpass.getpass('SMTP_PASS: ')


def _repeat_on_exception(num_times=3, exception=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            count = 1
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


def send_email(from_name, recipient, subject, text, html, msg_id=None, previous_msg_id=None):
    logger.info('sending email')

    msg = MIMEMultipart('alternative')

    msg['From'] = f'{from_name} <{smtp_user}>'
    msg['To'] = recipient
    msg['Subject'] = subject
    msg['Date'] = formatdate()
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
