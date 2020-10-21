"""
Module used to run app with TestConfig as configuration. Every run destroys and recreates sql tables.
It can create data based on json got as argument passed in cmd. Without it, creates 3 sample users: 'test', 'test2' and 'admin'.
Json working example:
data = {"users": [{"username": "test", "email": "test@test.com", "password": "test"},
                  {"username": "test2", "email": "test2@test.com", "password": "test"},
                  {"username": "admin", "email": "admin@test.com", "password": "admin"}],
        "recipes": [
            {"title": "test", "time": 30, "difficulty": 3, "link": "http://test.pl", "preparation": "test test", "author": "test2", "ingredients": [
                 {"title": "test1", "amount": 3, "unit": "kg"},
                 {"title": "test2"}]
             }],
        "waiting_recipes": [
            {"title": "test", "time": 30, "difficulty": 3, "link": "http://test.pl", "preparation": "test test", "author": "test2",
            {"title": "test2", "link": "http://test.pl", "preparation": "test test", "author": "test", "ingredients": [
                 {"title": "test1", "amount": 3, "unit": "kg"},
                 {"title": "test2"}]
             }]
        }
"""

import argparse
import json
import os

from app import create_app, db
from app.models.auth import User
from app.models.recipes import Recipe, WaitingRecipe
from app.services.auth import get_user_by_name
from app.services.recipes import get_recipe_by_title
from tests.utils import TestConfig


def set_up_data(data_dict):
    # set up users
    for user_data in data_dict.get('users', ()):
        user = User(username=user_data.get('username'), email=user_data.get('email'))
        user.set_password(user_data.get('password'))
        db.session.add(user)

    # set up recipes
    for recipe_data in data_dict.get('recipes', ()):
        author = recipe_data.pop('author', None)
        ingredients_data = recipe_data.pop('ingredients', ())
        recipe = Recipe(**recipe_data)
        recipe.author = get_user_by_name(author)

        for ingredient_data in ingredients_data:
            recipe.add_ingredient(**ingredient_data)

        db.session.add(recipe)

    # set up waiting recipes
    for waiting_recipe_data in data_dict.get('waiting_recipes', ()):
        author = waiting_recipe_data.pop('author', None)
        updated_recipe = waiting_recipe_data.pop('updated_recipe', None)
        ingredients_data = waiting_recipe_data.pop('ingredients', ())

        waiting_recipe = WaitingRecipe(**waiting_recipe_data)
        waiting_recipe.author = get_user_by_name(author)
        waiting_recipe.updated_recipe = get_recipe_by_title(updated_recipe)

        for ingredient_data in ingredients_data:
            waiting_recipe.add_ingredient(**ingredient_data)

        db.session.add(waiting_recipe)

    # commit data
    db.session.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='json load and set up data')
    parser.add_argument('-i', '--inputstring', help='Input string in json format', required=False)
    args = parser.parse_args()
    inp = args.inputstring

    if inp:
        data = json.loads(inp)
    else:
        data = {"users": [{"username": "test", "email": "test@test.com", "password": "test"},
                          {"username": "test2", "email": "test2@test.com", "password": "test"},
                          {"username": "admin", "email": "admin@test.com", "password": "admin"}]}

    app = create_app(TestConfig)
    db.session.remove()
    db.drop_all()
    db.create_all()

    set_up_data(data)

    app.run(port=os.environ.get('AUT_PORT'), debug=False)
