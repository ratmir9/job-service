from flask import jsonify, make_response
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from src.services.base import BaseService
from src.schemas.resumes import ResumeSchema
from src.models.resumes import Resume


class ResumeService(BaseService):
	resume_schema = ResumeSchema()

	def _get_resume_by_id(self, resume_id):
		resume = self.get_obj_by_id(Resume, resume_id)
		if not resume:
			return ""
		return resume
	
	def _check_valid_data(self, obj):
		return self.resume_schema.load(obj)

	def get_all_resumes(self):
		resumes = self.get_all_obj(Resume)
		return make_response(jsonify(self.resume_schema.dump(resumes, many=True)), 200)
	
	def get_all_resume_for_user(self, user_id):
		resumes = (
			self.session
			.query(Resume)
			.filter_by(owner_id=user_id)
			.all()
		)
		return make_response(jsonify(self.resume_schema.dump(resumes, many=True)), 200)

	def get_resume_by_id(self, resume_id):
		resume = self._get_resume_by_id(resume_id)
		if not resume:
			return "", 404
		return self.resume_schema.dump(resume)


	def create_new_resume(self, data, user_id):
		try:
			resume = self.resume_schema.load(data)
		except ValidationError as err:
			return {'msg': str(err)}
		new_resume = Resume(**resume, owner_id=user_id)
		try:
			result = self.create(obj=new_resume)
		except IntegrityError:
			self.session.rollback()
			return {'msg': 'resume already exist'}, 400
		return make_response(jsonify(self.resume_schema.dump(result)), 201)

	def update_data_resume(self, resume_id, resume_data, user_id):
		resume = self._get_resume_by_id(resume_id=resume_id)
		if not resume:
			return {'msg': f'not resume with {resume_id}'}, 404
		if not self.check_user_in_owner(instance=resume, user_id=user_id):
			return {"msg": "you don't have access"}, 403
		try:
			resume_update = self._check_valid_data(resume_data)
		except ValidationError as err:
			return {'msg': str(err)}, 400
		self.update(
			id=resume_id,
			table_name=Resume, 
			obj_data=self.resume_schema.dump(resume_update)
		)
		return {'msg': 'Successfully update'}, 200
	
	def delete_resume(self, resume_id, user_id):
		resume = self._get_resume_by_id(resume_id)
		if not resume:
			return {'msg': f'not found resume with id {resume_id}'}, 404
		if not self.check_user_in_owner(resume, user_id):
			return {"msg":"you don't have access" }, 403
		self.delete_obj(resume)
		return '', 204

