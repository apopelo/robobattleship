# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
This module contains RoboBattleship Battle class which contains information
about battle state between two players.
"""
from __future__ import print_function
from __future__ import unicode_literals

from random import choice
from datetime import datetime

from robobattleship.errors import BattleException


CELL_EMPTY = '0'
CELL_SHIP = '1'
CELL_MISS = '•'
CELL_HIT = 'x'

class Battle(object):
    """
    RoboBattleship Battle class which holds state of battle between two players
    """

    def __init__(self, player_with_ships1, player_with_ships2):
        self.player1 = player_with_ships1
        self.player2 = player_with_ships2
        self.bid = self.generate_bid(self.player1.uid, self.player2.uid)
        self.winner = None
        self.looser = None

        # randomly choose shooter and opponent
        self.shooter = choice([self.player1, self.player2])
        self.opponent = self.player1 if self.shooter == self.player2 \
                                     else self.player2

    def shoot(self, shooter_uid, x, y):
        """
        One player shoots at another player.
        """
        if not self.is_active():
            raise BattleException(304, winner=self.winner, looser=self.looser)

        if self.shooter.uid != shooter_uid:
            raise BattleException(301)

        status = 'miss'
        if self.opponent.ships[x][y] == CELL_SHIP:
            self.opponent.ships[x][y] = CELL_HIT
            status = 'hit'
        elif self.opponent.ships[x][y] == CELL_EMPTY:
            self.opponent.ships[x][y] = CELL_MISS

        if self.is_shipdown(x, y, self.opponent.ships):
            status = 'touchdown'

        if self.is_shooter_win():
            self.winner = self.shooter
            self.looser = self.opponent
            status = 'win'

        if status == 'miss':
            # swap players
            self.shooter, self.opponent = self.opponent, self.shooter

        return status

    def is_shipdown(self, x, y, ships):
        """
        Returns true if all cells of ship were hit.
        """
        if (x < 0 or x > len(ships)-1 or
            y < 0 or y > len(ships)-1):
            return False

        if ships[x][y] != CELL_HIT:
            return False

        def is_down(x, y, ships, test, inc):
            "Helper function"
            while test(x, y) and (ships[x][y] == CELL_HIT or ships[x][y] == CELL_SHIP):
                if ships[x][y] == CELL_SHIP:
                    return False
                x, y = inc(x, y)
            return True

        # now let's try to find an alive ship cell
        return all([
            # searching to the right side
            is_down(x, y, ships, lambda x,y: y<len(ships), lambda x,y: (x,y+1)),

            # searching to the left side
            is_down(x, y, ships, lambda x,y: y>=0, lambda x,y: (x,y-1)),

            # searching down
            is_down(x, y, ships, lambda x,y: x<len(ships), lambda x,y: (x+1,y)),

            # searching up
            is_down(x, y, ships, lambda x,y: x>=0, lambda x,y: (x-1,y))
        ])

    def is_shooter_win(self):
        """
        Returns True if current shooter did win the battle.
        Shooter wins the battle if matrix of opponents ships doesn't have alive
        ship cells in it.
        """
        return not any(i == CELL_SHIP for j in self.opponent.ships for i in j)

    def is_active(self):
        "Returns True if battle is active (winner is unknown)."
        return not bool(self.winner)

    @classmethod
    def generate_bid(cls, p1uid, p2uid):
        """
        Returns unique battle ID for two players identified by uids
        """
        # make sure uids of two same players always go in the same order
        if p2uid > p1uid:
            p1uid, p2uid = p2uid, p1uid
        return "{p1uid}_vs_{p2uid}".format(p1uid=p1uid, p2uid=p2uid)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return "RoboBattleship Battle between [player1] and [player2]" \
            .format(player1=self.shooter, player2=self.opponent)

    def __repr__(self):
        return "Battle({player1}, {player2})" \
            .format(player1=repr(self.shooter), player2=repr(self.opponent))
