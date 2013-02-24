# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
This module contains RoboBattleship Server implementation.
"""
from __future__ import print_function
from __future__ import unicode_literals

from robobattleship.settings import ADMIN_EMAIL


ERRORS = {
    # ERRORS SPEC
    # -----------
    #
    # 1 2 3 --> full error code
    # ^ ^ ^
    # | | |
    # `-|-|---- error group
    #   | |
    #   `--`--- error code
    #
    # Error groups:
    #  1 - Core errors
    #  2 - Data validation errors
    #  3 - Battle errors

    # Core errors
    101: "Unexpected error occured. This shouldn't happen, "
         "please, contact server administrator at {email}." \
         .format(email=ADMIN_EMAIL),

    # Data validation errors
    201: "Not enough parameters",
    202: "Player name can't be empty",
    203: "Player with name '{name}' is already "
         "registered, try choosing a different name",
    204: "Player with uid '{uid}' is not registered on the server",
    205: "Player uid can't be empty",
    206: "Player secret can't be empty",
    207: "Invalid secret for player '{uid}'",
    208: "Target coordinates (x,y) must be integers",
    209: "Battle with id '{bid}' doesn't exist",
    210: "Coordinate value must be in range [0,9]",
    211: "Length of ships string must be 100 characters exactly, you supplied "
         "{characters} characters",
    212: "Ships string must contain only '0' and '1' characters",

    # Battle errors
    301: "It's not your turn to shoot, wait until your opponent shoots and "
         "shoot again",
    302: "Unknown opponent '{uid}'",
    303: "Can't create battle, because player {uid} didn't set his ships "
         "arrangement yet",
    304: "This battle is over. Winner - {winner}. Looser - {looser}.",
}


class RoboBattleshipException(Exception):
    "Base exception class for all RoboBattleship exceptions"

    def __init__(self, code, *args, **kwargs):
        super(RoboBattleshipException, self).__init__()
        self.code = code
        self.message = ERRORS.get(self.code, "").format(**kwargs)


class ValidationException(RoboBattleshipException):
    "Input data validation exception"

class BattleException(RoboBattleshipException):
    "Exception wich can happen during a battle between two players"
