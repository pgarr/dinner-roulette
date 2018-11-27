from marshmallow import Schema, fields, ValidationError


def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


class RecipeIngredientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(validate=must_not_be_blank)
    amount = fields.Int()
    unit = fields.Str()


class RecipeDetailSchema(Schema):
    id = fields.Int(dump_only=True)
    link = fields.Str()
    description = fields.Str(validate=must_not_be_blank)


class RecipeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(validate=must_not_be_blank)
    detail = fields.Nested(RecipeDetailSchema, validate=must_not_be_blank)
    ingredients = fields.Nested(RecipeIngredientSchema, many=True, validate=must_not_be_blank)


class RecipeUpdateSchema(Schema):
    name = fields.Str(validate=must_not_be_blank)
    detail = fields.Nested(RecipeDetailSchema, validate=must_not_be_blank)
    update = fields.Nested(RecipeIngredientSchema, many=True)
    add = fields.Nested(RecipeIngredientSchema, many=True)
    delete = fields.List(fields.String)


recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True, only=("id", "name"))
recipe_detail_schema = RecipeDetailSchema()
recipe_ingredients_schema = RecipeIngredientSchema(many=True)
recipe_update_schema = RecipeUpdateSchema()
