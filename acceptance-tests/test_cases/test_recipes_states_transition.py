from base_test import BaseTest
from models.pages import HomePage, NewRecipePage, WaitingRecipePage, WaitingRecipesPage, RecipePage


class RecipesStatesTransitionTest(BaseTest):

    def setUp_users(self):
        return [{"username": "test", "email": "test@test.com", "password": "test"},
                {"username": "admin", "email": "admin@test.com", "password": "admin"}]

    def setUp_recipes(self):
        recipes = [
            {"title": "test", "time": 30, "difficulty": 3, "link": "http://test.pl", "preparation": "test test",
             "author": "test", "ingredients": [
                {"title": "test1", "amount": 3, "unit": "kg"},
                {"title": "test2"}]}
        ]
        return recipes

    def setUp_waiting_recipes(self):
        waiting_recipes = [
            {"title": "test", "time": 30, "difficulty": 3, "link": "http://test.pl", "preparation": "test test",
             "author": "test", "ingredients": [
                {"title": "test1", "amount": 3, "unit": "kg"},
                {"title": "test2"}]}
        ]
        return waiting_recipes

    def test_new_recipe_goes_to_waiting(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)

        self.smart_login('test', 'test')

        home_page.go_to_new_recipe_page()
        new_recipe_page = self.wait_page_changes(home_page, NewRecipePage(self.driver))

        new_recipe_page.name.set_text('New Recipe')
        new_recipe_page.submit()
        waiting_recipe_page = self.wait_page_changes(new_recipe_page, WaitingRecipePage(self.driver))

        waiting_recipe_page.go_to_home_page()
        self.wait_page_changes(waiting_recipe_page, home_page)

        self.assertEqual(len(home_page.recipes), 1,
                         msg="After adding new recipe, recipes count is the same")
        home_page.go_to_waiting_page()
        waiting_list_page = self.wait_page_changes(home_page, WaitingRecipesPage(self.driver))

        self.assertEqual(len(waiting_list_page.recipes), 2,
                         msg="After adding new recipe, waiting recipes count is higher by 1")

    def test_accepted_waiting_recipe_goes_to_accepted(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)

        self.smart_login('admin', 'admin')

        home_page.go_to_waiting_page()
        waiting_list_page = self.wait_page_changes(home_page, WaitingRecipesPage(self.driver))

        waiting_list_page.recipes[0].go_to_details()
        waiting_recipe_page = self.wait_page_changes(waiting_list_page, WaitingRecipePage(self.driver))

        waiting_recipe_page.accept()
        recipe_page = self.wait_page_changes(waiting_recipe_page, RecipePage(self.driver))

        recipe_page.go_to_waiting_page()
        self.wait_page_changes(recipe_page, waiting_list_page)

        self.assertEqual(len(waiting_list_page.recipes), 0,
                         msg="After accepting waiting recipe, waiting recipes count is lesser by 1")

        waiting_list_page.go_to_home_page()
        self.wait_page_changes(waiting_list_page, home_page)

        self.assertEqual(len(home_page.recipes), 2,
                         msg="After accepting waiting recipe, accepted recipes count is higher by 1")

    def test_updated_recipe_goes_to_waiting_but_old_stays_in_accepted(self):
        self.fail()

    def test_updated_waiting_recipe_stays_updated_in_waiting(self):
        self.fail()

    def test_accepted_waiting_updates_overrides_accepted_recipe(self):
        self.fail()
