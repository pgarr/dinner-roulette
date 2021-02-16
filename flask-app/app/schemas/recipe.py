from marshmallow import Schema, fields, pre_load, post_dump, EXCLUDE


class RecipeIngredientSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    amount = fields.Float(allow_none=True)
    unit = fields.Str()

    class Meta:
        unknown = EXCLUDE

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
        return data


class RecipeSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    time = fields.Int()
    difficulty = fields.Int()
    link = fields.Str()
    preparation = fields.Str()
    ingredients = fields.Nested(RecipeIngredientSchema, many=True, required=True)
    author = fields.Function(serialize=lambda obj: obj.author.username, dump_only=True)
    status = fields.Function(serialize=lambda obj: obj.status.name, dump_only=True)

    class Meta:
        unknown = EXCLUDE

    @post_dump
    def replace_nones_with_empty_strings(self, data, **kwargs):
        keys = ['preparation', 'link']
        for key in keys:
            if key in data.keys():
                data[key] = data[key] or ''
        return data


class FullRecipe(RecipeSchema):
    create_date = fields.DateTime()
    last_modified = fields.DateTime()


recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True, only=("id", "title", "time", "difficulty", "status"))
full_recipes_schema = FullRecipe(many=True)
recipe_ingredients_schema = RecipeIngredientSchema(many=True)
