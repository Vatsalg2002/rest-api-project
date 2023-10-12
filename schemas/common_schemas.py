from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True )
    name = fields.Str(required=True, 
                    error_messages={"": "name is required.",
                                    "invalid":"name must be strrequireding"})
    price = fields.Float(required=True,
                    error_messages={"invalid": "price shoudl be a float",
                                    "required":"price is required parameter"}
                    )


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, 
                    error_messages={"required": "name is required.",
                                    "invalid":"name must be string"},
                    )

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str() 