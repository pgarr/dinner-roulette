from flask import abort, render_template, flash, redirect, url_for
from flask_login import current_user, login_required

from app.main import bp
from app.main.forms import RecipeForm
from app.models import RecipeIngredient
from app.services import init_recipe, get_recipe, save_recipe, get_all_recipes


@bp.route('/')
@bp.route('/index')
def index():
    recipes = get_all_recipes()
    return render_template('index.html', title='Home Page', recipes=recipes)


@bp.route('/recipe/<int:pk>', methods=['GET'])
def get(pk):
    recipe = get_recipe(pk)
    return render_template('recipe.html', title=recipe.title, recipe=recipe)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    recipe_model = init_recipe(author=current_user)
    form = RecipeForm()
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
@login_required
def edit(pk):
    recipe_model = get_recipe(pk)
    if current_user == recipe_model.author or current_user.admin:
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
            ingredient_model = RecipeIngredient(
                title=i.title.data,
                amount=i.amount.data,
                unit=i.unit.data
            )
            model.ingredients.append(ingredient_model)
    save_recipe(model)
