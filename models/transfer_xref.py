from db import db

transfer_table = db.Table(
    "Transfers",
    db.Model.metadata,
    db.Column('team_id', db.ForeignKey('Teams.team_id', ondelete="CASCADE"), primary_key=True),
    db.Column('player_id', db.ForeignKey('Players.player_id', ondelete="CASCADE"), primary_key=True)
)
