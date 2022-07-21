from marshmallow import Schema, fields

from src.schemas.resumes import ResumeSchema


class ResponseSchema(Schema):
	resume_id = fields.Integer(load_only=True, required=True)
	resumes = fields.Nested(ResumeSchema(), many=True, dump_only=True)
