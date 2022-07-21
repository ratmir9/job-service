from src import db
from src.models.jobs import Job

class BaseService:
	def __init__(self):
		self.session = db.session

	def get_obj_by_id(self, db_table_name, id):
		obj = (
			self.session
			.query(db_table_name)
			.filter_by(id=id)
			.first()
		)

		if not obj:
			return ""
		return obj

	def get_all_obj(self, db_table_name):
		objects = self.session.query(db_table_name).all()
		return objects

	def create(self, obj):
		self.session.add(obj)
		self.session.commit()
		return obj
	
	def update(self, id, table_name, obj_data):
		obj = (
			self.session
			.query(table_name)
			.filter_by(id=id)
			.update(dict(**obj_data))
		)
		self.session.commit()
		return obj

	def delete_obj(self, obj):
		self.session.delete(obj)
		self.session.commit()
		return obj
		
	def check_user_in_owner(self, instance, user_id):
		# if not instance.owner_id == user_id:
		# 	return False
		# return True
		return bool(instance.owner_id == user_id)