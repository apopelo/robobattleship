# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0321
"""
This module contains RoboBattleship Server http views and http server runner.
"""
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys

from gevent import monkey; monkey.patch_all()
from bottle import route, run, response, hook, static_file, TEMPLATE_PATH
from bottle import jinja2_template as template

# XXX: think about this line
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import robobattleship.log
from robobattleship.settings import TEMPLATES_ROOT, STATIC_ROOT, HOST, PORT
from robobattleship.server import Server
from robobattleship.utils import JsonResponse, delay
from robobattleship.errors import RoboBattleshipException, ERRORS
from robobattleship.players.stupid import StupidBot

LOG = robobattleship.log.getLogger("robobattleship.main")

# Configure path to templates
TEMPLATE_PATH.append(TEMPLATES_ROOT)

# -----
# Hooks
# -----

@hook('after_request')
def enable_crossdomain():
    "Allow cross domain requests from browsers"
    response.headers[b'Access-Control-Allow-Origin'] = b'*'


# --------------
# Standard views
# --------------

@route('/')
def index():
    """
    Shows index page of the server.
    """
    try:
        return template('index.html',
            players=SERVER.players.values(),
            battles=SERVER.battles.values(),
            archived_battles=SERVER.archived_battles.values(),
            errorcodes=[(code, ERRORS[code]) for code in sorted(ERRORS)])
    except RoboBattleshipException as e:
        return JsonResponse.error(e)
    except:
        LOG.exception("Failed to show server index page")
        return JsonResponse.error(101)

@route('/about/')
def about():
    """
    Shows about page
    """
    try:
        return template('about.html')
    except RoboBattleshipException as e:
        return JsonResponse.error(e)
    except:
        LOG.exception("Failed to show about page")
        return JsonResponse.error(101)


@route('/players/')
def players():
    """
    Shows a list of all registered players on the server
    """
    try:
        return template('players.html', players=SERVER.players.values())
    except RoboBattleshipException as e:
        return JsonResponse.error(e)
    except:
        LOG.exception("Failed to show a list of all registered players on the "
            "server")
        return JsonResponse.error(101)

@route('/battle/<bid>')
def battle(bid):
    """
    Shows battle between two players on the screen
    """
    try:
        return template('battle.html', battle=SERVER.get_battle(bid))
    except RoboBattleshipException as e:
        return JsonResponse.error(e)
    except:
        LOG.exception("Failed to show battle with bid '%s'", bid)
        return JsonResponse.error(101)

@route('/gameboard/<bid>')
def gameboard(bid):
    """
    Shows battle board between two players on the screen
    """
    try:
        battle = SERVER.get_battle(bid)
        return JsonResponse.success({"battle": {
            "active": battle.is_active(),
            "html": template('gameboard.html', battle=battle)
        }})
    except RoboBattleshipException as e:
        return JsonResponse.error(e)
    except:
        LOG.exception("Failed to show game board with bid '%s'", bid)
        return JsonResponse.error(101)


# ------------
# Static files
# ------------

@route('/static/<filepath:path>')
def static(filepath):
    "Serves static files"
    try:
        return static_file(filepath, root=STATIC_ROOT)
    except:
        LOG.exception("Failed to show static file '%s'", filepath)
        return JsonResponse.error(101)


# ----------------
# REST API methods
# ----------------

@route('/register/<name>')
@delay()
def register(name):
    """
    Registers a new player on the server.

    :param name: player name
    """
    try:
        name = name.decode("utf-8")
        player = SERVER.register_player(name)
        BOT_STUPID1.add_opponent(player.uid)
        BOT_STUPID2.add_opponent(player.uid)
        return JsonResponse.success({'player': player.to_dict()})
    except RoboBattleshipException as e:
        return JsonResponse.error(e)
    except:
        LOG.exception("Failed to register player '%s'", name)
        return JsonResponse.error(101)

    return JsonResponse.success()

@route('/setships/<uid>/<secret>/<ships>')
@delay()
def setships(uid, secret, ships):
    """
    Set player's ships arrangement
    """
    try:
        SERVER.validate_player(uid, secret)
        SERVER.setships(uid, ships)
    except RoboBattleshipException as e:
        return JsonResponse.error(e)
    except:
        LOG.exception("Failed to set ships '%s' for player '%s'", ships, uid)
        return JsonResponse.error(101)
    return JsonResponse.success()

@route('/shoot/<uid>/<secret>/<enemy_uid>/<x:int>/<y:int>')
@delay()
def shoot(uid, secret, enemy_uid, x, y):
    """
    One player shoots at another player.
    """
    try:
        SERVER.validate_player(uid, secret)
        result = SERVER.shoot(uid, enemy_uid, x, y)
    except RoboBattleshipException as e:
        # if battle is over - archive it
        if e.code == 304:
            SERVER.archive_battle(uid, enemy_uid)
        return JsonResponse.error(e)
    except:
        LOG.exception("Failed to shoot at player '%s' at [%s,%s]",
            enemy_uid, x, y)
        return JsonResponse.error(101)

    return JsonResponse.success({'result': result})

# Service methods
@route('/dumpstate/')
@route('/dumpstate/<filename>')
@delay()
def dumpstate(filename=None):
    """
    Dumps server state into a file.
    """
    try:
        SERVER.dumpstate(filename)
    except:
        LOG.exception("Failed to dump server state")
        return JsonResponse.error(101)
    return JsonResponse.success()


# Create an instance of the server
SERVER = Server()

# Restore server state from a dumpfile
#from robobattleship.dumps.latest import server
#SERVER = server

# Create a thread with stupid bot
BOT_STUPID1 = StupidBot(name="Garry (bot)", uid="uid-63aaf540",
                        secret="usec-d821af30")
BOT_STUPID1.start()

# Create a thread with stupid bot
BOT_STUPID2 = StupidBot(name="Barry (bot)", uid="uid-566f73bf",
                        secret="usec-3f8718cb")
BOT_STUPID2.start()

# Run the web server
LOG.info("Starting RoboBattleship Web Server on {host}:{port}"
    .format(host=HOST, port=PORT))
run(host=HOST, port=PORT, server='gevent')

# Stop fighting after webserver terminates
BOT_STUPID1.stop_fight()
BOT_STUPID2.stop_fight()
