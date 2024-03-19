import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Managers(db.Model):
    __tablename__ = "Managers"

    manager_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manager_name = db.Column(db.String(), nullable=False)
    nationality = db.Column(db.String(), nullable=False)
    date_of_birth = db.Column(db.String(), nullable=False)

    team = db.relationship("Teams", foreign_keys='[Teams.manager_id]', back_populates='manager')

    def __init__(self, manager_name, nationality, date_of_birth):
        self.manager_name = manager_name
        self.nationality = nationality
        self.date_of_birth = date_of_birth

    def new_manager_obj():
        return Managers("", "", "")


class ManagersSchema(ma.Schema):
    class Meta:
        fields = ['manager_name', 'nationality', 'date_of_birth']
    team = ma.fields.Nested("TeamsSchema", exclude=[''])


manager_schema = ManagersSchema()
managers_schema = ManagersSchema(many=True)
