import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from datetime import datetime


class Transfers(db.Model):
    __tablename__ = "Transfers"

    transfer_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Players.player_id', ondelete="CASCADE"), nullable=False)
    team_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Teams.team_id', ondelete="CASCADE"), nullable=False)
    transfer_date = db.Column(db.DateTime, nullable=False)

    player = db.relationship("Players", foreign_keys='[Players.player_id]', back_populates='transfers')
    teams = db.relationship("Teams", foreign_keys='[Teams.team_id]', back_populates='transfers')

    def __init__(self, player_id, team_id, transfer_date):
        self.player_id = player_id
        self.team_id = team_id
        self.transfer_date = transfer_date

    def new_transfer_obj():
        return Transfers("", "", "")


class TransfersSchema(ma.Schema):
    class Meta:
        fields = ['transfer_id', 'transfer_date', 'player', 'teams']
    player = ma.fields.Nested('PlayerNameSchema')
    teams = ma.fields.Nested('TeamNameSchema')


transfer_schema = TransfersSchema()
transfers_schema = TransfersSchema(many=True)
