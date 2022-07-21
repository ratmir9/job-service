from flask import request
from flask_restful import Resource

from src.services.auth import AuthService


class AuthRegister(Resource):
	auth_service = AuthService()

	def post(self):
		data = request.json
		return self.auth_service.register_new_user(data)


class AuthLogin(Resource):
	auth_service = AuthService()

	def post(self):
		data = request.json
		email = data.get('email', '')
		password = data.get('password', '')
		return self.auth_service.authenticate_user(email, password)