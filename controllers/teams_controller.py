from flask import jsonify

from db import db
from lib.authenticate import auth, auth_admin
from models.teams import Teams, team_schema, teams_schema
from util.reflection import populate_object


@auth_admin
def team_add(req):
    post_data = req.form if req.form else req.json

    new_team = Teams.new_team_obj()
    populate_object(new_team, post_data)

    try:
        db.session.add(new_team)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to create new team'}), 400

    return jsonify({'message': 'team created', 'result': team_schema.dump(new_team)}), 201


@auth
def teams_get_all():
    try:
        query = db.session.query(Teams).all()

        if not query:
            return jsonify({'message': 'no teams found'}), 404

        else:
            return jsonify({'message': 'teams found', 'results': teams_schema.dump(query)})
    except Exception as e:
        return jsonify({'message': f'unable to fetch teams: {str(e)}'}), 500


@auth
def team_get_by_id(team_id):
    try:
        team_query = db.session.query(Teams).filter(Teams.team_id == team_id).first()

        return jsonify({'message': f'team found by team_id {team_id}', 'team': team_schema.dump(team_query)}), 200
    except:
        return jsonify({'message': f'no team found with the following id: {team_id}'}), 404


@auth_admin
def team_update(req, team_id):
    post_data = req.form if req.form else req.json

    query = db.session.query(Teams).filter(Teams.team_id == team_id).first()
    if not query:
        return jsonify({'message': f'team with id {team_id} not found'}), 404

    populate_object(query, post_data)

    try:
        db.session.commit()
        return jsonify({'message': 'team updated', 'results': team_schema.dump(query)}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to update team'}), 400


@auth_admin
def team_delete(team_id):
    query = db.session.query(Teams).filter(Teams.team_id == team_id).first()

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'error': 'unable to delete team'}), 400

    return jsonify({'message': 'team successfully deleted'}), 200


@auth_admin
def deactivate_team(team_id):
    try:
        team = db.session.query(Teams).filter(Teams.team_id == team_id).first()

        if not team:
            return jsonify({'message': 'team not found'}), 404

        if team.active is False:
            return jsonify({'message': 'team is already deactivated'}), 400

        team.active = False
        db.session.commit()

        return jsonify({'message': 'team deactivated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'unable to deactivate team', 'error': str(e)}), 400


@auth_admin
def activate_team(team_id):
    try:
        team = db.session.query(Teams).filter(Teams.team_id == team_id).first()

        if not team:
            return jsonify({'message': 'team not found'}), 404

        if team.active is True:
            return jsonify({'message': 'team is already active'}), 400

        team.active = True
        db.session.commit()

        return jsonify({'message': 'team activated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'unable to activate team', 'error': str(e)}), 400


@auth
def teams_get_active():
    try:
        query = db.session.query(Teams).filter(Teams.active).all()

        return jsonify({'message': 'active teams found', 'results': teams_schema.dump(query)}), 200
    except:
        return jsonify({'message': 'no active teams found'}), 500
