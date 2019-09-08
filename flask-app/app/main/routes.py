from flask import abort, render_template, flash, redirect, url_for
from flask_login import current_user, login_required

from app.main import bp
from app.main.forms import RecipeForm
from app.services import init_waiting_recipe, get_recipe, save_recipe, get_all_recipes, get_waiting_recipe, \
    clone_recipe_to_waiting, get_all_waiting_recipes, accept_waiting
from flask_babel import _


@bp.route('/')
@bp.route('/index')
def index():
    recipes_models = get_all_recipes()
    return render_template('index.html', title=_('Home Page'), recipes=recipes_models)


@bp.route('/recipe/<int:pk>', methods=['GET'])
def get(pk):
    recipe_model = get_recipe(pk)
    return render_template('recipe.html', title=_('Recipe'), recipe=recipe_model)


@bp.route('/waiting/<int:pk>', methods=['GET'])
@login_required
def get_waiting(pk):
    waiting_model = get_waiting_recipe(pk)
    if current_user == waiting_model.author or current_user.admin:
        flash(_('This recipe is pending approval by the administrator.'))
        return render_template('recipe.html', title=_('Waiting Recipe'), recipe=waiting_model, waiting=True)
    else:
        abort(401)


@bp.route('/waiting', methods=['GET'])
@login_required
def get_waiting_list():
    waitings_models = get_all_waiting_recipes(user=current_user)
    return render_template('index.html', title=_('Waiting Recipes'), recipes=waitings_models, waiting=True)


@bp.route('/waiting/<int:pk>/accept', methods=['GET'])
@login_required
def accept(pk):
    if current_user.admin:
        waiting_model = get_waiting_recipe(pk)
        recipe_model = accept_waiting(waiting_model)
        flash(_('Recipe accepted!'))
        return redirect(url_for('.get', pk=recipe_model.id))
    else:
        abort(401)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    waiting_model = init_waiting_recipe(author=current_user)
    form = RecipeForm()
    if form.add_ingredient.data:
        form.ingredients.append_entry()
    elif form.remove_ingredient.data:
        form.ingredients.pop_entry()
    elif form.submit.data and form.validate_on_submit():
        save_recipe_from_form(form, waiting_model)
        flash(_('Recipe added!'))
        flash(_('Recipe will be seen for other users after administrator acceptance.'))
        return redirect(url_for('.get_waiting', pk=waiting_model.id))
    return render_template('new-recipe.html', title=_('New Recipe'), form=form)


@bp.route('/edit/<int:pk>', methods=['GET', 'POST'])
@login_required
def edit(pk):
    recipe_model = get_recipe(pk)
    if current_user == recipe_model.author or current_user.admin:
        if recipe_model.waiting_updates:
            flash(_('Recipe already has changes waiting for acceptance!'))
            return redirect(url_for('.edit_waiting', pk=recipe_model.waiting_updates.id))
        else:
            waiting_model = clone_recipe_to_waiting(recipe_model)
        form = RecipeForm(obj=waiting_model)
        if form.add_ingredient.data:  # TODO: edit powoduje dodanie 1 pustego wiersza. Zbadać
            form.ingredients.append_entry()
        elif form.remove_ingredient.data:
            form.ingredients.pop_entry()
        elif form.submit.data and form.validate_on_submit():
            save_recipe_from_form(form, waiting_model)
            flash(_('Recipe updated!'))
            flash(_('Changes will be seen for other users after administrator acceptance.'))
            return redirect(url_for('.get_waiting', pk=waiting_model.id))
        return render_template('new-recipe.html', title=_('Edit Recipe'), form=form)
    else:
        abort(401)


@bp.route('/waiting/<int:pk>/edit', methods=['GET', 'POST'])
@login_required
def edit_waiting(pk):
    waiting_model = get_waiting_recipe(pk)
    if current_user == waiting_model.author or current_user.admin:
        form = RecipeForm(obj=waiting_model)
        if form.add_ingredient.data:
            form.ingredients.append_entry()
        elif form.remove_ingredient.data:
            form.ingredients.pop_entry()
        elif form.submit.data and form.validate_on_submit():
            save_recipe_from_form(form, waiting_model)
            flash(_('Pending changes saved!'))
            return redirect(url_for('.get_waiting', pk=waiting_model.id))
        return render_template('new-recipe.html', title=_('Edit Waiting Recipe'), form=form)
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
