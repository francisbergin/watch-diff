"""
"""

import functools
import logging
import smtplib
import socket
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid, formatdate


logger = logging.getLogger(__name__)


def _repeat_on_exceptions(num_times=3, *exceptions):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            count = 1
            while True:
                try:
                    logger.info('running func: "{}", count: {}'.format(func.__name__, count))
                    return func(*args, **kwargs)
                except Exception as e:
                    if (not exceptions or e.__class__ in exceptions) and count < num_times:
                        count += 1
                        time.sleep(30)
                        continue
                    else:
                        raise
        return wrapper
    return decorator


class Email:

    def __init__(self, smtp_host, smtp_port, smtp_user, smtp_pass, from_name, recipient):
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._smtp_user = smtp_user
        self._smtp_pass = smtp_pass
        self._from_name = from_name
        self._recipient = recipient

    @_repeat_on_exceptions(3, smtplib.SMTPServerDisconnected, socket.gaierror, socket.timeout)
    def _smtp_connect(self, smtp_host, smtp_port):
        return smtplib.SMTP(host=self._smtp_host, port=self._smtp_port)

    @_repeat_on_exceptions(3, smtplib.SMTPAuthenticationError, socket.gaierror, socket.timeout)
    def _smtp_login(self, session, smtp_user, smtp_pass):
        session.login(self._smtp_user, self._smtp_pass)

    def send_email(self, subject, text, html, msg_id=None, previous_msg_id=None):
        logger.info('sending email')

        msg = MIMEMultipart('alternative')

        msg['From'] = '{} <{}>'.format(self._from_name, self._smtp_user)
        msg['To'] = self._recipient
        msg['Subject'] = subject
        msg['Date'] = formatdate()
        msg['Message-ID'] = msg_id or make_msgid()

        if previous_msg_id:
            msg['In-Reply-To'] = previous_msg_id

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        s = self._smtp_connect(self._smtp_host, self._smtp_port)
        s.ehlo()
        s.starttls()
        s.ehlo()
        self._smtp_login(s, self._smtp_user, self._smtp_pass)
        s.sendmail(self._smtp_user, self._recipient, msg.as_string())
        s.quit()

        logger.info('email sent successfully')
