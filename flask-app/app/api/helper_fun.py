from flask import url_for, jsonify

from app.api.schemas import recipes_schema, waitings_schema
from app.services import save_recipe


def save_recipe_from_schema(data, model):
    model.title = data.get('title')
    model.time = data.get('time')
    model.difficulty = data.get('difficulty')
    model.link = data.get('link')
    model.preparation = data.get('preparation')
    model.ingredients = []
    for data_ingredient in data['ingredients']:
        model.add_ingredient(**data_ingredient)
    save_recipe(model)


def paginated_recipes_jsonify(paginated, page, per_page, endpoint, items_name, waiting=False, **kwargs):
    if waiting:
        result = waitings_schema.dump(paginated.items)
    else:
        result = recipes_schema.dump(paginated.items)
    page = int(page)
    per_page = int(per_page)
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
    return jsonify({items_name: result.data, '_meta': meta, '_links': links})


class SearchAPIPaginatedAdapter:
    """Adapter between search result and paginated_recipes_jsonify"""

    def __init__(self, items, page, per_page, total):
        self.items = items
        self.page = int(page)
        self.total = int(total)
        self.per_page = int(per_page)

    @property
    def pages(self):
        return -(-self.total // self.per_page)

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def has_prev(self):
        return self.page > 1
