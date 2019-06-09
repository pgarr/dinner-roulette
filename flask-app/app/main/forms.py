from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, FormField, \
    FieldList, FloatField
from wtforms.validators import URL, NumberRange, Optional, Length


class IngredientForm(FlaskForm):
    title = StringField(_l('Ingredient name'), validators=[Optional(), Length(max=100)])
    amount = FloatField(_l('Ingredient amount'), validators=[Optional(), NumberRange(0, 999)])
    unit = StringField(_l('Ingredient unit'),
                       validators=[Optional(), Length(max=20)])  # TODO: w formularzu dać podpowiedzi z istniejących


class RecipeForm(FlaskForm):
    title = StringField(_l('Recipe title'), validators=[Length(min=3, max=200)])
    time = IntegerField(_l('Preparation time (minutes)'), validators=[Optional(), NumberRange(1, 999)])
    difficulty = IntegerField(_l('Preparation difficulty (1-5)'),
                              validators=[Optional(), NumberRange(1, 5)])  # TODO: Powiązać z ładnym selectorem
    # difficulty = SelectField('Preparation difficulty', choices=[(c, c) for c in [1, 2, 3, 4, 5]])
    link = StringField(_l('Website'), validators=[Optional(), URL()])
    preparation = TextAreaField(_l('Preparation'), validators=[Optional(), Length(max=10000)])
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)
    add_ingredient = SubmitField('+')
    remove_ingredient = SubmitField('-')
    submit = SubmitField(_l('Submit'))
