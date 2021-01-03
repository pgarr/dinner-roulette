import pytest

from app import create_app, db
from app.models.auth import User
from app.models.recipes import Recipe, RecipeIngredient, WaitingRecipe, WaitingRecipeIngredient
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

    MAIL_SERVER = None
    MAIL_PORT = None
    MAIL_USERNAME = None
    MAIL_PASSWORD = None

    RECIPES_PER_PAGE = 4
    ELASTICSEARCH_URL = None


@pytest.fixture(scope='session')
def test_client():
    # set up
    flask_app = create_app(TestConfig)

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    # tear down
    ctx.pop()


@pytest.fixture
def database():
    # set up
    db.create_all()

    yield db

    # tear down
    db.session.remove()
    db.drop_all()


@pytest.fixture
def make_user(database):
    def _make_user(username, password, email):
        user = User(username=username, email=email)
        user.set_password(password)

        database.session.add(user)
        database.session.commit()

        return user

    return _make_user


@pytest.fixture
def make_recipe(database):
    def _make_recipe(ingredients=(), **kwargs):
        recipe_model = Recipe(**kwargs,
                              ingredients=[RecipeIngredient(title=ingredient['title'], amount=ingredient['amount'],
                                                            unit=ingredient['unit']) for ingredient in ingredients])

        database.session.add(recipe_model)
        database.session.commit()

        return recipe_model

    return _make_recipe


@pytest.fixture
def make_waiting_recipe(database):
    def _make_waiting_recipe(ingredients=(), **kwargs):
        waiting_recipe_model = WaitingRecipe(**kwargs, ingredients=[WaitingRecipeIngredient(title=ingredient['title'],
                                                                                            amount=ingredient['amount'],
                                                                                            unit=ingredient['unit']) for
                                                                    ingredient in ingredients])

        database.session.add(waiting_recipe_model)
        database.session.commit()

        return waiting_recipe_model

    return _make_waiting_recipe


@pytest.fixture
def users_set(make_user):
    user1 = make_user("test", "test", "test@test.com")
    user2 = make_user("test2", "test", "test2@test.com")
    admin = make_user("admin", "test", "admin@test.com")

    return user1, user2, admin
