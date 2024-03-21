from flask import jsonify

from db import db
from lib.authenticate import auth, auth_admin
from models.performances import Performances, performance_schema, performances_schema
from util.reflection import populate_object
