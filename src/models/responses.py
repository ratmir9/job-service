from datetime import datetime

from sqlalchemy.orm import backref

from src import db


class Response(db.Model):
	__tablename__ = 'responses'
	__table_args__ = (
		db.UniqueConstraint('job_id', 'resume_id'),
	)

	id = db.Column(db.Integer, primary_key=True)
	job_id = db.Column(db.ForeignKey('jobs.id'), nullable=False)
	resume_id = db.Column(db.ForeignKey('resumes.id'), nullable=False)
	response_at = db.Column(db.DateTime, default=datetime.utcnow)
	job = db.relationship(
		'Job',
		backref=backref('responses', cascade='all, delete-orphan')
	)
	resume = db.relationship(
		'Resume',
		backref=backref('responses', cascade='all, delete-orphan')
	)
	
