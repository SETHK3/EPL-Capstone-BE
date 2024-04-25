from flask import jsonify, request
from flask_bcrypt import generate_password_hash

from db import db
from lib.authenticate import auth, auth_admin
from models.user import Users, user_schema, users_schema
from util.reflection import populate_object


def add_user(req):
    post_data = request.form if request.form else request.json

    password = post_data.get('password')

    new_user = Users.get_new_user()
    populate_object(new_user, post_data)
    new_user.password = generate_password_hash(password).decode('utf8')

    try:
        db.session.add(new_user)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({'message': 'unable to create user'}), 400

    return jsonify({'message': 'user created', 'results': user_schema.dump(new_user)})


@auth
def users_get_active():
    try:
        query = db.session.query(Users).filter(Users.active).all()

        return jsonify({'message': 'active users found', 'results': users_schema.dump(query)}), 200
    except:
        return jsonify({'message': 'no active users found'}), 500


@auth
def user_get_by_id(user_id):
    try:
        user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

        return jsonify({'message': f'user record found', 'user': user_schema.dump(user_query)}), 200
    except:
        return jsonify({'message': f'no user record found with the following id: {user_id}'}), 404


@auth
def users_get_all():
    try:
        query = db.session.query(Users).all()

        if not query:
            return jsonify({'message': 'no users found'}), 404

        else:
            return jsonify({'message': 'users found', 'results': users_schema.dump(query)}), 200
    except:
        return jsonify({'message': 'unable to fetch users'}), 500


@auth_admin
def user_update(req, user_id):
    post_data = req.form if req.form else req.json
    query = db.session.query(Users).filter(Users.user_id == user_id).first()
    if not query:
        return jsonify({'message': f'user with id {user_id} not found'}), 404

    populate_object(query, post_data)

    try:
        db.session.commit()
        return jsonify({'message': 'user updated', 'results': user_schema.dump(query)}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to update record'}), 400


@auth_admin
def user_status(user_id):
    try:
        user = db.session.query(Users).filter(Users.user_id == user_id).first()

        if user:
            user.active = not user.active
            db.session.commit()
            return jsonify({'message': 'user status updated successfully', 'results': user_schema.dump(user)}), 200

        return jsonify({'message': 'user not found'}), 404

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'unable to activate user', 'error': str(e)}), 400


@auth_admin
def delete_user(user_id):
    user = db.session.query(Users).filter(Users.user_id == user_id).first()

    if not user:
        return jsonify({'message': f'user with user_id {user_id} not found'}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'user removed successfully', 'user_id': user_id}), 200

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'message': 'unable to remove user'}), 400
