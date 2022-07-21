from datetime import datetime
from werkzeug.security import generate_password_hash

from src import db


class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64))
  email = db.Column(db.String, unique=True)
  password_hash = db.Column(db.String)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)

  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.password_hash = generate_password_hash(password)
    self.created_at = datetime.utcnow()

  