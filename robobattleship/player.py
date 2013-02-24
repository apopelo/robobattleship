# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
This module contains RoboBattleship Player implementation.
"""
from __future__ import print_function
from __future__ import unicode_literals

import hashlib


class PlayerWithShips(object):
    """
    Wrapper which wraps player and his current ships arrangement
    """

    def __init__(self, player, ships):
        self.player = player
        self.ships = ships

    def __getattr__(self, attrname):
        return getattr(self.player, attrname)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return "RoboBattleship Player with Ships. Player: [{player}]. " \
            "Ships: {ships}".format(player=self.player, ships=self.ships)

    def __repr__(self):
        return "PlayerWithShips({player},\n{ships})" \
            .format(player=repr(self.player), ships=repr(self.ships))


class Player(object):
    """
    RoboBattleship Player class which holds information about player
    """

    def __init__(self, name, uid=None, secret=None):
        self.name = name
        self.uid = uid or self.generate_uid(name)
        self.secret = secret or self.generate_secret(name)

    def to_dict(self):
        """
        Returns information about player as dictionary
        """
        return {"name": self.name, "uid": self.uid, "secret": self.secret}

    def generate_uid(self, name):
        """
        Generates random player id
        """
        return "uid-{uid}".format(uid=hashlib.sha1(name.encode("utf-8")).hexdigest()[:8])

    def generate_secret(self, name):
        """
        Generates random player secret
        """
        # FIXME: non-secure algorithm, this is a temporary solution for easier
        #        debugging only. Make this value random.
        return "usec-{sec}".format(sec=hashlib.sha1(name.encode("utf-8")).hexdigest()[10:18])

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return "RoboBattleship Player. Name: '{name}'. UID: '{uid}'" \
            .format(name=self.name, uid=self.uid)

    def __repr__(self):
        return "Player({name}, uid={uid}, secret={secret})" \
            .format(name=repr(self.name), uid=repr(self.uid),
                secret=repr(self.secret))
