from marshmallow import Schema, fields
from schemas import ItemSchema, PlainStoreSchema, PlainTagSchema


class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)

class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)