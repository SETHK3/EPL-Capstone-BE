from flask import jsonify

from db import db
from lib.authenticate import auth, auth_admin
from models.performances import Performances, performance_schema, performances_schema
from util.reflection import populate_object


@auth_admin
def performance_add(req):
    post_data = req.form if req.form else req.json

    new_performance = Performances.new_performance_obj()
    populate_object(new_performance, post_data)

    try:
        db.session.add(new_performance)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to create new performance record'}), 400

    return jsonify({'message': 'performance record created', 'result': performance_schema.dump(new_performance)}), 201
