from marshmallow import fields, Schema

from schemas.validators import must_not_be_blank


class IngredientUnitMultiplierSchema(Schema):
    id = fields.Int(dump_only=True)
    unit = fields.Str(validate=must_not_be_blank)
    multiplier = fields.Float(validate=must_not_be_blank)


class IngredientInfoSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(validate=must_not_be_blank)
    calories_per_gram = fields.Int()
    unit_multipliers = fields.Nested(IngredientUnitMultiplierSchema, many=True)


ingredient_info_schema = IngredientInfoSchema()
ingredient_infos_schema = IngredientInfoSchema(many=True)
