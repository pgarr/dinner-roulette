from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, FormField, \
    FieldList
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, URL, NumberRange, Optional, InputRequired, \
    Length

from app.models import User


class IngredientForm(FlaskForm):
    title = StringField('Ingredient name', validators=[Optional()])
    amount = IntegerField('Ingredient amount', validators=[Optional(), NumberRange(1, 999)])
    unit = StringField('Ingredient unit', validators=[Optional()])  # TODO: selector będzie lepszy


class RecipeDetailForm(FlaskForm):
    link = StringField('Website', validators=[Optional(), URL()])
    preparation = TextAreaField('Preparation', validators=[Optional()])


class RecipeForm(FlaskForm):
    title = StringField('Recipe title', validators=[Length(min=3)])
    time = IntegerField('Preparation time', validators=[Optional(), NumberRange(1, 999)])
    difficulty = IntegerField('Preparation difficulty (1-5)',
                              validators=[Optional(), NumberRange(1, 5)])  # TODO: Powiązać z ładnym selectorem
    # difficulty = SelectField('Preparation difficulty', choices=[(c, c) for c in [1, 2, 3, 4, 5]])
    detail = FormField(RecipeDetailForm)
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)
    add_ingredient = SubmitField('+')
    remove_ingredient = SubmitField('-')
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
