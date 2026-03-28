import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()

class Group(db.Model):
    __tablename__ = 'groups'
    code = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group = db.Column(db.String(100), nullable=False)
    esta_activo = db.Column(db.Boolean, default=True)

    persons = db.relationship('Person', backref='group', lazy=True)

class Person(db.Model):
    __tablename__ = 'persons'
    code = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    names = db.Column(db.String(100), nullable=False)
    last_names = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    cellphone = db.Column(db.String(20))
    address = db.Column(db.Text)
    observations = db.Column(db.Text)
    photograph = db.Column(db.Text)  # base64 string
    esta_activo = db.Column(db.Boolean, default=True)

    group_id = db.Column(UUID(as_uuid=True), db.ForeignKey('groups.code'), nullable=False)