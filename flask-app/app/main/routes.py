from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import db
from app.main import bp
from app.main.forms import LoginForm, RegistrationForm, RecipeForm
from app.main.services import init_recipe, save_recipe_from_form, get_recipe
from app.models import User, Recipe


@bp.route('/')
@bp.route('/index')
def index():
    recipes = Recipe.query.all()
    return render_template('index.html', title='Home Page', recipes=recipes)


@bp.route('/recipe/<int:pk>', methods=['GET'])
def get(pk):
    recipe = get_recipe(pk)
    if not recipe:
        flash('Recipe does not exist!')
        return redirect(url_for('.index'))  # TODO: powinien być jakiś błąd
    return render_template('recipe.html', title=recipe.title, recipe=recipe)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    recipe_model = init_recipe()
    form = RecipeForm(obj=recipe_model)
    if form.add_ingredient.data:
        form.ingredients.append_entry()
    elif form.remove_ingredient.data:
        form.ingredients.pop_entry()
    elif form.submit.data and form.validate_on_submit():
        save_recipe_from_form(form, recipe_model)
        flash('Recipe added!')
        return redirect(url_for('.get', pk=recipe_model.id))
    return render_template('new-recipe.html', title='New Recipe', form=form)


@bp.route('/edit/<int:pk>', methods=['GET', 'POST'])
@login_required  # TODO: tylko autor
def edit(pk):
    recipe_model = get_recipe(pk)
    if not recipe_model:
        flash('Recipe does not exist!')
        return redirect(url_for('.index'))  # TODO: powinien być jakiś błąd
    if current_user == recipe_model.author:
        form = RecipeForm(obj=recipe_model)
        if form.add_ingredient.data:
            form.ingredients.append_entry()
        elif form.remove_ingredient.data:
            form.ingredients.pop_entry()
        elif form.submit.data and form.validate_on_submit():
            save_recipe_from_form(form, recipe_model)
            flash('Recipe updated!')
            return redirect(url_for('.get', pk=recipe_model.id))
        return render_template('new-recipe.html', title='Edit Recipe', form=form)
    else:
        flash('You are not allowed to do this!')
        return redirect(url_for('.index'))  # TODO: powinien być jakiś błąd


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Recipe does not exist!')
        return redirect(url_for('.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('.next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('.login'))
    return render_template('register.html', title='Register', form=form)
