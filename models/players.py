import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Players(db.Model):
    __tablename__ = "Players"

    player_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_name = db.Column(db.String(), nullable=False)
    nationality = db.Column(db.String(), nullable=False)
    date_of_birth = db.Column(db.String(), nullable=False)
    position = db.Column(db.String(), nullable=False)
    team_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Teams.team_id"), nullable=False)

    team = db.relationship("Teams", foreign_keys='[Players.team_id]', back_populates='players')

    def __init__(self, player_name, nationality, date_of_birth, position, team_id):
        self.player_name = player_name
        self.nationality = nationality
        self. date_of_birth = date_of_birth
        self.position = position
        self.team_id = team_id

    def new_player_obj():
        return Players("", "", "", "", "")


class PlayersSchema(ma.Schema):
    class Meta:
        fields = ['player_name', 'nationality', 'date_of_birth', 'position', 'team', 'stats']
    team = ma.fields.Nested("TeamsSchema", exclude=[''])
    stats = ma.fields.Nested("PerformanceSchema", exclude=[''])


player_schema = PlayersSchema()
players_schema = PlayersSchema(many=True)
