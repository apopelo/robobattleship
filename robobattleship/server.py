# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
This module contains RoboBattleship Server implementation.
"""
from __future__ import print_function
from __future__ import unicode_literals

import os
import re
import copy
import textwrap
from datetime import datetime

import robobattleship.log
from robobattleship.player import Player, PlayerWithShips
from robobattleship.battle import Battle
from robobattleship.errors import ValidationException, BattleException
from robobattleship.settings import DUMPS_ROOT

LOG = robobattleship.log.getLogger(__name__)


class Server(object):
    """
    The RoboBattleship Server which controls game state and accepts
    requests from clients
    """

    def __init__(self, players=None, ships=None, battles=None,
        archived_battles=None, last_archived_battles=None):
        self.players = players or {}
        self.ships = ships or {}
        self.battles = battles or {}
        self.archived_battles = archived_battles or {}
        self.last_archived_battles = last_archived_battles or {}
        LOG.info("Initializing the RoboBattleship Server with %s "
            "players and %s battles", self.total_players(), self.total_battles())

    def register_player(self, name):
        """
        Registeres player with given name on the server and returns a new
        player instance.

        :param name: player name
        """
        if not name:
            raise ValidationException(202)
        if len(name) > 50:
            raise ValidationException(213, maxlength=50)
        if len(name) < 2:
            raise ValidationException(214, minlength=2)
        if self.is_player_registered(name=name):
            raise ValidationException(203, name=name)

        player = Player(name)

        LOG.info("Registering [%s]", player)

        self.players[player.uid] = player
        return player

    def validate_player(self, uid, secret):
        """
        Returns True if player with given name and secret is registered on
        the server.

        Throws ValidationException otherwise.
        """
        if not uid:
            raise ValidationException(205)
        if not secret:
            raise ValidationException(206)
        if not self.is_player_registered(uid=uid):
            raise ValidationException(204, uid=uid)
        if self.get_player(uid).secret != secret:
            raise ValidationException(207, uid=uid)

    def shoot(self, p1uid, p2uid, x, y):
        """
        Player with given p1uid shoots at player with p2uid at [x,y]
        coordinates.
        """
        if not self.is_player_registered(uid=p1uid):
            raise ValidationException(204, uid=p1uid)
        if not self.is_player_registered(uid=p2uid):
            raise ValidationException(204, uid=p2uid)
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            raise ValidationException(208)
        if not (0 <= x <= 9) or not (0 <= y <= 9):
            raise ValidationException(210)

        try:
            battle = self.get_active_battle(Battle.generate_bid(p1uid, p2uid))
        except ValidationException:
            battle = self.create_battle(p1uid, p2uid)
            self.battles[battle.bid] = battle

        return battle.shoot(p1uid, x, y)

    def setships(self, uid, ships):
        """
        Sets ships arrangement for the player with given uid
        """
        if len(ships) != 100:
            raise ValidationException(211, characters=len(ships))
        if not re.match("^[10]+$", ships):
            raise ValidationException(212)

        # convert string into matrix
        self.ships[uid] = [textwrap.wrap(s, 1) for s in textwrap.wrap(ships, 10)]

    def get_player(self, uid):
        """
        Returns player instance for given uid
        """
        return self.players.get(uid)

    def get_battle(self, bid):
        """
        Returns exising battle with given bid (battle id)
        """
        if bid in self.battles:
            return self.battles.get(bid)
        if bid in self.last_archived_battles:
            return self.last_archived_battles.get(bid)
        if bid in self.archived_battles:
            return self.archived_battles.get(bid)

        raise ValidationException(209, bid=bid)

    def get_active_battle(self, bid):
        """
        Returns exising *active* battle with given bid (battle id)
        """
        if bid in self.battles:
            return self.battles.get(bid)

        raise ValidationException(209, bid=bid)

    def create_battle(self, p1uid, p2uid):
        """
        Creates new battle between players with given uids
        """
        p1 = self.get_player(p1uid)
        p2 = self.get_player(p2uid)
        p1ships = self.ships.get(p1uid)
        p2ships = self.ships.get(p2uid)

        if not p1ships:
            raise BattleException(303, uid=p1uid)
        if not p2ships:
            raise BattleException(303, uid=p2uid)

        battle = Battle(PlayerWithShips(p1, copy.deepcopy(p1ships)),
                        PlayerWithShips(p2, copy.deepcopy(p2ships)))
        return battle

    def archive_battle(self, p1uid, p2uid):
        """
        Moves active battle into archive.
        """
        # add time marker to battle id
        oldbid = Battle.generate_bid(p1uid, p2uid)
        newbid = "{oldbid}_{time}".format(oldbid=oldbid,
            time=datetime.now().strftime("%Y.%m.%d_%H.%M.%S"))

        # remove battle from active list
        battle = self.get_active_battle(oldbid)
        del self.battles[oldbid]

        # save battle to the last archived list so it will still be available
        # by old battle id
        self.last_archived_battles[oldbid] = battle

        # set new bid and add battle to archive
        battle.bid = newbid
        self.archived_battles[newbid] = battle

    def is_player_registered(self, name=None, uid=None, secret=None):
        """
        Returns True if player with given name or uid or secret is already
        registered on the server.

        :param name: player name
        """
        if name:
            return any(player.name == name for player in self.players.values())
        elif uid:
            return uid in self.players
        elif secret:
            return any(player.secret == secret for player in self.players.values())

    def total_players(self):
        "Returns total number of players registered on the server"
        return len(self.players)

    def total_battles(self):
        "Returns total number of battles registered on the server"
        return len(self.battles)

    def dumpstate(self, filename=None):
        """
        Service method which dumps surrent state of the server with players,
        battles and stats into a file
        """
        dumpfilename = filename or "server_dump_{date}.py" \
            .format(date=datetime.now().strftime("%Y_%m_%d_%H_%M"))
        with open(os.path.join(DUMPS_ROOT, dumpfilename), "w") as dumpfile:
            dumpfile.write(repr(self))

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return "RoboBattleship Server. Players: {players}. Battles: {battles}." \
            .format(players=self.total_players(), battles=self.total_battles())

    def __repr__(self):
        return (
            "from robobattleship.server import Server\n"
            "from robobattleship.player import Player, PlayerWithShips\n"
            "from robobattleship.battle import Battle\n\n"

            "server = Server("
                "players={players},\n"
                "ships={ships},\n"
                "battles={battles},\n"
                "archived_battles={archived_battles})"
            .format(players=repr(self.players),
                ships=repr(self.ships),
                battles=repr(self.battles),
                archived_battles=repr(self.archived_battles))
        )
