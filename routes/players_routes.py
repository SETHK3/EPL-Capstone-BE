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


@players.route('/players/team/<team_id>', methods=['GET'])
def players_get_by_team_id(team_id):
    return controllers.players_get_by_team_id(team_id)


@players.route('/player/<player_id>', methods=['GET'])
def player_get_by_id(player_id):
    return controllers.player_get_by_id(player_id)


@players.route('/player/<player_id>', methods=['PUT'])
def player_update(player_id):
    return controllers.player_update(request, player_id)


@players.route('/player/delete/<player_id>', methods=['DELETE'])
def player_delete(player_id):
    return controllers.player_delete(request, player_id)


@players.route('/player/team', methods=['POST'])
def player_add_transfer():
    return controllers.player_add_transfer(request)


@players.route('/player/team/<player_id>/<team_id>', methods=['DELETE'])
def player_remove_transfer(player_id, team_id):
    return controllers.player_remove_transfer(request, player_id, team_id)
