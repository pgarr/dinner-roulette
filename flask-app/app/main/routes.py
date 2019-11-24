from flask import abort, render_template, flash, redirect, url_for, g, request, current_app
from flask_babel import _
from flask_login import current_user, login_required

from app.main import bp
from app.main.forms import RecipeForm, SearchForm
from app.services import init_waiting_recipe, get_recipe, save_recipe, get_recipes, get_waiting_recipe, \
    clone_recipe_to_waiting, get_waiting_recipes, accept_waiting, get_user_recipes, search_recipe, reindex_es


@bp.route('/')
@bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    recipes = get_recipes(page=page, per_page=current_app.config['RECIPES_PER_PAGE'])
    next_url = url_for('.index', page=recipes.next_num) if recipes.has_next else None
    prev_url = url_for('.index', page=recipes.prev_num) if recipes.has_prev else None
    return render_template('index.html', title=_('Home Page'), recipes=recipes.items, next_url=next_url,
                           prev_url=prev_url)


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


@bp.route('/recipes/my', methods=['GET'])
@login_required
def get_my_recipes():
    page = request.args.get('page', 1, type=int)
    recipes = get_user_recipes(author=current_user, page=page, per_page=current_app.config['RECIPES_PER_PAGE'])
    next_url = url_for('.get_my_recipes', page=recipes.next_num) if recipes.has_next else None
    prev_url = url_for('.get_my_recipes', page=recipes.prev_num) if recipes.has_prev else None
    return render_template('index.html', title=_('My Recipes'), recipes=recipes.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/waiting', methods=['GET'])
@login_required
def get_waiting_list():
    page = request.args.get('page', 1, type=int)
    waiting_recipes = get_waiting_recipes(user=current_user, page=page, per_page=current_app.config['RECIPES_PER_PAGE'])
    next_url = url_for('.get_waiting_list', page=waiting_recipes.next_num) if waiting_recipes.has_next else None
    prev_url = url_for('.get_waiting_list', page=waiting_recipes.prev_num) if waiting_recipes.has_prev else None
    return render_template('index.html', title=_('Waiting Recipes'), recipes=waiting_recipes.items, next_url=next_url,
                           prev_url=prev_url, waiting=True)


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


@bp.route('/search')
def search():
    if not g.search_form.validate():
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    recipes, total = search_recipe(g.search_form.q.data, page, current_app.config['RECIPES_PER_PAGE'])
    next_url = url_for('.search', q=g.search_form.q.data, page=page + 1) if total > page * current_app.config[
        'RECIPES_PER_PAGE'] else None
    prev_url = url_for('.search', q=g.search_form.q.data, page=page - 1) if page > 1 else None
    return render_template('index.html', title=_('Search'), recipes=recipes, next_url=next_url, prev_url=prev_url)
    # recipes, total = search_recipe(g.search_form.q.data, 1, 100)
    # return render_template('index.html', title=_('Search'), recipes=recipes)


@bp.route('/admin/reindex')
@login_required
def reindex():
    """Temporary endpoint to reindex recipes in elasticsearch"""
    # TODO: remove or develop
    if current_user.admin:
        reindex_es()
        return 'Done'
    else:
        abort(401)


# helper functions
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


@bp.before_app_request
def before_request():
    g.search_form = SearchForm()
