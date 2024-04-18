from flask import Blueprint, request

import controllers

performances = Blueprint('performances', __name__)


@performances.route('/performance', methods=['POST'])
def add_performance():
    return controllers.performance_add(request)


@performances.route('/performances', methods=['GET'])
def performances_get_all():
    return controllers.performances_get_all()


@performances.route('/performance/<performance_id>', methods=['GET'])
def performance_get_by_id(performance_id):
    return controllers.performance_get_by_id(performance_id)


@performances.route('/performances/active', methods=['GET'])
def performances_get_active():
    return controllers.performances_get_active()


@performances.route('/performance/<performance_id>', methods=['PUT'])
def performance_update(performance_id):
    return controllers.performance_update(request, performance_id)


@performances.route('/performance/status/<performance_id>', methods=['PUT'])
def performance_status(performance_id):
    return controllers.performance_status(performance_id)


@performances.route('/performance/delete/<performance_id>', methods=['DELETE'])
def performance_delete(performance_id):
    return controllers.performance_delete(performance_id)
