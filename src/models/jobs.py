from datetime import datetime

from sqlalchemy.orm import backref

from src import db


class Job(db.Model):
  __tablename__ = 'jobs'

  __table_args__ = (
    db.UniqueConstraint('title', 'owner_id'),
  )
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(255), nullable=False)
  description = db.Column(db.String, nullable=False)
  salary_from = db.Column(db.Integer)
  is_active = db.Column(db.Boolean, default=True) 
  salary_to = db.Column(db.Integer)
  owner_id = db.Column(db.ForeignKey('users.id'), nullable=False)
  owner = db.relationship(
    'User',
    backref=backref("jobs", cascade="all, delete-orphan")
  )
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
  
