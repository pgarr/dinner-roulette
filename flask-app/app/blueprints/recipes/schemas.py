from marshmallow import Schema, fields, pre_load, post_dump


class RecipeIngredientSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    amount = fields.Float(allow_none=True)
    unit = fields.Str()

    @pre_load
    def replace_empty_strings_with_nones(self, data, **kwargs):
        keys = ['amount']
        for key in keys:
            if key in data.keys():
                data[key] = data[key] or None
        return data

    @post_dump
    def replace_nones_with_empty_strings(self, data, **kwargs):
        keys = ['unit', 'amount']
        for key in keys:
            if key in data.keys():
                data[key] = data[key] or ''


class RecipeSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    time = fields.Int()
    difficulty = fields.Int()
    link = fields.Str()
    preparation = fields.Str()
    ingredients = fields.Nested(RecipeIngredientSchema, many=True, required=True)
    author = fields.Nested("self", only="username", dump_only=True)

    @post_dump
    def replace_nones_with_empty_strings(self, data, **kwargs):
        keys = ['preparation', 'link']
        for key in keys:
            if key in data.keys():
                data[key] = data[key] or ''


class WaitingRecipeSchema(RecipeSchema):
    refused = fields.Boolean(dump_only=True)
    recipe_id = fields.Int(dump_only=True)  # TODO: test that update cannot change this value


recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True, only=("id", "title", "time", "difficulty"))
waiting_schema = WaitingRecipeSchema()
waitings_schema = WaitingRecipeSchema(many=True, only=("id", "title", "time", "difficulty", "refused"))
recipe_ingredients_schema = RecipeIngredientSchema(many=True)
