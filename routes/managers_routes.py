from flask import Blueprint, request

import controllers

managers = Blueprint('managers', __name__)


@managers.route('/manager', methods=['POST'])
def add_manager():
    return controllers.manager_add(request)


@managers.route('/managers', methods=['GET'])
def managers_get_all():
    return controllers.managers_get_all()
