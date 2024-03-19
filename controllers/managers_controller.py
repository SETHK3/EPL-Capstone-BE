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


@auth
def managers_get_all():
    try:
        query = db.session.query(Managers).all()

        if not query:
            return jsonify({'message': 'no managers found'}), 404

        else:
            return jsonify({'message': 'managers found', 'results': managers_schema.dump(query)})
    except:
        return jsonify({'message': 'unable to fetch managers'}), 500


@auth
def manager_get_by_id(manager_id):
    try:
        manager_query = db.session.query(Managers).filter(Managers.manager_id == manager_id).first()

        return jsonify({'message': f'manager found by manager_id {manager_id}', 'manager': manager_schema.dump(manager_query)}), 200
    except:
        return jsonify({'message': f'no manager found with the following id: {manager_id}'}), 404
