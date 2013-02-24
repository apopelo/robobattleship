# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
This module contains various utility functions.
"""
from __future__ import print_function
from __future__ import unicode_literals

import time
import functools

from robobattleship.errors import RoboBattleshipException, ERRORS
from robobattleship.settings import DELAY


class JsonResponse(object):
    """
    Utility class which simplifies creation of success and error JSON
    responses.
    """

    @classmethod
    def error(cls, error):
        "Returns an error message with given error code, wrapped in JSON"
        if isinstance(error, RoboBattleshipException):
            code = error.code
            message = error.message
        elif isinstance(error, int):
            code = error
            message = ERRORS.get(code)

        packet = {'status': 'fail',
                  'error': {
                         'code': code,
                         'message': message,
                     }
                 }
        return packet

    @classmethod
    def success(cls, payload=None):
        "Returns a success message with given payload, wrapped in JSON"
        packet = {'status': 'success'}
        if isinstance(payload, dict):
            packet.update(payload)
        return packet


def delay(seconds=DELAY):
    """
    Decorator: makes a delay before executing code of a function.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(seconds)
            return func(*args, **kwargs)
        return wrapper
    return decorator
