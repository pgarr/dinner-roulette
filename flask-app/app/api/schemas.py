from marshmallow import Schema, fields


class RecipeIngredientSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    amount = fields.Float()
    unit = fields.Str()


class RecipeSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    time = fields.Int()
    difficulty = fields.Int()
    link = fields.Str()
    preparation = fields.Str()
    ingredients = fields.Nested(RecipeIngredientSchema, many=True, required=True)


recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True, only=("id", "title"))
recipe_ingredients_schema = RecipeIngredientSchema(many=True)
