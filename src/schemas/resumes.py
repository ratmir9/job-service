from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField

from src.models.resumes import GenderEnum


class ResumeSchema(Schema):
	id = fields.Integer(dump_only=True)
	last_name = fields.String(required=True, validate=[
		validate.Length(max=64)
	])
	first_name = fields.String(required=True, validate=[
		validate.Length(max=64)
	])
	about_me = fields.String(required=True)
	speciality = fields.String(required=True, validate=[
		validate.Length(max=255)
	])
	position = fields.String(required=True, validate=[
		validate.Length(max=255)
	])
	gender = EnumField(GenderEnum, required=True)
	birth_day = fields.Date(required=True)
	owner_id = fields.Integer(dump_only=True, required=True)
	created_at = fields.DateTime(dump_only=True)