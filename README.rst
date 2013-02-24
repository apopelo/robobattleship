RoboBattleship game server
==========================

A simple Battleship game server which provides a REST API for players to
register, connect and fight with other players.

Website - http://robobattleship.com
GitHub - https://github.com/apopelo/robobattleship


Starting the server
-------------------

You need to have libevent and python-dev installed in your system.

Create virtualenv::

    $ mkvirtualenv robobattleship

Install requirements into virtualenv::

    $ workon robobattleship && pip install -r requirements.pip

Run the server::

    $ python robobattleship/main.py


Authors
-------

Original implementation by:

- Andrey Popelo <andrey@popelo.com>
- Sergey Lysach <sergikoff88@gmail.com>

Big thanks for idea and help to Sergey Lysach
