from flask import jsonify

from db import db
from lib.authenticate import auth, auth_admin
from models.player_transfer_xref import transfer_table
from models.team import Teams
from models.player import Players, player_schema, players_schema
from util.reflection import populate_object


@auth_admin
def player_add(req):
    post_data = req.form if req.form else req.json

    new_player = Players.new_player_obj()
    populate_object(new_player, post_data)

    try:
        db.session.add(new_player)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'unable to create player', 'error': str(e)}), 400

    return jsonify({'message': 'player created', 'result': player_schema.dump(new_player)}), 201


@auth
def players_get_all():
    try:
        query = db.session.query(Players).all()

        if not query:
            return jsonify({'message': 'no players found'}), 404

        else:
            return jsonify({'message': 'players found', 'results': players_schema.dump(query)}), 200
    except Exception as e:
        return jsonify({'message': 'unable to fetch players', 'error': str(e)}), 500


@auth
def players_get_by_team_id(team_id):
    try:
        query = db.session.query(Players).filter(Players.team_id == team_id).all()

        return jsonify({'message': f'players found by team_id {team_id}', 'results': players_schema.dump(query)}), 200
    except Exception as e:
        return jsonify({'message': f'no players found with the following id: {team_id}', 'error': str(e)}), 404


@auth
def player_get_by_id(player_id):
    try:
        query = db.session.query(Players).filter(Players.player_id == player_id).first()

        return jsonify({'message': f'player found by player_id: {player_id}', 'results': player_schema.dump(query)}), 200
    except Exception as e:
        return jsonify({'message': f'no player found with the following id: {player_id}', 'error': str(e)}), 404


@auth
def players_get_active():
    try:
        query = db.session.query(Players).filter(Players.active).all()

        return jsonify({'message': 'active players found', 'results': players_schema.dump(query)}), 200
    except Exception as e:
        return jsonify({'message': 'no active players found', 'error': str(e)}), 500


@auth_admin
def player_update(req, player_id):
    post_data = req.form if req.form else req.json
    query = db.session.query(Players).filter(Players.player_id == player_id).first()
    if not query:
        return jsonify({'message': f'player with id {player_id} not found'}), 404

    populate_object(query, post_data)

    try:
        db.session.commit()
        return jsonify({'message': 'player updated', 'results': player_schema.dump(query)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'unable to update player record', 'error': str(e)}), 400


@auth_admin
def player_status(player_id):
    try:
        player = db.session.query(Players).filter(Players.player_id == player_id).first()

        if player:
            player.active = not player.active
            db.session.commit()
            return jsonify({'message': 'player status updated successfully', 'results': player_schema.dump(player)}), 200

        return jsonify({'message': 'player not found'}), 404

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'unable to activate player', 'error': str(e)}), 400


@auth_admin
def player_delete(player_id):
    player_query = db.session.query(Players).filter(Players.player_id == player_id).first()

    try:
        db.session.delete(player_query)
        db.session.commit()

        return jsonify({'message': f'player with player_id {player_id} was deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'player with player_id {player_id} could not be deleted', 'error': str(e)}), 400
