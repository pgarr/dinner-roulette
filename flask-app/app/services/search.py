from app.models.recipes import Recipe


def search_recipe(string, page, per_page):
    page = int(page)
    per_page = int(per_page)
    return Recipe.search(string, page, per_page)


def reindex_es():
    Recipe.reindex()
