from flask import Blueprint, request

import controllers

teams = Blueprint('teams', __name__)


@teams.route('/team', methods=['POST'])
def add_team():
    return controllers.team_add(request)


@teams.route('/teams', methods=['GET'])
def teams_get_all():
    return controllers.teams_get_all()


@teams.route('/team/<team_id>', methods=['GET'])
def team_get_by_id():
    return controllers.team_get_by_id()


@teams.route('/team/<team_id>', methods=['PUT'])
def team_update(team_id):
    return controllers.team_update(request, team_id)


@teams.route('/team/delete/<team_id>', methods=['DELETE'])
def team_delete(team_id):
    return controllers.team_delete(team_id)
