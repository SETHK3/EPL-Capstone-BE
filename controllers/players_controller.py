from flask import jsonify

from db import db
from lib.authenticate import auth, auth_admin
from models.transfer_xref import transfer_table
from models.teams import Teams
from models.players import Players, player_schema, players_schema
from util.reflection import populate_object


@auth_admin
def player_add(req):
    post_data = req.form if req.form else req.json

    new_player = Players.new_player_obj()
    populate_object(new_player, post_data)

    try:
        db.session.add(new_player)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to create player'}), 400

    return jsonify({'message': 'player created', 'result': player_schema.dump(new_player)}), 201


@auth
def players_get_all():
    try:
        query = db.session.query(Players).all()

        if not query:
            return jsonify({'message': 'no players found'}), 404

        else:
            return jsonify({'message': 'players found', 'results': players_schema.dump(query)}), 200
    except:
        return jsonify({'message': 'unable to fetch players'}), 500


@auth
def players_get_active():
    try:
        query = db.session.query(Players).filter(Players.active).all()

        return jsonify({'message': 'active players found', 'results': players_schema.dump(query)}), 200
    except:
        return jsonify({'message': 'no active players found'}), 500


@auth
def players_get_by_team_id(team_id):
    try:
        query = db.session.query(Players).filter(Players.team_id == team_id).all()

        return jsonify({'message': f'players found by team_id {team_id}', 'results': players_schema.dump(query)}), 200
    except:
        return jsonify({'message': f'no players found with the following id: {team_id}'}), 404


@auth
def player_get_by_id(player_id):
    try:
        query = db.session.query(Players).filter(Players.player_id == player_id).first()

        return jsonify({'message': f'player found by player_id: {player_id}', 'results': player_schema.dump(query)}), 200
    except:
        return jsonify({'message': f'no player found with the following id: {player_id}'}), 404


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
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to update player record'}), 400


@auth_admin
def player_delete(req, player_id):
    player_query = db.session.query(Players).filter(Players.player_id == player_id).first()

    try:
        db.session.delete(player_query)
        db.session.commit()

        return jsonify({'message': f'player with player_id {player_id} was deleted'}), 200
    except:
        db.session.rollback()
        return jsonify({'message': f'player with player_id {player_id} could not be deleted'}), 400


@auth_admin
def player_add_transfer(req):
    post_data = req.form if req.form else req.json

    player_id = post_data.get('player_id')
    team_id = post_data.get('team_id')

    player_query = db.session.query(Players).filter(Players.player_id == player_id).first()
    team_query = db.session.query(Teams).filter(Teams.team_id == team_id).first()

    player_query.teams.append(team_query)

    try:
        db.session.commit()
        return jsonify({'message': 'player transferred successfully', 'result': player_schema.dump(player_query)}), 201
    except:
        db.session.rollback()
        return jsonify({'message': 'error recognizing transfer'}), 400


@auth_admin
def player_remove_transfer(req, player_id, team_id):
    try:
        player_query = db.session.query(Players).filter(Players.player_id == player_id).first()
        team_query = db.session.query(Teams).filter(Teams.team_id == team_id).first()

        player_query.categories.remove(team_query)

        db.session.commit()

        return jsonify({'message': 'player transferred back to parent club successfully'}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to undo transfer'}), 400
