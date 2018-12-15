"""
"""

import logging
import shlex
import subprocess


logger = logging.getLogger(__name__)


def send_message(subject, message):
    logger.info('sending notification')
    subprocess.Popen(['notify-send', subject, shlex.quote(message)])
    logger.info('notification sent successfully')
