from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField, \
    FormField, FieldList
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, URL, NumberRange, Optional

from app.models import User


class IngredientForm(FlaskForm):
    ingredient_name = StringField('Ingredient name', validators=[DataRequired()])
    amount = IntegerField('Ingredient amount', validators=[Optional(), NumberRange(1, 999)])
    unit = StringField('Ingredient unit', validators=[Optional()])  # TODO: selector będzie lepszy


class RecipeForm(FlaskForm):
    recipe_name = StringField('Recipe title', validators=[DataRequired()])
    time = IntegerField('Preparation time', validators=[Optional(), NumberRange(1, 999)])
    # TODO: Powiązać z ładnym selectorem
    difficulty = IntegerField('Preparation difficulty (1-5)',
                              validators=[Optional(), NumberRange(1, 5)])
    # difficulty = SelectField('Preparation difficulty', choices=[(c, c) for c in [1, 2, 3, 4, 5]])
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)
    preparation = TextAreaField('Preparation')
    link = StringField('Website', validators=[Optional(), URL()])
    # TODO: dynamicznie dodawane ingredientsy
    submit = SubmitField('Add')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('User with this name already exist.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This e-mail address is already registered.')
