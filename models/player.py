import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from .player_transfer_xref import transfer_table


class Players(db.Model):
    __tablename__ = "Players"

    player_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    nationality = db.Column(db.String(), nullable=False)
    date_of_birth = db.Column(db.String(), nullable=False)
    position = db.Column(db.String(), nullable=False)
    team_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Teams.team_id"), nullable=True)
    active = db.Column(db.Boolean, default=True)

    team = db.relationship("Teams", foreign_keys='[Players.team_id]', back_populates='players')
    performance = db.relationship("Performances", foreign_keys='[Performances.player_id]', back_populates='player')
    transfers = db.relationship("Transfers", secondary=transfer_table, back_populates='player')

    def __init__(self, first_name, last_name, nationality, date_of_birth, position, team_id, transfer_id, active):
        self.first_name = first_name
        self.last_name = last_name
        self.nationality = nationality
        self. date_of_birth = date_of_birth
        self.position = position
        self.team_id = team_id
        self.transfer_id = transfer_id
        self.active = active

    def new_player_obj():
        return Players("", "", "", "", "", "", "", True)


class PlayersSchema(ma.Schema):
    class Meta:
        fields = ['player_id', 'first_name', 'last_name', 'nationality', 'date_of_birth', 'position', 'team', 'stats', 'active']
    team = ma.fields.Nested("TeamNameSchema")
    stats = ma.fields.Nested("PerformanceSchema", exclude=['player'])


player_schema = PlayersSchema()
players_schema = PlayersSchema(many=True)


class PlayerNameSchema(ma.Schema):
    class Meta:
        fields = ['first_name', 'last_name']


player_name_schema = PlayerNameSchema()
players_name_schema = PlayerNameSchema(many=True)
