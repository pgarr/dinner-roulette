from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required, current_user

from app.api import bp
from app.api.errors import error_response, bad_request
from app.api.helpers import save_recipe_from_schema, paginated_recipes_jsonify, SearchAPIPaginatedAdapter
from app.api.schemas import recipe_schema, waiting_schema
from app.services import get_recipe, init_waiting_recipe, get_recipes, get_waiting_recipe, \
    get_waiting_recipes, accept_waiting, clone_recipe_to_waiting, get_user_recipes, search_recipe, reject_waiting


@bp.route('/', methods=['GET'])
def connection():
    return jsonify({'message': 'API is online!'}), 200


@bp.route('/recipes', methods=['GET'])
def recipes():
    page = request.args.get('page', 1)  # FIXME: jeśli jest string (np. "undefined") zwraca 500
    per_page = request.args.get('per_page', current_app.config['RECIPES_PER_PAGE'])
    recipe_models = get_recipes(page=page, per_page=per_page)
    return paginated_recipes_jsonify(recipe_models, page, per_page, endpoint='.recipes', items_name='recipes')


@bp.route('/recipes/my', methods=['GET'])
@jwt_required
def my_recipes():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', current_app.config['RECIPES_PER_PAGE'])
    my_models = get_user_recipes(author=current_user, page=page, per_page=per_page)
    return paginated_recipes_jsonify(my_models, page, per_page, endpoint='.my_recipes', items_name='recipes')


@bp.route('/recipe/<int:pk>', methods=['GET'])
def recipe(pk):
    recipe_model = get_recipe(pk)
    result = recipe_schema.dump(recipe_model)
    return jsonify({'recipe': result.data})


@bp.route('/waiting/<int:pk>', methods=['GET'])
@jwt_required
def waiting_recipe(pk):
    waiting_model = get_waiting_recipe(pk)
    if current_user == waiting_model.author or current_user.admin:
        result = waiting_schema.dump(waiting_model)
        return jsonify({'pending_recipe': result.data})
    else:
        return error_response(403)


@bp.route('/waiting', methods=['GET'])
@jwt_required
def waiting_recipes():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', current_app.config['RECIPES_PER_PAGE'])
    waitings_models = get_waiting_recipes(user=current_user, page=page,
                                          per_page=per_page)
    return paginated_recipes_jsonify(waitings_models, page, per_page, endpoint='.waiting_recipes',
                                     items_name='pending_recipes', waiting=True)


@bp.route('/waiting/<int:pk>/accept', methods=['GET'])
@jwt_required
def accept(pk):
    if current_user.admin:
        waiting_model = get_waiting_recipe(pk)
        recipe_model = accept_waiting(waiting_model)
        result = recipe_schema.dump(recipe_model)
        return jsonify({"message": "Recipe accepted!",
                        "recipe": result.data}), 200
    else:
        return error_response(401)


@bp.route('/waiting/<int:pk>/reject', methods=['GET'])
@jwt_required
def reject(pk):
    if current_user.admin:
        waiting_model = get_waiting_recipe(pk)
        reject_waiting(waiting_model)
        result = waiting_schema.dump(waiting_model)
        return jsonify({"message": "Recipe rejected!",
                        "rejected_recipe": result.data}), 200
    else:
        return error_response(401)


@bp.route('/recipe', methods=['POST'])
@jwt_required
def create_recipe():
    json_data = request.get_json()
    if not json_data:
        return bad_request('No input data provided')
    data, errors = waiting_schema.load(json_data)
    if errors:
        return jsonify(errors), 422
    waiting_model = init_waiting_recipe(author=current_user)
    save_recipe_from_schema(data, waiting_model)
    waiting_model = get_waiting_recipe(waiting_model.id)
    result = waiting_schema.dump(waiting_model)
    return jsonify({"message": "Recipe will be seen for other users after administrator acceptance.",
                    "pending_recipe": result.data}), 201


@bp.route('/recipe/<int:pk>', methods=['PATCH'])
@jwt_required
def update_recipe(pk):
    json_data = request.get_json()
    if not json_data:
        return bad_request('No input data provided')
    recipe_model = get_recipe(pk)
    if current_user == recipe_model.author or current_user.admin:
        if recipe_model.waiting_updates:
            result = waiting_schema.dump(recipe_model.waiting_updates)
            return jsonify({"message": "Recipe already has changes waiting for acceptance!",
                            "pending_recipe": result.data}), 400
        else:
            data, errors = waiting_schema.load(json_data)
            if errors:
                return jsonify(errors), 422
            waiting_model = clone_recipe_to_waiting(recipe_model)
            save_recipe_from_schema(data, waiting_model)
            waiting_model = get_waiting_recipe(waiting_model.id)
            result = waiting_schema.dump(waiting_model)
            return jsonify({"message": "Changes will be seen for other users after administrator acceptance.",
                            "pending_recipe": result.data}), 200
    else:
        return error_response(401)


@bp.route('/waiting/<int:pk>', methods=['PATCH'])
@jwt_required
def update_waiting_recipe(pk):
    json_data = request.get_json()
    if not json_data:
        return bad_request('No input data provided')
    waiting_model = get_waiting_recipe(pk)
    if current_user == waiting_model.author or current_user.admin:
        data, errors = waiting_schema.load(json_data)
        if errors:
            return jsonify(errors), 422
        save_recipe_from_schema(data, waiting_model)
        waiting_model = get_waiting_recipe(waiting_model.id)
        result = waiting_schema.dump(waiting_model)
        return jsonify({"message": "Pending changes saved.",
                        "pending_recipe": result.data}), 200
    else:
        return error_response(401)


@bp.route('/search', methods=['GET'])
def search():
    q = request.args.get('q', '')
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', current_app.config['RECIPES_PER_PAGE'])
    recipe_models, total = search_recipe(q, page, per_page)
    paginated = SearchAPIPaginatedAdapter(recipe_models, page, per_page, total)
    return paginated_recipes_jsonify(paginated, page, per_page, endpoint='.search', items_name='recipes', q=q)
