from flask import make_response

from src import db
from src.schemas.users import UserSchema
from src.models.users import User
from src.services.base import BaseService 


class UserService(BaseService):
	user_schema = UserSchema()

	def get_user_by_id(self, id):
		user = self.get_obj_by_id(User, id)
		if not user:
			return {'msg':"user not found"}, 404
		return self.user_schema.dump(user), 200
	
	def get_user_by_username(self, username):
		user = db.session.query(User).where(username==username).one()
		if not user:
			return {'msg': 'user not found'}, 404
		return user

	def get_user_by_email(self, email):
		user = (
			db.session
			.query(User)
			.filter_by(email=email)
			.first()
		)
		if not user:
			return ""
		return user

	def delete_user(self, user_id, id):
		user = self.get_obj_by_id(User, id)
		if not user:
			return {'msg': 'user not found'}, 404
		if not user.id == user_id:
			return {"msg": "you don't have access"}, 403
		self.delete_obj(user)
		return '', 204

