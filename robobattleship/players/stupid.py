# -*- coding: utf-8 -*-
"""
This module contains implementation of a very stupid RoboBattleship client
player.
"""
from __future__ import print_function
from __future__ import unicode_literals

import time
import random

from robobattleship.players import Bot


SHIPS1 = ("1000100001"
          "0000000000"
          "1000000000"
          "1000000110"
          "0000010000"
          "0010010000"
          "0010010010"
          "0010010010"
          "0000000000"
          "0010000111")

SHIPS2 = ("1100000011"
          "0000000000"
          "0000000000"
          "1000100010"
          "1000000010"
          "1011110000"
          "0000000100"
          "0111000000"
          "0000000000"
          "1000000010")

SHIPS3 = ("0001100000"
          "0000000000"
          "0000011110"
          "0100000000"
          "0100000101"
          "0100010000"
          "0001010000"
          "0001010100"
          "0100000100"
          "0000010000")

SHIPS4 = ("0000000001"
          "0010111100"
          "0010000000"
          "0010000000"
          "1000001100"
          "0010000000"
          "0010000000"
          "0000111000"
          "0100000000"
          "0001100001")

SHIPS5 = ("0001100001"
          "1000000000"
          "0000000000"
          "0000100100"
          "0100100101"
          "0100100100"
          "0100100000"
          "0000000000"
          "0110001100"
          "0000100000")

class StupidBot(Bot):
    """
    A very stupid RoboBattleship client player
    """

    def __init__(self,server_url=None, name="Bot", uid=None, secret=None,
                 opponents=None):
        super(StupidBot, self).__init__(server_url, name, uid, secret)

        self.opponents = opponents or []
        self.stop_fight_flag = False

    def getships(self):
        return random.choice([SHIPS1, SHIPS2, SHIPS3, SHIPS4, SHIPS5])

    def fight_loop(self):
        """
        Infinite loop in which player shoots everyone he knows about, then
        sleeps for 0.25 sec and starts over
        """
        while True:
            if self.stop_fight_flag:
                break

            if not self.opponents:
                time.sleep(5)
                continue

            for opponent in self.opponents:
                result = self.shoot(opponent, random.randrange(10),
                                              random.randrange(10))
                if result == 304 or result == 'win':
                    self.opponents.remove(opponent)
            time.sleep(0.25)

    def add_opponent(self, uid):
        "Adds an opponent to opponents list of a bot"
        if self.uid != uid:
            self.opponents.append(uid)

    def stop_fight(self):
        "Tells bot to stop fighting"
        self.stop_fight_flag = True
