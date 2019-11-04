import re

from app import db, BackupScheduler
from app.models import User, RecipeIngredient, Recipe, WaitingRecipe, WaitingRecipeIngredient
from tests.base_test import TestAppSetUp


class TestBackup(TestAppSetUp):
    def setUp(self):
        super().setUp()

        # users test test2 admin
        self.user = User(username="test", email="test@test.com")
        self.user.set_password("test")
        db.session.add(self.user)
        self.user2 = User(username="test2", email="test2@test.com")
        self.user2.set_password("test")
        db.session.add(self.user2)
        self.admin = User(username="admin", email="admin@test.com")
        self.admin.set_password("admin")
        db.session.add(self.admin)

        db.session.commit()

        self.user_pattern = '{\"user\": \[{\"id\": 1, \"username\": \"test\", \"email\": \"test@test\.com\", \"password_hash\":' \
                            ' \"pbkdf2:sha256:150000\$.*\"}, {\"id\": 2, \"username\": \"test2\", \"email\": \"test2@test\.com\",' \
                            ' \"password_hash\": \"pbkdf2:sha256:150000\$.*\"}, {\"id\": 3, \"username\": \"admin\", \"email\":' \
                            ' \"admin@test\.com\", \"password_hash\": \"pbkdf2:sha256:150000\$.*\"}\],'

        self.bh = BackupScheduler(db)

    def test_backup_users_created_and_other_tables_are_empty(self):
        result = self.bh.dump_backup()
        pattern = self.user_pattern + ' \"recipe\": \[\],' \
                                      ' \"recipe_ingredient\": \[\],' \
                                      ' \"waiting_recipe\": \[\],' \
                                      ' \"waiting_recipe_ingredient\": \[\]}'
        match = re.fullmatch(pattern, result)
        self.assertTrue(match)

    def test_backup_users_created_and_populated_all_tables(self):
        recipe_model = Recipe(title='test', time=1, difficulty=1, link='http://test.com', preparation='test',
                              author=self.user, ingredients=[RecipeIngredient(title='test1', amount=1, unit='kg'),
                                                             RecipeIngredient(title='test2', amount=1, unit='kg')])
        recipe_model_2 = Recipe(title='test2', time=2, difficulty=2, link='http://test2.com', preparation='test',
                                author=self.user2, ingredients=[RecipeIngredient(title='test1', amount=2, unit='kg'),
                                                                RecipeIngredient(title='test2', amount=2, unit='dag')])
        waiting_model = WaitingRecipe(title='test', time=3, difficulty=3, link='http://test3.com', preparation='test3',
                                      author=self.user2,
                                      ingredients=[WaitingRecipeIngredient(title='test1', amount=3, unit='g'),
                                                   WaitingRecipeIngredient(title='test2', amount=3, unit='g')])

        db.session.add(recipe_model)
        db.session.add(recipe_model_2)
        db.session.add(waiting_model)
        db.session.commit()

        result = self.bh.dump_backup()
        pattern = self.user_pattern + ' \"recipe\": \[{\"id\": 1, \"title\": \"test\", \"time\": 1, \"difficulty\": 1, ' \
                                      '\"link\": \"http://test\.com\", \"preparation\": \"test\", \"author_id\": 1}, ' \
                                      '{\"id\": 2, \"title\": \"test2\", \"time\": 2, \"difficulty\": 2, \"link\": ' \
                                      '\"http://test2\.com\", \"preparation\": \"test\", \"author_id\": 2}], ' \
                                      '\"recipe_ingredient\": \[{\"id\": 1, \"title\": \"test1\", \"amount\": 1\.0, ' \
                                      '\"unit\": \"kg\", \"recipe_id\": 1}, {\"id\": 2, \"title\": \"test2\", ' \
                                      '\"amount\": 1\.0, \"unit\": \"kg\", \"recipe_id\": 1}, {\"id\": 3, \"title\": ' \
                                      '\"test1\", \"amount\": 2\.0, \"unit\": \"kg\", \"recipe_id\": 2}, {\"id\": 4, ' \
                                      '\"title\": \"test2\", \"amount\": 2\.0, \"unit\": \"dag\", \"recipe_id\": 2}\], ' \
                                      '\"waiting_recipe\": \[{\"id\": 1, \"title\": \"test\", \"time\": 3, ' \
                                      '\"difficulty\": 3, \"link\": \"http://test3\.com\", \"preparation\": \"test3\", ' \
                                      '\"recipe_id\": null, \"author_id\": 2}\], \"waiting_recipe_ingredient\": ' \
                                      '\[{\"id\": 1, \"title\": \"test1\", \"amount\": 3\.0, \"unit\": \"g\", ' \
                                      '\"recipe_id\": 1}, {\"id\": 2, \"title\": \"test2\", \"amount\": 3\.0, ' \
                                      '\"unit\": \"g\", \"recipe_id\": 1}\]}'
        match = re.fullmatch(pattern, result)
        self.assertTrue(match)
