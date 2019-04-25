from marshmallow import ValidationError, Schema, fields


def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


class RecipeIngredientSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(validate=must_not_be_blank)
    amount = fields.Int()
    unit = fields.Str()


class RecipeDetailSchema(Schema):
    id = fields.Int(dump_only=True)
    link = fields.Str()
    preparation = fields.Str()


class RecipeSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(validate=must_not_be_blank)
    time = fields.Int()
    difficulty = fields.Int()
    detail = fields.Nested(RecipeDetailSchema, validate=must_not_be_blank)
    ingredients = fields.Nested(RecipeIngredientSchema, many=True, validate=must_not_be_blank)


recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True, only=("id", "title"))
recipe_detail_schema = RecipeDetailSchema()
recipe_ingredients_schema = RecipeIngredientSchema(many=True)
