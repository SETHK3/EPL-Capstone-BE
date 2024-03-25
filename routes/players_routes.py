from flask import Blueprint, request

import controllers

players = Blueprint('players', __name__)


@players.route('/player', methods=['POST'])
def player_add():
    return controllers.player_add(request)


@players.route('/players', methods=['GET'])
def players_get_all():
    return controllers.players_get_all()


@players.route('/players/active', methods=['GET'])
def players_get_active():
    return controllers.players_get_active()
