import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Teams(db.Model):
    __tablename__ = "Teams"

    team_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_name = db.Column(db.String(), nullable=False)
    location = db.Column(db.String(), nullable=False)
    stadium_name = db.Column(db.String(), nullable=False)
    manager_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Managers.manager_id"), nullable=True)
    active = db.Column(db.Boolean, default=True)

    players = db.relationship("Players", foreign_keys='[Players.team_id]', back_populates='team')
    manager = db.relationship("Managers", foreign_keys='[Teams.manager_id]', back_populates='team')
    transfers = db.relationship("Transfers", back_populates='teams')

    def __init__(self, team_name, location, stadium_name, manager_id, active):
        self.team_name = team_name
        self.location = location
        self.stadium_name = stadium_name
        self.manager_id = manager_id
        self.active = active

    def new_team_obj():
        return Teams("", "", "", "", True)


class TeamsSchema(ma.Schema):
    class Meta:
        fields = ['team_id', 'team_name', 'location', 'stadium_name', 'manager', 'players', 'active']
    players = ma.fields.Nested("PlayerNameSchema", many=True)
    manager = ma.fields.Nested("ManagerNameSchema")


team_schema = TeamsSchema()
teams_schema = TeamsSchema(many=True)


class TeamNameSchema(ma.Schema):
    class Meta:
        fields = ['team_name', 'team_id']


team_name_schema = TeamNameSchema()
team_names_schema = TeamNameSchema(many=True)
