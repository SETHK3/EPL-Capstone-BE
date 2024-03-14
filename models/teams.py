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
    manager_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Managers.manager_id"), nullable=False)

    players = db.relationship("Players", foreign_keys='[Players.team_id]', back_populates='team')
