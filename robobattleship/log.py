# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
This module contains logger configuration and helper functions.
"""
from __future__ import print_function
from __future__ import unicode_literals

import logging
import logging.config

from robobattleship.settings import LOGGING

# Configure logger
logging.config.dictConfig(LOGGING)
getLogger = logging.getLogger
