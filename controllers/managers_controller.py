from flask import jsonify

from db import db
from lib.authenticate import auth, auth_admin
from models.managers import Managers, manager_schema, managers_schema
from util.reflection import populate_object


@auth_admin
def manager_add(req):
    post_data = req.form if req.form else req.json

    new_manager = Managers.new_manager_obj()
    populate_object(new_manager, post_data)

    try:
        db.session.add(new_manager)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to create new manager'}), 400

    return jsonify({'message': 'manager created', 'result': manager_schema.dump(new_manager)}), 201
