from flask import jsonify, request
from flask_restful import Resource

from src.services.jobs import JobService
from src.services.auth import token_required


class UserJobApi(Resource):
  job_service = JobService()

  @token_required
  def get(self, user_id):
    return self.job_service.get_list_job_for_user(user_id)

  @token_required  
  def post(self, user_id):
    data = request.json
    return self.job_service.add_job(data, user_id)

  
class UserJobDetailApi(Resource):
  job_service = JobService()

  @token_required
  def put(self, user_id, job_id):
    data = request.json
    return self.job_service.update_data_job(
      user_id=user_id,
      job_id=job_id,
      data_job=data
    )

  @token_required
  def delete(self, user_id, job_id):
    return self.job_service.delete_job(
      user_id=user_id, 
      job_id=job_id
    )


class JobApi(Resource):
  job_service = JobService()
  
  def get(self, id=None):
    if not id and not request.args:
      return self.job_service.get_all_jobs()
    if id and request.args:
      return jsonify({'msg': 'выберите один способ для поиска'})
    if id:
      return self.job_service.get_job_by_id(id)
    if request.args:
      return self.job_service.search_jobs(query_params=request.args)






