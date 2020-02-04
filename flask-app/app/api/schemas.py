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


class WaitingRecipeSchema(RecipeSchema):
    refused = fields.Boolean(dump_only=True)


recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True, only=("id", "title", "time", "difficulty"))
waiting_schema = WaitingRecipeSchema()
waitings_schema = WaitingRecipeSchema(many=True, only=("id", "title", "time", "difficulty", "refused"))
recipe_ingredients_schema = RecipeIngredientSchema(many=True)
