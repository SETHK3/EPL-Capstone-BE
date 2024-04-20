from flask import Blueprint, request

import controllers

transfers = Blueprint('transfers', __name__)


@transfers.route('/transfer', methods=['POST'])
def add_transfer():
    return controllers.transfer_add(request)


@transfers.route('/transfers', methods=['GET'])
def transfers_get_all():
    return controllers.transfers_get_all()


@transfers.route('/transfer/<transfer_id>', methods=['GET'])
def transfer_get_by_id(transfer_id):
    return controllers.transfer_get_by_id(transfer_id)


@transfers.route('/transfers/active', methods=['GET'])
def transfers_get_active():
    return controllers.transfers_get_active()


@transfers.route('/transfer/<transfer_id>', methods=['PUT'])
def transfer_update(transfer_id):
    return controllers.transfer_update(request, transfer_id)


@transfers.route('/transfer/status/<transfer_id>', methods=['PUT'])
def transfer_status(transfer_id):
    return controllers.transfer_status(transfer_id)


@transfers.route('/transfer/delete/<transfer_id>', methods=['DELETE'])
def transfer_delete(transfer_id):
    return controllers.transfer_delete(transfer_id)
