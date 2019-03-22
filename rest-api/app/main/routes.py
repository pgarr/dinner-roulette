from flask import render_template, flash, redirect, url_for
from app.main import bp
from app.main.forms import LoginForm


@bp.route('/')
@bp.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Sign In', form=form)
