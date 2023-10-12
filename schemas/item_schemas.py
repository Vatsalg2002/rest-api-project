from marshmallow import Schema, fields
from schemas import PlainItemSchema, PlainStoreSchema, PlainTagSchema
# class PlainItemSchema(Schema):
#     id = fields.Int(dump_only=True)
#     name = fields.Str(required=True)
#     price = fields.Float(required=True)


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(
        required=True, 
        load_only=True,
        error_messages={"required": "Field 1 is required."}
    )
    
    store = fields.Nested(
        PlainStoreSchema(), 
        dump_only=True
    )
        
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()