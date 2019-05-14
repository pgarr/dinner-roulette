from marshmallow import ValidationError, Schema, fields


class RecipeIngredientSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    amount = fields.Int()
    unit = fields.Str()


class RecipeDetailSchema(Schema):
    id = fields.Int(dump_only=True)
    link = fields.Str()
    preparation = fields.Str()


class RecipeSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    time = fields.Int()
    difficulty = fields.Int()
    detail = fields.Nested(RecipeDetailSchema, required=True)
    ingredients = fields.Nested(RecipeIngredientSchema, many=True, required=True)


recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True, only=("id", "title"))
recipe_detail_schema = RecipeDetailSchema()
recipe_ingredients_schema = RecipeIngredientSchema(many=True)
