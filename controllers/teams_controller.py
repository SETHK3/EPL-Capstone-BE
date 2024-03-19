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
    except:
        return jsonify({'message': 'unable to fetch teams'}), 500
