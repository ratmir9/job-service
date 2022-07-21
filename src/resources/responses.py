from flask import jsonify, request
from flask_restful import Resource

from src.services.auth import token_required
from src.services.responses import ResponseService


class UserResponseDetailApi(Resource):
	response_service = ResponseService()	

	@token_required
	def get(self, user_id, job_id):
		return self.response_service.get_list_response(
			job_id=job_id,
			user_id=user_id
		)
	
	@token_required
	def post(self, user_id, job_id):
		data = request.json
		return self.response_service.add_response(
			job_id=job_id,
			data=data,
			user_id=user_id
		)
