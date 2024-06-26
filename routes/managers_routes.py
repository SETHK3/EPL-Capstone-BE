from flask import Blueprint, request

import controllers

managers = Blueprint('managers', __name__)


@managers.route('/manager', methods=['POST'])
def add_manager():
    return controllers.manager_add(request)


@managers.route('/managers', methods=['GET'])
def managers_get_all():
    return controllers.managers_get_all()


@managers.route('/manager/<manager_id>', methods=['GET'])
def manager_get_by_id(manager_id):
    return controllers.manager_get_by_id(manager_id)


@managers.route('/managers/active', methods=['GET'])
def managers_get_active():
    return controllers.managers_get_active()


@managers.route('/manager/<manager_id>', methods=['PUT'])
def manager_update(manager_id):
    return controllers.manager_update(request, manager_id)


@managers.route('/manager/status/<manager_id>', methods=['PUT'])
def manager_status(manager_id):
    return controllers.manager_status(manager_id)


@managers.route('/manager/delete/<manager_id>', methods=['DELETE'])
def manager_delete(manager_id):
    return controllers.manager_delete(manager_id)
