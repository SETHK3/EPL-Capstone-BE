from db import db

transfer_table = db.Table(
    "TransferHistory",
    db.Model.metadata,
    db.Column('transfer_id', db.ForeignKey('Transfers.transfer_id', ondelete="CASCADE"), primary_key=True),
    db.Column('player_id', db.ForeignKey('Players.player_id', ondelete="CASCADE"), primary_key=True)
)
