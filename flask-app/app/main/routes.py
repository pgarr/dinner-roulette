from flask import abort, render_template, flash, redirect, url_for
from flask_login import current_user, login_required

from app.main import bp
from app.main.forms import RecipeForm
from app.services import init_waiting_recipe, get_recipe, save_recipe, get_all_recipes, get_waiting_recipe, \
    clone_recipe_to_waiting


@bp.route('/')
@bp.route('/index')
def index():
    recipes_models = get_all_recipes()
    return render_template('index.html', title='Home Page', recipes=recipes_models)


@bp.route('/recipe/<int:pk>', methods=['GET'])
def get(pk):
    recipe_model = get_recipe(pk)
    return render_template('recipe.html', title=recipe_model.title, recipe=recipe_model)


@bp.route('/waiting/<int:pk>', methods=['GET'])
@login_required
def get_waiting(pk):
    recipe_model = get_waiting_recipe(pk)
    if current_user == recipe_model.author or current_user.admin:
        return render_template('recipe.html', title=recipe_model.title, recipe=recipe_model)
    else:
        abort(401)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    recipe_model = init_waiting_recipe(author=current_user)
    form = RecipeForm()
    if form.add_ingredient.data:
        form.ingredients.append_entry()
    elif form.remove_ingredient.data:
        form.ingredients.pop_entry()
    elif form.submit.data and form.validate_on_submit():
        save_recipe_from_form(form, recipe_model)
        flash('Recipe added!')
        flash('Recipe will be seen for other users after administrator acceptance.')
        return redirect(url_for('.get_waiting', pk=recipe_model.id))
    return render_template('new-recipe.html', title='New Recipe', form=form)


@bp.route('/edit/<int:pk>', methods=['GET', 'POST'])
@login_required
def edit(pk):
    edited_model = get_recipe(pk)
    if current_user == edited_model.author or current_user.admin:
        if edited_model.waiting_updates:
            flash('Recipe already has changes waiting for acceptance!')
            recipe_model = edited_model.waiting_updates
        else:
            recipe_model = clone_recipe_to_waiting(edited_model)
        form = RecipeForm(obj=recipe_model)
        if form.add_ingredient.data:  # TODO: edit powoduje dodanie 1 pustego wiersza. Zbadać
            form.ingredients.append_entry()
        elif form.remove_ingredient.data:
            form.ingredients.pop_entry()
        elif form.submit.data and form.validate_on_submit():
            save_recipe_from_form(form, recipe_model)
            flash('Recipe updated!')
            flash('Changes will be seen for other users after administrator acceptance.')
            return redirect(url_for('.get_waiting', pk=recipe_model.id))
        return render_template('new-recipe.html', title='Edit Recipe', form=form)
    else:
        abort(401)


def save_recipe_from_form(form, model):
    model.title = form.title.data
    model.time = form.time.data
    model.difficulty = form.difficulty.data
    model.link = form.link.data
    model.preparation = form.preparation.data
    model.ingredients = []
    for i in form.ingredients:
        if i.title.data:
            model.add_ingredient(title=i.title.data, amount=i.amount.data, unit=i.unit.data)
    save_recipe(model)
