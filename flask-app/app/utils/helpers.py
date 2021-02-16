from flask import current_app


# TODO: unit tests
def page_handler(page, per_page):
    try:
        page = int(page)
    except ValueError:
        page = 1

    try:
        per_page = int(per_page)
    except ValueError:
        per_page = current_app.config['RECIPES_PER_PAGE']

    return page, per_page
