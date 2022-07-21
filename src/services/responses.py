from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from src.services.base import BaseService
from src.schemas.responses import ResponseSchema
from src.models.responses import Response
from src.models.resumes import Resume
from src.models.jobs import Job


class ResponseService(BaseService):
	response_schema = ResponseSchema()
	
	def get_list_response(self, user_id, job_id):
		job = self.get_obj_by_id(Job, job_id)
		if not job:
			return {'msg': 'not job'}
		if not self.check_user_in_owner(instance=job, user_id=user_id):
			return {"msg" : "I don't have access"}
		
		resumes = (
			self.session()
			.query(Resume)
			.filter(Response.job_id == job_id)
			.join(Response, Resume.id == Response.resume_id)
			.all()
		)
		return self.response_schema.dump(
			{
				'job_id': job_id,
				'resumes': resumes
			}
		)	

	def add_response(self,job_id, data, user_id):
		job =  self.get_obj_by_id(Job, job_id)
		if not job:
			return {'msg': f'not job with id {job_id}'}, 404
		try:
			self.response_schema.load(data)
		except ValidationError as err:
			return {'msg': str(err)}, 400
		
		resume_id = data.get('resume_id', '') 
		resume = self.get_obj_by_id(Resume, resume_id)
		if not resume:
			return {'msg': 'resume not found'}, 404 
		if not self.check_user_in_owner(instance=resume, user_id=user_id):
			return {"msg": "I don't have access"}, 403
		
		new_response = Response(job_id=job_id, resume_id=resume_id)
		
		try:
			self.create(new_response)
		except IntegrityError:
			self.session.rollback()
			return {'msg': 'you already responded'}, 200
		return {'msg': 'success'}, 201
		
	
