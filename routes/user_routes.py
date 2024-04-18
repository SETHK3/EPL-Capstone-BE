from flask import Blueprint, request

import controllers

users = Blueprint('users', __name__)


@users.route('/signup', methods=['POST'])
def add_user():
    return controllers.add_user(request)


@users.route('/users', methods=['GET'])
def users_get_all():
    return controllers.users_get_all()


@users.route('/users/active', methods=['GET'])
def users_get_active():
    return controllers.users_get_active()


@users.route('/user/<user_id>', methods=['PUT'])
def user_update(user_id):
    return controllers.user_update(request, user_id)


@users.route('/user/status/<user_id>', methods=['PUT'])
def user_status(user_id):
    return controllers.user_status(user_id)


@users.route('/user/delete/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    return controllers.delete_user(user_id)
