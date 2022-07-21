from marshmallow import Schema, fields, validate


class JobSchema(Schema):
	id = fields.Integer(dump_only=True)
	title = fields.String(required=True, validate=[
		validate.Length(max=255)
	])
	description = fields.String(required=True)
	salary_to = fields.Integer(required=True)
	salary_from = fields.Integer(required=True)
	is_active = fields.Boolean(default=True, required=True)
	owner_id = fields.Integer(required=True, dump_only=True)
	created_at = fields.DateTime(dump_only=True)