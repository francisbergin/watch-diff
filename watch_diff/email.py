"""
"""

import email
import email.mime.multipart
import email.mime.text
import getpass
import json
import logging
import os
import smtplib


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


smtp_host = config.get('SMTP_HOST') or input('SMTP_HOST: ')
smtp_port = int(config.get('SMTP_PORT')) or int(input('SMTP_PORT: '))
smtp_user = config.get('SMTP_USER') or input('SMTP_USER: ')
smtp_pass = config.get('SMTP_PASS') or getpass.getpass('SMTP_PASS: ')


def send_email(recipient, subject, text, html):
    logger.info('sending email')

    msg = email.mime.multipart.MIMEMultipart('alternative')

    msg['From'] = f'watch-diff <{smtp_user}>'
    msg['To'] = recipient
    msg['Subject'] = subject

    part1 = email.mime.text.MIMEText(text, 'plain')
    part2 = email.mime.text.MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    s = smtplib.SMTP(host=smtp_host, port=smtp_port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(smtp_user, smtp_pass)
    s.sendmail(smtp_user, recipient, msg.as_string())
    s.quit()

    logger.info('email sent successfully')
