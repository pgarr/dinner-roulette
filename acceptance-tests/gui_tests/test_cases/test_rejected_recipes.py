from gui_tests.base_test import BaseTest
from gui_tests.helpers import wait_page_changes
from gui_tests.models.pages import HomePage, WaitingRecipesPage, RecipePage, WaitingRecipePage, \
    EditWaitingRecipePage


class RejectedRecipesTest(BaseTest):

    def setUp_recipes(self):
        return [
            {"title": "accepted", "time": 30, "difficulty": 3, "link": "http://test.pl", "preparation": "test test",
             "author": "test", "ingredients": [
                {"title": "test1", "amount": 3, "unit": "kg"},
                {"title": "test2"}]},
        ]

    def setUp_waiting_recipes(self):
        return [
            {"title": "rejected", "time": 30, "difficulty": 3, "link": "http://test.pl", "preparation": "test test",
             "author": "test", "updated_recipe": "accepted", "refused": True, "ingredients": [
                {"title": "test1", "amount": 3, "unit": "kg"},
                {"title": "test2"}]},
            {"title": "waiting", "time": 10, "difficulty": 1, "link": "http://test.pl",
             "preparation": "test test", "author": "test", "ingredients": [
                {"title": "test1", "amount": 3, "unit": "kg"},
                {"title": "test2"}]}
        ]

    def test_user_sees_his_rejected_recipe_on_list(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)

        self.navbar.smart_login(home_page, 'test', 'test')

        self.navbar.go_to_waiting_page()
        waiting_recipes_page = wait_page_changes(home_page, WaitingRecipesPage(self.driver))

        self.assertEqual(len(waiting_recipes_page.recipes), 2)

    def test_admin_dont_see_rejected_recipe_on_list(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)

        self.navbar.smart_login(home_page, 'admin', 'admin')

        self.navbar.go_to_waiting_page()
        waiting_recipes_page = wait_page_changes(home_page, WaitingRecipesPage(self.driver))

        self.assertEqual(len(waiting_recipes_page.recipes), 1)

    def test_new_updates_overrides_rejected_updates(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)

        self.navbar.smart_login(home_page, 'test', 'test')

        home_page.recipes[0].go_to_details()
        recipe_page = wait_page_changes(home_page, RecipePage(self.driver))

        recipe_page.edit()
        edit_waiting_page = wait_page_changes(recipe_page, EditWaitingRecipePage(self.driver))

        self.assertEqual(edit_waiting_page.name.get_text(), 'rejected')

        edit_waiting_page.name.set_text('new_name')
        edit_waiting_page.submit()
        waiting_recipe_page = wait_page_changes(edit_waiting_page, WaitingRecipePage(self.driver))

        self.navbar.go_to_waiting_page()
        waiting_recipes_page = wait_page_changes(waiting_recipe_page, WaitingRecipesPage(self.driver))

        self.assertEqual(len(waiting_recipes_page.recipes), 2)
        self.assertEqual(waiting_recipes_page.recipes[1].name, 'new_name')

    def test_rejecting_recipe(self):
        self.fail()
