from flask import Blueprint, request

import controllers

users = Blueprint('users', __name__)


@users.route('/user', methods=['POST'])
def add_user():
    return controllers.add_user(request)


@users.route('/users', methods=['GET'])
def users_get_all():
    return controllers.users_get_all()


@users.route('/user/<user_id>', methods=['PUT'])
def user_update(user_id):
    return controllers.user_update(request, user_id)


@users.route('/user/delete/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    return controllers.delete_user(user_id)


@users.route('/user/deactivate/<user_id>', methods=['PUT'])
def deactivate_user(user_id):
    return controllers.deactivate_user(user_id)


@users.route('/user/activate/<user_id>', methods=['PUT'])
def activate_user(user_id):
    return controllers.activate_user(user_id)


@users.route('/users/active', methods=['GET'])
def users_get_active():
    return controllers.users_get_active()
