from flask import Blueprint, request

import controllers

teams = Blueprint('teams', __name__)


@teams.route('/team', methods=['POST'])
def add_team():
    return controllers.team_add(request)


@teams.route('/teams', methods=['GET'])
def teams_get_all():
    return controllers.teams_get_all()


@teams.route('/team', methods=['GET'])
def team_get_by_id():
    return controllers.team_get_by_id()
