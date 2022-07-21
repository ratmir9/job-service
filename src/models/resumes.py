from datetime import datetime
from enum import Enum

from sqlalchemy.orm import backref

from src import db


class GenderEnum(Enum):
	man = 'man'
	woman = 'woman'


class Resume(db.Model):
	__tablename__ = 'resumes'
	__table_args__ = (
		db.UniqueConstraint(
			'first_name', 'last_name','about_me',
			'gender', 'birth_day', 'owner_id', 'speciality', 'position'
		),
	)

	id = db.Column(db.Integer, primary_key=True)
	last_name = db.Column(db.String(64), nullable=False)
	first_name = db.Column(db.String(64), nullable=False)
	about_me = db.Column(db.String)
	speciality = db.Column(db.String(255))
	position = db.Column(db.String(255))
	gender = db.Column(db.Enum(GenderEnum), nullable=False)
	birth_day = db.Column(db.Date, nullable=False)
	owner_id = db.Column(db.ForeignKey('users.id'), nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	owner = db.relationship(
		'User',
		backref=backref('resumes', cascade="all, delete-orphan")
	)
