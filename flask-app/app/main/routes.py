from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import db
from app.main import bp
from app.main.forms import LoginForm, RegistrationForm, RecipeForm
from app.models import User, Recipe


@bp.route('/')
@bp.route('/index')
def index():
    recipes = Recipe.query.all()
    return render_template('index.html', title='Home Page', recipes=recipes)


@bp.route('/recipe/<int:pk>', methods=['GET'])
def recipe(pk):
    rcp = Recipe.query.get(pk)
    if not rcp:
        return redirect(url_for('main.index'))  # TODO: powinien być jakiś błąd
    return render_template('recipe.html', title=rcp.name, recipe=rcp)


@bp.route('/new', methods=['GET', 'POST'])
def new():
    form = RecipeForm()
    if form.validate_on_submit():
        # TODO: dodaj przepis
        flash('Recipe added!')
        return redirect(url_for('main.index'))  # TODO: powinno wyświetlać ten przepis
    return render_template('new-recipe.html', title='New Recipe', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('main.next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

# @login_required
