from flask import Blueprint, request

import controllers

performances = Blueprint('performances', __name__)


@performances.route('/performance', methods=['POST'])
def add_performance():
    return controllers.performance_add(request)


@performances.route('/performances', methods=['GET'])
def performances_get_all():
    return controllers.performances_get_all()


@performances.route('/performance', methods=['GET'])
def performance_get_by_id():
    return controllers.performance_get_by_id()


@performances.route('/performance/<performance_id>', methods=['PUT'])
def performance_update(performance_id):
    return controllers.performance_update(request, performance_id)


@performances.route('/performance/delete/<performance_id>', methods=['DELETE'])
def performance_delete(performance_id):
    return controllers.performance_delete(request, performance_id)
