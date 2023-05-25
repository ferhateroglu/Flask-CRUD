from marshmallow import Schema, fields

class MeetingSchema(Schema):
    id = fields.Int(dump_only=True)
    topic = fields.Str()
    date_ = fields.Str()
    start_time = fields.Str()
    end_time = fields.Str()
    participants = fields.Str()

meeting_schema = MeetingSchema()
meetings_schema = MeetingSchema(many=True)