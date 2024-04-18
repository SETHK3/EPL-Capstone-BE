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

        return jsonify({'message': f'manager found', 'manager': manager_schema.dump(manager_query)}), 200
    except:
        return jsonify({'message': f'no manager found with the following id: {manager_id}'}), 404


@auth
def managers_get_active():
    try:
        query = db.session.query(Managers).filter(Managers.active).all()

        return jsonify({'message': 'active managers found', 'results': managers_schema.dump(query)}), 200
    except:
        return jsonify({'message': 'no active managers found'}), 500


@auth_admin
def manager_update(req, manager_id):
    post_data = req.form if req.form else req.json

    query = db.session.query(Managers).filter(Managers.manager_id == manager_id).first()
    if not query:
        return jsonify({'message': f'manager with id {manager_id} not found'}), 404

    populate_object(query, post_data)

    try:
        db.session.commit()
        return jsonify({'message': 'manager updated', 'results': manager_schema.dump(query)}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to update manager'}), 400


@auth_admin
def manager_status(manager_id):
    try:
        manager = db.session.query(Managers).filter(Managers.manager_id == manager_id).first()

        if manager:
            manager.active = not manager.active
            db.session.commit()
            return jsonify({'message': 'manager status updated successfully', 'results': manager_schema.dump(manager)}), 200

        return jsonify({'message': 'manager not found'}), 404

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'unable to activate manager', 'error': str(e)}), 400


@auth_admin
def manager_delete(manager_id):
    query = db.session.query(Managers).filter(Managers.manager_id == manager_id).first()

    try:
        db.session.delete(query)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'unable to delete manager: {str(e)}'}), 400

    return jsonify({'message': 'manager successfully deleted'}), 200
