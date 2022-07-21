from datetime import (
	datetime, 
	timedelta
)
from functools import wraps

from flask import request
from werkzeug.security import check_password_hash
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from jose import (
	JWTError, 
	jwt
)

from src.services.users import UserService
from src.schemas.users import UserSchema
from src.models.users import User
from src.services.base import BaseService
from config import JWT_EXPIRATION, JWT_SECRET_KEY, JWT_ALGORITHM


class AuthService:
	user_schema = UserSchema()
	user_service = UserService()
	base_service = BaseService()

	@classmethod
	def verify_password(cls, hash, plain_password):
		return check_password_hash(hash, plain_password)

	@classmethod
	def generate_jwt_token(cls, user_data):
		current_datetime = datetime.utcnow()

		payload = {
			'exp': current_datetime + timedelta(seconds=JWT_EXPIRATION),
			'user': {
				'id': user_data['id'],
				'email': user_data['email'],
				'username': user_data['username']
			}
		}
		token = jwt.encode(
			payload,
			JWT_SECRET_KEY,
			algorithm=JWT_ALGORITHM
		)
		return {'token': token}

	@classmethod
	def validate_token(cls, token):
		try:
			payload = jwt.decode(
				token,
				JWT_SECRET_KEY,
				algorithms=JWT_ALGORITHM
			)
			user = payload.get('user', '')
			return user
		except JWTError:
			raise Exception("Could not validate token")

	@classmethod
	def register_new_user(cls, data):
		try:
			user = cls.user_schema.load(data)
		except ValidationError as err:
			return {'msg': str(err)}
		
		new_user = User(**user)
		try:
			res = cls.base_service.create(new_user)
		except IntegrityError:
			cls.base_service.session.rollback()
			return {'msg': 'user such exist'}, 400
		return {
			"msg": 'Success',
			'user': cls.user_schema.dump(res)
		}, 201

	@classmethod
	def authenticate_user(cls, email, password):
		user = cls.user_service.get_user_by_email(email)
		if not user:
			return {'msg': 'user not found'}
		if not user or not cls.verify_password(hash=user.password_hash, plain_password=password):
			return {'msg': 'data is wrong'}
		user_data = {
			'id': user.id,
			'email': user.email,
			'username': user.username
		}
		return cls.generate_jwt_token(user_data)	


def token_required(func):
	@wraps(func)
	def wrapper(self, *args, **kwargs):
		token = request.headers.get('Authorization', '')
		if not token:
			return '', 401, {"WWW-Authenticate": "Basic realm='Authenticate required'"}
		try:
			user = AuthService.validate_token(token)
		except Exception as err:
			return {'msg': str(err)}, 401, {'BAD-Authenticate': 'Bearer'}
		user = UserService().get_user_by_email(email=user['email'])
		if not user:
			return {'msg': 'user not found'}, 401
		user_id = user.id
		return func(self, user_id, **kwargs)
	return wrapper
