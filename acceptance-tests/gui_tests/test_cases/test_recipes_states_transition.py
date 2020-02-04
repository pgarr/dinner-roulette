from gui_tests.base_test import BaseTest
from gui_tests.models.pages import NewRecipePage, WaitingRecipePage, WaitingRecipesPage, RecipePage, HomePage, \
    EditRecipePage, EditWaitingRecipePage


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


class RecipesUpdatesTest(BaseTest):

    def setUp_recipes(self):
        return [
            {"title": "accepted", "time": 30, "difficulty": 3, "link": "http://test.pl", "preparation": "test test",
             "author": "test", "ingredients": [
                {"title": "test1", "amount": 3, "unit": "kg"},
                {"title": "test2"}]},
            {"title": "accepted_waiting_updates", "time": 10, "difficulty": 1, "link": "http://test.pl",
             "preparation": "test test",
             "author": "test2", "ingredients": [
                {"title": "test1", "amount": 1, "unit": "g"},
                {"title": "test2"}]}
        ]

    def setUp_waiting_recipes(self):
        return [
            {"title": "waiting", "time": 30, "difficulty": 3, "link": "http://test.pl", "preparation": "test test",
             "author": "test2", "ingredients": [
                {"title": "test1", "amount": 3, "unit": "kg"},
                {"title": "test2"}]},
            {"title": "waiting_updates", "time": 10, "difficulty": 1, "link": "http://test.pl",
             "preparation": "test test", "author": "test2", "updated_recipe": "accepted_waiting_updates",
             "ingredients": [
                 {"title": "test1", "amount": 3, "unit": "kg"},
                 {"title": "test2"}]}
        ]

    def test_updated_recipe_goes_to_waiting_but_old_stays_in_accepted(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)

        self.smart_login('test', 'test')

        home_page.recipes[1].go_to_details()
        recipe_page = self.wait_page_changes(home_page, RecipePage(self.driver))

        recipe_page.edit()
        edit_recipe_page = self.wait_page_changes(recipe_page, EditRecipePage(self.driver))

        edit_recipe_page.name.set_text('updated')
        edit_recipe_page.submit()
        waiting_recipe_page = self.wait_page_changes(edit_recipe_page, WaitingRecipePage(self.driver))

        waiting_recipe_page.go_to_home_page()
        self.wait_page_changes(waiting_recipe_page, home_page)

        self.assertEqual('accepted', home_page.recipes[1].name)

        home_page.go_to_waiting_page()
        waiting_list_page = self.wait_page_changes(home_page, WaitingRecipesPage(self.driver))

        self.assertEqual('updated', waiting_list_page.recipes[0].name)

    def test_updated_waiting_recipe_stays_updated_in_waiting(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)

        self.smart_login('test2', 'test')

        home_page.go_to_waiting_page()
        waiting_list_page = self.wait_page_changes(home_page, WaitingRecipesPage(self.driver))

        waiting_list_page.recipes[0].go_to_details()
        waiting_recipe_page = self.wait_page_changes(home_page, WaitingRecipePage(self.driver))

        waiting_url = self.driver.current_url

        waiting_recipe_page.edit()
        edit_waiting_page = self.wait_page_changes(waiting_recipe_page, EditWaitingRecipePage(self.driver))

        edit_waiting_page.name.set_text('updated')
        edit_waiting_page.submit()
        self.wait_page_changes(edit_waiting_page, waiting_recipe_page)

        # verify this is the same recipe (url)
        self.assertEqual(self.driver.current_url, waiting_url)

        waiting_recipe_page.go_to_home_page()
        self.wait_page_changes(waiting_recipe_page, home_page)

        self.assertEqual(len(home_page.recipes), 2, msg="No new accepted recipe was created")

        home_page.go_to_waiting_page()
        self.wait_page_changes(home_page, waiting_list_page)

        self.assertEqual(len(waiting_list_page.recipes), 2, msg="No new waiting recipe was created")

    def test_accepted_waiting_updates_overrides_accepted_recipe(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)

        self.smart_login('admin', 'admin')

        home_page.recipes[0].go_to_details()
        recipe_page = self.wait_page_changes(home_page, RecipePage(self.driver))

        recipe_url = self.driver.current_url

        recipe_page.go_to_waiting_page()
        waiting_list_page = self.wait_page_changes(recipe_page, WaitingRecipesPage(self.driver))

        waiting_list_page.recipes[1].go_to_details()
        waiting_recipe_page = self.wait_page_changes(waiting_list_page, WaitingRecipePage(self.driver))

        waiting_recipe_page.accept()
        self.wait_page_changes(waiting_recipe_page, recipe_page)

        self.assertEqual(self.driver.current_url, recipe_url)

        recipe_page.go_to_home_page()
        self.wait_page_changes(recipe_page, home_page)

        self.assertEqual(len(home_page.recipes), 2, msg="No new accepted recipe was created")
        self.assertEqual("waiting_updates", home_page.recipes[0].name, msg="Name was updated")

        home_page.go_to_waiting_page()
        self.wait_page_changes(home_page, waiting_list_page)

        self.assertEqual(len(waiting_list_page.recipes), 1, msg="Accepted waiting recipe was removed from waiting list")
