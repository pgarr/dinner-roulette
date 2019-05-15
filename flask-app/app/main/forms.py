from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, FormField, \
    FieldList, FloatField
from wtforms.validators import URL, NumberRange, Optional, Length


class IngredientForm(FlaskForm):
    title = StringField('Ingredient name', validators=[Optional(), Length(max=100)])
    amount = FloatField('Ingredient amount', validators=[Optional(), NumberRange(1, 999)])
    unit = StringField('Ingredient unit', validators=[Optional(), Length(max=20)])  # TODO: w formularzu dać podpowiedzi z istniejących


class RecipeDetailForm(FlaskForm):
    link = StringField('Website', validators=[Optional(), URL()])
    preparation = TextAreaField('Preparation', validators=[Optional(), Length(max=10000)])


class RecipeForm(FlaskForm):
    title = StringField('Recipe title', validators=[Length(min=3, max=200)])
    time = IntegerField('Preparation time', validators=[Optional(), NumberRange(1, 999)])
    difficulty = IntegerField('Preparation difficulty (1-5)',
                              validators=[Optional(), NumberRange(1, 5)])  # TODO: Powiązać z ładnym selectorem
    # difficulty = SelectField('Preparation difficulty', choices=[(c, c) for c in [1, 2, 3, 4, 5]])
    detail = FormField(RecipeDetailForm)
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)
    add_ingredient = SubmitField('+')
    remove_ingredient = SubmitField('-')
    submit = SubmitField('Add')



