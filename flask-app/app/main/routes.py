from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import db
from app.main import bp
from app.main.forms import LoginForm, RegistrationForm, RecipeForm
from app.models import User, Recipe, RecipeDetail


@bp.route('/')
@bp.route('/index')
def index():
    recipes = Recipe.query.all()
    return render_template('index.html', title='Home Page', recipes=recipes)


@bp.route('/recipe/<int:pk>', methods=['GET'])
def recipe(pk):
    rcp = Recipe.query.get(pk)
    if not rcp:
        return redirect(url_for('.index'))  # TODO: powinien być jakiś błąd
    return render_template('recipe.html', title=rcp.name, recipe=rcp)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe_detail_model = RecipeDetail(
            link=form.link.data,
            description=form.preparation.data
        )
        recipe_model = Recipe(
            name=form.recipe_name.data,
            time=form.time.data,
            difficulty=form.difficulty.data,
            detail=recipe_detail_model,
            author=current_user,
            ingredients=[]
        )
        # TODO: dodaj ingredientsy
        # TODO: dopisać użytkownika który to utworzył
        db.session.add(recipe_model)
        db.session.commit()
        flash('Recipe added!')
        return redirect(url_for('.recipe', pk=recipe_model.id))
    return render_template('new-recipe.html', title='New Recipe', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
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
