from marshmallow import Schema, fields

from schemas.validators import must_not_be_blank


class RecipeIngredientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(validate=must_not_be_blank)
    amount = fields.Int()
    unit = fields.Str()
    calories = fields.Method("count_calories", dump_only=True)  # TODO: preprocess this from IngredientInfo

    def count_calories(self, ingredient):
        if ingredient.info:
            for unit_multiplier in ingredient.info.unit_multipliers:
                if unit_multiplier.unit == ingredient.unit:
                    return unit_multiplier.multiplier * ingredient.info.calories_per_gram * ingredient.amount


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
