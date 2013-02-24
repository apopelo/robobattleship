# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
This module contains project settings.
"""
from __future__ import print_function
from __future__ import unicode_literals

import os


# Host and port for web server to listen
HOST = "0.0.0.0"
PORT = 9999

# Number of seconds to sleep before sending HTTP response to client
DELAY = 0.25

# Administrator's email
ADMIN_EMAIL = "andrey@popelo.com"

# Project's root directory
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

# Project's server dumps root directory
DUMPS_ROOT = os.path.join(PROJECT_ROOT, "dumps")

# Project's templates root directory
TEMPLATES_ROOT = os.path.join(PROJECT_ROOT, "templates")

# Project's static files root directory
STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")

# Project's log root directory
LOG_ROOT = os.path.join(PROJECT_ROOT, "logs")
LOG_FILE = os.path.join(LOG_ROOT, "robobattleship.log")

# Logger config
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'logsna': {
            '()': 'logsna.Formatter',
        }
    },
    'handlers': {
        'robobattleship': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 20,
            'filename': LOG_FILE,
            'formatter': 'logsna',
        },
    },
    'loggers': {
        'robobattleship': {
            'handlers': ['robobattleship'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'bottle': {
            'handlers': ['robobattleship'],
            'level': 'ERROR',
            'propagate': True,
        },
        'requests': {
            'handlers': ['robobattleship'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
