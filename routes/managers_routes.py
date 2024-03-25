from flask import Blueprint, request

import controllers

managers = Blueprint('managers', __name__)


@managers.route('/manager', methods=['POST'])
def add_manager():
    return controllers.manager_add(request)
