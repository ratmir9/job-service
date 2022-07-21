from flask_restful import Resource

from src.services.users import UserService
from src.services.auth import token_required


class UserApi(Resource):
	user_service = UserService()

	def get(self, id):
		return self.user_service.get_user_by_id(id)

	@token_required
	def delete(self, user_id, id):
		return self.user_service.delete_user(user_id, id)
