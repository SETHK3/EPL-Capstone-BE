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
    active = db.Column(db.Boolean, default=True)

    team = db.relationship("Teams", foreign_keys='[Teams.manager_id]', back_populates='manager')

    def __init__(self, manager_name, nationality, date_of_birth, active):
        self.manager_name = manager_name
        self.nationality = nationality
        self.date_of_birth = date_of_birth
        self.active = active

    def new_manager_obj():
        return Managers("", "", "", True)


class ManagersSchema(ma.Schema):
    class Meta:
        fields = ['manager_id', 'manager_name', 'nationality', 'date_of_birth', 'team', 'active']
    team = ma.fields.Nested("TeamNameSchema", many=True)


manager_schema = ManagersSchema()
managers_schema = ManagersSchema(many=True)


class ManagerNameSchema(ma.Schema):
    class Meta:
        fields = ['manager_name']


manager_name_schema = ManagerNameSchema()
manager_names_schema = ManagerNameSchema(many=True)
