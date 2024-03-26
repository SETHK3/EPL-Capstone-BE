import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Performances(db.Model):
    __tablename__ = "Performances"

    performance_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Players.player_id"), nullable=False)
    goals_scored = db.Column(db.String())
    assists = db.Column(db.String())
    yellow_cards = db.Column(db.String())
    red_cards = db.Column(db.String())

    player = db.relationship("Players", back_populates='performance')

    def __init__(self, player_id, goals_scored, assists, yellow_cards, red_cards):
        self.player_id = player_id
        self.goals_scored = goals_scored
        self.assists = assists
        self.yellow_cards = yellow_cards
        self.red_cards = red_cards

    def new_performance_obj():
        return Performances("", "", "", "", "")


class PerformancesSchema(ma.Schema):
    class Meta:
        fields = ['performance_id', 'player', 'player_id', 'goals_scored', 'assists', 'yellow_cards', 'red_cards']
    player = ma.fields.Nested("PlayerNameSchema")


performance_schema = PerformancesSchema()
performances_schema = PerformancesSchema(many=True)
