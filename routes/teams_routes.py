from flask import Blueprint, request

import controllers

teams = Blueprint('teams', __name__)


@teams.route('/team', methods=['POST'])
def add_team():
    return controllers.team_add(request)


@teams.route('/teams', methods=['POST'])
def teams_get_all():
    return controllers.teams_get_all()
