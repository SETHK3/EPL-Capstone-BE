from flask import jsonify

from db import db
from lib.authenticate import auth, auth_admin
from models.managers import Managers, manager_schema, managers_schema
from util.reflection import populate_object
