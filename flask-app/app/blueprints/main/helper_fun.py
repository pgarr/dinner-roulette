from app.services.recipes import save_recipe


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
