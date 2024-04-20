from flask import jsonify

from db import db
from lib.authenticate import auth, auth_admin
from models.transfers import Transfers, transfer_schema, transfers_schema
from util.reflection import populate_object


@auth_admin
def transfer_add(req):
    post_data = req.form if req.form else req.json

    new_transfer = Transfers.new_transfer_obj()
    populate_object(new_transfer, post_data)

    try:
        db.session.add(new_transfer)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to create new transfer'}), 400

    return jsonify({'message': 'transfer created', 'result': transfer_schema.dump(new_transfer)}), 201


@auth
def transfers_get_all():
    try:
        query = db.session.query(Transfers).all()

        if not query:
            return jsonify({'message': 'no transfers found'}), 404

        else:
            return jsonify({'message': 'transfers found', 'results': transfers_schema.dump(query)})
    except:
        return jsonify({'message': 'unable to fetch transfers'}), 500


@auth
def transfer_get_by_id(transfer_id):
    try:
        transfer_query = db.session.query(Transfers).filter(Transfers.transfer_id == transfer_id).first()

        return jsonify({'message': f'transfer found', 'transfer': transfer_schema.dump(transfer_query)}), 200
    except:
        return jsonify({'message': f'no transfer found with the following id: {transfer_id}'}), 404


@auth
def transfers_get_active():
    try:
        query = db.session.query(Transfers).filter(Transfers.active).all()

        return jsonify({'message': 'active transfers found', 'results': transfers_schema.dump(query)}), 200
    except:
        return jsonify({'message': 'no active transfers found'}), 500


@auth_admin
def transfer_update(req, transfer_id):
    post_data = req.form if req.form else req.json

    query = db.session.query(Transfers).filter(Transfers.transfer_id == transfer_id).first()
    if not query:
        return jsonify({'message': f'transfer with id {transfer_id} not found'}), 404

    populate_object(query, post_data)

    try:
        db.session.commit()
        return jsonify({'message': 'transfer updated', 'results': transfer_schema.dump(query)}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to update transfer'}), 400


@auth_admin
def transfer_status(transfer_id):
    try:
        transfer = db.session.query(Transfers).filter(Transfers.transfer_id == transfer_id).first()

        if transfer:
            transfer.active = not transfer.active
            db.session.commit()
            return jsonify({'message': 'transfer status updated successfully', 'results': transfer_schema.dump(transfer)}), 200

        return jsonify({'message': 'transfer not found'}), 404

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'unable to activate transfer', 'error': str(e)}), 400


@auth_admin
def transfer_delete(transfer_id):
    query = db.session.query(Transfers).filter(Transfers.transfer_id == transfer_id).first()

    try:
        db.session.delete(query)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'unable to delete transfer: {str(e)}'}), 400

    return jsonify({'message': 'transfer successfully deleted'}), 200
