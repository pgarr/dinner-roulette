from gui_tests.base_test import BaseTest
from gui_tests.helpers import wait_page_changes
from gui_tests.models.pages import HomePage, MyRecipesPage, WaitingRecipesPage


class MyRecipesTest(BaseTest):

    def setUp_recipes(self):
        recipes = [
            {"title": "test", "time": 30, "difficulty": 3, "link": "http://test.pl", "preparation": "test test",
             "author": "test2", "ingredients": [
                {"title": "test1", "amount": 3, "unit": "kg"},
                {"title": "test2"}]},
            {"title": "test2", "time": 30, "difficulty": 3, "link": "http://test2.pl", "preparation": "test2 test2",
             "author": "test2", "ingredients": [
                {"title": "test1", "amount": 3, "unit": "kg"},
                {"title": "test2"}]}
        ]
        return recipes

    def test_my_recipes_two_recipes(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)

        self.smart_login('test2', 'test')

        self.navbar.go_to_my_recipes_page()
        my_recipes_page = wait_page_changes(home_page, MyRecipesPage(self.driver))

        self.assertEqual(len(my_recipes_page.recipes), 2, msg="My recipes count is correct")

    def test_my_recipes_no_recipes(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)

        self.smart_login('test', 'test')

        self.navbar.go_to_my_recipes_page()
        my_recipes_page = wait_page_changes(home_page, MyRecipesPage(self.driver))

        self.assertEqual(len(my_recipes_page.recipes), 0,
                         msg="My recipes count is correct")


class RecipesVisibilityTest(BaseTest):
    def setUp_users(self):
        return [{"username": "test", "email": "test@test.com", "password": "test"},  # has 2 waiting recipes
                {"username": "test2", "email": "test2@test.com", "password": "test"},  # has 2 recipes
                {"username": "test3", "email": "test3@test.com", "password": "test"},  # has 1 waiting recipe, 1 recipe
                {"username": "admin", "email": "admin@test.com", "password": "admin"}]

    def setUp_recipes(self):
        recipes = [
            {"title": "test", "time": 30, "difficulty": 3, "link": "http://test.pl", "preparation": "test test",
             "author": "test2", "ingredients": [
                {"title": "test1", "amount": 3, "unit": "kg"},
                {"title": "test2"}]},
            {"title": "test2", "time": 30, "difficulty": 3, "link": "http://test2.pl", "preparation": "test2 test2",
             "author": "test2", "ingredients": [
                {"title": "test1", "amount": 3, "unit": "kg"},
                {"title": "test2"}]},
            {"title": "test3", "time": 30, "difficulty": 3, "link": "http://test.pl", "preparation": "test test",
             "author": "test3", "ingredients": [
                {"title": "test1", "amount": 3, "unit": "kg"},
                {"title": "test2"}]}
        ]
        return recipes

    def setUp_waiting_recipes(self):
        waiting_recipes = [
            {"title": "test", "time": 30, "difficulty": 3, "link": "http://test.pl", "preparation": "test test",
             "author": "test", "ingredients": [
                {"title": "test1", "amount": 3, "unit": "kg"},
                {"title": "test2"}]},
            {"title": "test2", "time": 30, "difficulty": 3, "link": "http://test2.pl", "preparation": "test2 test2",
             "author": "test", "ingredients": [
                {"title": "test1", "amount": 3, "unit": "kg"},
                {"title": "test2"}]},
            {"title": "test3", "time": 30, "difficulty": 3, "link": "http://test.pl", "preparation": "test test",
             "author": "test3", "ingredients": [
                {"title": "test1", "amount": 3, "unit": "kg"},
                {"title": "test2"}]}
        ]
        return waiting_recipes

    def test_waiting_recipes_two_recipes(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)

        self.smart_login('test', 'test')

        self.navbar.go_to_waiting_page()
        waiting_recipes_page = wait_page_changes(home_page, WaitingRecipesPage(self.driver))

        self.assertEqual(len(waiting_recipes_page.recipes), 2,
                         msg="Waiting recipes count is correct")

    def test_waiting_recipes_no_recipes(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)

        self.smart_login('test2', 'test')

        self.navbar.go_to_waiting_page()
        waiting_recipes_page = wait_page_changes(home_page, WaitingRecipesPage(self.driver))

        self.assertEqual(len(waiting_recipes_page.recipes), 0,
                         msg="Waiting recipes count is correct")

    def test_waiting_recipes_admin_sees_all(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)

        self.smart_login('admin', 'admin')

        self.navbar.go_to_waiting_page()
        waiting_recipes_page = wait_page_changes(home_page, WaitingRecipesPage(self.driver))

        self.assertEqual(len(waiting_recipes_page.recipes), 3,
                         msg="Waiting recipes count is correct")

    def test_my_recipes_two_recipes(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)

        self.smart_login('test2', 'test')

        self.navbar.go_to_my_recipes_page()
        my_recipes_page = wait_page_changes(home_page, MyRecipesPage(self.driver))

        self.assertEqual(len(my_recipes_page.recipes), 2,
                         msg="My recipes count is correct")

    def test_my_recipes_no_recipes(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)

        self.smart_login('test', 'test')

        self.navbar.go_to_my_recipes_page()
        my_recipes_page = wait_page_changes(home_page, MyRecipesPage(self.driver))

        self.assertEqual(len(my_recipes_page.recipes), 0,
                         msg="My recipes count is correct")

    def test_anonymous_sees_all_accepted_recipes(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)

        self.assertEqual(len(home_page.recipes), 3,
                         msg="Recipes count is correct")
