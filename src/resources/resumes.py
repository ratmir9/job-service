from flask import jsonify, request
from flask_restful import Resource

from src.services.resumes import ResumeService
from src.services.auth import token_required


class ResumeApi(Resource):
	resume_service = ResumeService()

	@token_required
	def get(self, user_id):
		return self.resume_service.get_all_resume_for_user(user_id)

	@token_required
	def post(self, user_id):
		data = request.json
		return self.resume_service.create_new_resume(
		 	data=data,
		 	user_id=user_id
		)


class ResumeDetailApi(Resource):
	resume_service = ResumeService()

	@token_required
	def get(self, user_id, resume_id):
		return self.resume_service.get_resume_by_id(resume_id)
	
	@token_required
	def put(self, user_id, resume_id):
		resume_data = request.json
		return self.resume_service.update_data_resume(
			resume_id=resume_id,
			resume_data=resume_data,
			user_id=user_id
		)
	
	@token_required
	def delete(self, user_id, resume_id):
		return self.resume_service.delete_resume(
			resume_id=resume_id,
			user_id=user_id
		)
