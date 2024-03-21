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


@auth
def performances_get_all():
    try:
        query = db.session.query(Performances).all()

        if not query:
            return jsonify({'message': 'no performance records found'}), 404

        else:
            return jsonify({'message': 'performance records found', 'results': performances_schema.dump(query)})
    except:
        return jsonify({'message': 'unable to fetch performance records'}), 500


@auth
def performance_get_by_id(performance_id):
    try:
        performance_query = db.session.query(Performances).filter(Performances.performance_id == performance_id).first()

        return jsonify({'message': f'performance record found by performance_id {performance_id}', 'performance record': performance_schema.dump(performance_query)}), 200
    except:
        return jsonify({'message': f'no performance record found with the following id: {performance_id}'}), 404


@auth_admin
def performance_update(req, performance_id):
    post_data = req.form if req.form else req.json

    query = db.session.query(Performances).filter(Performances.performance_id == performance_id).first()
    if not query:
        return jsonify({'message': f'performance record with id {performance_id} not found'}), 404

    populate_object(query, post_data)

    try:
        db.session.commit()
        return jsonify({'message': 'performance record updated', 'results': performance_schema.dump(query)}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to update performance record'}), 400


@auth_admin
def performance_delete(performance_id):
    query = db.session.query(Performances).filter(Performances.performance_id == performance_id).first()

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'error': 'unable to delete performance record'}), 400

    return jsonify({'message': 'performance record successfully deleted'}), 200
