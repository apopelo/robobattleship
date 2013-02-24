# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
Main module of RoboBattleship client players implementations.
"""
from __future__ import print_function
from __future__ import unicode_literals

import time
from threading import Thread

import requests

from robobattleship.settings import HOST, PORT


class Bot(Thread):
    """
    A base class for all bot implementations
    """

    def __init__(self, server_url=None, name="Bot", uid=None, secret=None):
        super(Bot, self).__init__()

        self.url = server_url or "http://%s:%s/" % (HOST, PORT)
        self.name = name
        self.uid = uid
        self.secret = secret

    def run(self):
        time.sleep(2)
        self.register()
        self.setships(self.getships())
        self.fight_loop()

    def getships(self):
        """
        Returns ships arrangement of the bot
        """
        raise NotImplementedError()

    def fight_loop(self):
        """
        Infinite loop in which player shoots enemies
        """
        raise NotImplementedError()

    def register(self):
        """
        Registers player on the server
        """
        response = self._get("{url}register/{name}".format(url=self.url,
            name=self.name))

        if response.get('status') == 'success':
            self.uid = response.get('player').get('uid')
            self.secret = response.get('player').get('secret')
        elif response.get('error').get('code') == 203:
            return

    def setships(self, ships):
        """
        Sets player's ships on the server
        """
        self._get("{url}setships/{uid}/{secret}/{ships}".format(url=self.url,
            uid=self.uid, secret=self.secret, ships=ships))

    def shoot(self, opponent, x, y):
        """
        Shoot opponent at x,y coordinates
        """
        response = self._get("{url}shoot/{uid}/{secret}/{opponent}/{x}/{y}" \
            .format(url=self.url, uid=self.uid, secret=self.secret,
                opponent=opponent, x=x, y=y))
        if response.get('status') == 'success':
            return response.get('result')
        elif response.get('status') == 'fail':
            return response.get('error').get('code')
        else:
            return 'fail'

    def _get(self, url):
        """
        Makes an HTTP GET request to given url, checks response status and
        returns parsed json dict.
        """
        response = requests.get(url)
        if (response.status_code == 200 and
            response.headers['content-type'] == 'application/json'):
            return response.json()
        else:
            return {}
