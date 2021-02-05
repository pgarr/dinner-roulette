from flask import url_for, jsonify

from app.schemas.recipe import recipes_schema
from app.services.recipes import save_recipe
from app.utils.helpers import page_handler


def save_recipe_from_schema(data, model):
    model.title = data.get('title')
    model.time = data.get('time')
    model.difficulty = data.get('difficulty')
    model.link = data.get('link')
    model.preparation = data.get('preparation')
    model.ingredients = []
    for data_ingredient in data['ingredients']:
        model.add_ingredient(**data_ingredient)
    return save_recipe(model)


def paginated_recipes_jsonify(paginated, page, per_page, endpoint, **kwargs):
    result = recipes_schema.dump(paginated.items)
    page, per_page = page_handler(page, per_page)
    meta = {
        'page': page,
        'per_page': per_page,
        'total_pages': paginated.pages,
        'total_items': paginated.total
    }
    links = {
        'self': url_for(endpoint, page=page, per_page=per_page,
                        **kwargs),
        'next': url_for(endpoint, page=page + 1, per_page=per_page,
                        **kwargs) if paginated.has_next else None,
        'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                        **kwargs) if paginated.has_prev else None
    }
    return jsonify({'recipes': result, '_meta': meta, '_links': links})
