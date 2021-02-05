from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.String()
    email = fields.String()
    isAdmin = fields.Function(serialize=lambda obj: obj.admin, dump_only=True)


users_schema = UserSchema(many=True)
