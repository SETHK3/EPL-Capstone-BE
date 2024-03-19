from flask import jsonify

from db import db
from lib.authenticate import auth, auth_admin
from models.teams import Teams, team_schema, teams_schema
from util.reflection import populate_object
