from marshmallow import ValidationError, Schema, fields


def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


class RecipeIngredientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(validate=must_not_be_blank)
    amount = fields.Int()
    unit = fields.Str()
    calories = fields.Method("count_calories", dump_only=True)

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


class IngredientUnitMultiplierSchema(Schema):
    id = fields.Int(dump_only=True)
    unit = fields.Str(validate=must_not_be_blank)
    multiplier = fields.Float(validate=must_not_be_blank)


class IngredientInfoSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(validate=must_not_be_blank)
    calories_per_gram = fields.Int()
    unit_multipliers = fields.Nested(IngredientUnitMultiplierSchema, many=True)


recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True, only=("id", "name"))
recipe_detail_schema = RecipeDetailSchema()
recipe_ingredients_schema = RecipeIngredientSchema(many=True)
ingredient_info_schema = IngredientInfoSchema()
ingredient_infos_schema = IngredientInfoSchema(many=True)
