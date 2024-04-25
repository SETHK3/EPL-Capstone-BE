from flask import jsonify
from datetime import datetime, timezone

from db import db
from lib.authenticate import auth, auth_admin
from models.transfer import Transfers, transfer_schema, transfers_schema
from models.player import Players
from models.team import Teams
from util.reflection import populate_object


@auth_admin
def transfer_add(req):
    post_data = req.form if req.form else req.json
    player_id = post_data.get("player_id")
    team_id = post_data.get("team_id")

    player = db.session.query(Players).filter(Players.player_id == player_id).first()
    team = db.session.query(Teams).filter(Teams.team_id == team_id).first()

    new_transfer = Transfers.new_transfer_obj()
    populate_object(new_transfer, post_data)

    new_transfer.transfer_date = datetime.now(timezone.utc)
    new_transfer.player.append(player)

    if new_transfer.teams is None:
        new_transfer.teams = [team]
    else:
        new_transfer.teams.append(team)

    player.team = new_transfer.teams

    try:
        db.session.add(new_transfer)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'unable to create new transfer record', 'error': str(e)}), 400

    return jsonify({'message': 'transfer record created', 'result': transfer_schema.dump(new_transfer)}), 201


@auth
def transfers_get_all():
    try:
        query = db.session.query(Transfers).all()

        if not query:
            return jsonify({'message': 'no transfer records found'}), 404

        else:
            return jsonify({'message': 'transfer record found', 'results': transfers_schema.dump(query)})
    except Exception as e:
        return jsonify({'message': 'unable to fetch transfer records', 'error': str(e)}), 500


@auth
def transfer_get_by_id(transfer_id):
    try:
        transfer_query = db.session.query(Transfers).filter(Transfers.transfer_id == transfer_id).first()

        return jsonify({'message': f'transfer record found', 'transfer': transfer_schema.dump(transfer_query)}), 200
    except Exception as e:
        return jsonify({'message': f'no transfer record found with the following id: {transfer_id}', 'error': str(e)}), 404


@auth
def transfers_get_active():
    try:
        query = db.session.query(Transfers).filter(Transfers.active).all()

        return jsonify({'message': 'active transfer records found', 'results': transfers_schema.dump(query)}), 200
    except Exception as e:
        return jsonify({'message': 'no active transfer records found', 'error': str(e)}), 500


@auth_admin
def transfer_update(req, transfer_id):
    post_data = req.form if req.form else req.json

    player_id = post_data.get("player_id")
    team_id = post_data.get("team_id")

    player = db.session.query(Players).filter(Players.player_id == player_id).first()
    team = db.session.query(Teams).filter(Teams.team_id == team_id).first()

    query = db.session.query(Transfers).filter(Transfers.transfer_id == transfer_id).first()
    if not query:
        return jsonify({'message': f'transfer record with id {transfer_id} not found'}), 404

    if not player:
        return jsonify({'message': f'player with id {player_id} not found'}), 404

    if not team:
        return jsonify({'message': f'team with id {team_id} not found'}), 404

    populate_object(query, post_data)

    try:
        db.session.commit()
        return jsonify({'message': 'transfer record updated', 'results': transfer_schema.dump(query)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'unable to update transfer record', 'error': str(e)}), 400


@auth_admin
def transfer_status(transfer_id):
    try:
        transfer = db.session.query(Transfers).filter(Transfers.transfer_id == transfer_id).first()

        if transfer:
            transfer.active = not transfer.active
            db.session.commit()
            return jsonify({'message': 'transfer record status updated successfully', 'results': transfer_schema.dump(transfer)}), 200

        return jsonify({'message': 'transfer record not found'}), 404

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
        return jsonify({'error': f'unable to delete transfer record: {str(e)}'}), 400

    return jsonify({'message': 'transfer record successfully deleted'}), 200
