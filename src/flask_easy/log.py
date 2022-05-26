"""
log.py

Author: Joseph Maclean Arhin
"""

import logging
from flask import has_request_context, request
from flask.logging import default_handler


class RequestFormatter(logging.Formatter):
    """
    Request formatter to handle log format
    """

    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


formatter = RequestFormatter(
    "[%(asctime)s] %(remote_addr)s requested %(url)s\n"
    "%(levelname)s in %(module)s: %(message)s"
)
default_handler.setFormatter(formatter)
default_handler.setLevel(logging.ERROR)
default_handler.setLevel(logging.INFO)
