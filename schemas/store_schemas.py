from marshmallow import Schema, fields
from schemas import PlainItemSchema, PlainStoreSchema, PlainTagSchema

# class PlainStoreSchema(Schema):
#     id = fields.Int(dump_only=True)
#     name = fields.Str()

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)