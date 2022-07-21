from flask import (
	jsonify,
	make_response
)

from marshmallow import ValidationError
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from src import db
from src.services.base import BaseService
from src.schemas.jobs import JobSchema
from src.models.jobs import Job


class JobService(BaseService):
	job_schema = JobSchema()

	def _check_valid_data(self, obj):
		return self.job_schema.load(obj)

	def get_job_by_id(self, id):
		job = self.get_obj_by_id(Job, id)
		if not job:
			return "", 404
		return make_response(jsonify(self.job_schema.dump(job)), 200)	
	
	def search_jobs(self, query_params):
		title = query_params.get('title', '')
		salary_from = query_params.get('salary_from', 0)
		salary_to = query_params.get('salary_to', 0)
		if title:
			if title and salary_from:
				return self.get_jobs_by_title_and_with_salary_from(title, salary_from)
			if title and salary_to:
				return self.get_jobs_by_title_and_with_salary_up_to(title, salary_to)
			if title and salary_from and salary_to:
				return self.get_jobs_by_title_and_with_between_salary(title, salary_from, salary_to)
			return self.get_jobs_by_title(title)
		if salary_from:
			if salary_from and salary_to:
				return self.get_job_between_salary(salary_from, salary_to)
			return self.get_jobs_with_salary_from(salary_from)
		if salary_to:
			return self.get_jobs_with_salary_up_to(salary_to)

	def get_all_jobs(self):
		jobs = (
			self.session
			.query(Job)
			.all()
		)
		return make_response(jsonify(self.job_schema.dump(jobs, many=True)), 200)

	def get_jobs_by_title(self, title):
		print(func.lower(title))
		jobs = (
			self.session
			.query(Job)
			.filter(
				func.lower(Job.title) == func.lower(title)
			).all()
		)
		return make_response(jsonify(self.job_schema.dump(jobs, many=True)), 200)
	
	def get_jobs_by_title_and_with_salary_from(self, title, salary_from):
		jobs = (
			self.session
			.query(Job)
			.filter(
				func.lower(Job.title) == func.lower(title)
			).filter(
				Job.salary_from >= salary_from
			).all()
		)
		return make_response(jsonify(self.job_schema.dump(jobs, many=True)), 200)

	def get_jobs_by_title_and_with_salary_up_to(self, title,  salary_to):
		jobs = (
			self.session
			.query(Job)
			.filter(
				func.lower(Job.title) == func.lower(title)
			).filter(
				Job.salary_to <= salary_to
			).all()
		)
		return make_response(jsonify(self.job_schema.dump(jobs, many=True)), 200)
	
	def get_jobs_by_title_and_with_between_salary(self, title, salary_from, salary_to):
		jobs = (
			self.session
			.query(Job)
			.filter(
				func.lower(Job.title) == func.lower(title)
			).filter(
				Job.salary_from >= salary_from,
				Job.salary_to <= salary_to
			).all())
		return make_response(jsonify(self.job_schema.dump(jobs, many=True)), 200)

	def get_jobs_with_salary_from(self, salary_from):
		jobs = (
			self.session
			.query(Job)
			.filter(
				Job.salary_from >= salary_from
			).all()
		)
		return make_response(jsonify(self.job_schema.dump(jobs, many=True)), 200)

	def get_job_between_salary(self, salary_from, salary_to):
		jobs = (
			self.session
			.query(Job)
			.filter(
				Job.salary_from >= salary_from,
				Job.salary_to <= salary_to
			).all()
		)
		return make_response(jsonify(self.job_schema.dump(jobs, many=True)), 200)
	
	def get_jobs_with_salary_up_to(self, salary_to):
		jobs = (
			self.session
			.query(Job)
			.filter(
				Job.salary_to <= salary_to
			).all()
		)
		return make_response(jsonify(self.job_schema.dump(jobs, many=True)), 200)
	
	def get_list_job_for_user(self, user_id):
		jobs = (
			db.session
			.query(Job)
			.filter_by(owner_id=user_id)
			.all()
		)
		return make_response(jsonify(self.job_schema.dump(jobs, many=True)), 200) 

	def add_job(self, job_data, user_id):
		try:
			job = self._check_valid_data(job_data)
		except ValidationError as err:
			return {'msg': str(err)}
		new_job = Job(**job, owner_id=user_id)
		try:
			result = self.create(obj=new_job)
		except IntegrityError:
			self.session.rollback()
			return {'msg': 'such exist'}, 400
		return make_response(jsonify({
			'msg': 'success',
			'job': self.job_schema.dump(result)
		}), 201)
	
	def update_data_job(self, user_id, job_id, data_job):
		job = self.get_obj_by_id(Job, id=job_id)
		if not job:
			return {'msg': f'not job with id = {job_id}'}, 404
		if not self.check_user_in_owner(instance=job, user_id=user_id):
			return make_response(jsonify({"msg": "you don't have access"}), 403)
		try:
			job_update = self._check_valid_data(data_job)
		except ValidationError as err:
			return {'msg': str(err)}, 400
		self.update(
			id=job_id,
			table_name=Job, 
			obj_data=self.job_schema.dump(job_update)
		)
		return {'msg': 'updated successefully'}, 200

	def delete_job(self, user_id, job_id):
		job = self.get_obj_by_id(Job, id=job_id)
		if not job:
			return {'msg': f'job with id {job_id} not found'}, 404
		if not self.check_user_in_owner(instance=job, user_id=user_id):
			return {"msg": "you don't have access"}, 403
		self.delete_obj(job)
		return '', 204
