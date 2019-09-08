import time

from models.pages import HomePage, LoginPage, WaitingRecipesPage, NewRecipePage, WaitingRecipePage, ErrorPage
from base_test import BaseTest


class RecipesVisibilityTest(BaseTest):

    def test_new_recipes_is_in_waiting_list(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)
        recipes_count = len(home_page.recipes)
        home_page.go_to_login_page()
        login_page = self.wait_page_changes(home_page, LoginPage(self.driver))

        login_page.login('test', 'test')
        self.wait_page_changes(login_page, home_page)

        home_page.go_to_waiting_page()
        waiting_recipes_page = self.wait_page_changes(home_page, WaitingRecipesPage(self.driver))

        waiting_recipes_count = len(waiting_recipes_page.recipes)
        waiting_recipes_page.go_to_new_recipe_page()
        new_recipe_page = self.wait_page_changes(waiting_recipes_page, NewRecipePage(self.driver))

        new_recipe_page.name.set_text('Test')
        new_recipe_page.submit()
        waiting_recipe_page = self.wait_page_changes(new_recipe_page, WaitingRecipePage(self.driver))

        waiting_recipe_page.go_to_home_page()
        self.wait_page_changes(waiting_recipe_page, home_page)

        self.assertEqual(len(home_page.recipes), recipes_count,
                         msg="After adding new recipe, recipes count is the same")
        home_page.go_to_waiting_page()
        self.wait_page_changes(home_page, waiting_recipes_page)

        self.assertEqual(len(waiting_recipes_page.recipes), waiting_recipes_count + 1,
                         msg="After adding new recipe, waiting recipes count is higher by 1")

    def test_waiting_recipe_not_visible_for_other_user(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)
        home_page.go_to_login_page()
        login_page = self.wait_page_changes(home_page, LoginPage(self.driver))

        login_page.login('test', 'test')
        self.wait_page_changes(login_page, home_page)

        home_page.go_to_waiting_page()
        waiting_recipes_page = self.wait_page_changes(home_page, WaitingRecipesPage(self.driver))

        waiting_recipes_count = len(waiting_recipes_page.recipes)
        waiting_recipes_page.logout()
        self.wait_page_changes(waiting_recipes_page, home_page)

        home_page.go_to_login_page()
        self.wait_page_changes(home_page, login_page)

        login_page.login('test2', 'test')
        self.wait_page_changes(login_page, home_page)
        home_page.go_to_new_recipe_page()
        new_recipe_page = self.wait_page_changes(waiting_recipes_page, NewRecipePage(self.driver))

        new_recipe_page.name.set_text('Test')
        new_recipe_page.submit()
        waiting_recipe_page = self.wait_page_changes(new_recipe_page, WaitingRecipePage(self.driver))

        waiting_link = self.driver.current_url
        waiting_recipe_page.logout()
        self.wait_page_changes(waiting_recipe_page, home_page)

        home_page.go_to_login_page()
        self.wait_page_changes(home_page, login_page)

        login_page.login('test', 'test')
        self.wait_page_changes(login_page, home_page)

        home_page.go_to_waiting_page()
        self.wait_page_changes(home_page, waiting_recipes_page)

        self.assertEqual(len(waiting_recipes_page.recipes), waiting_recipes_count,
                         msg="New waiting recipe is not visible for other user")

        self.driver.get(waiting_link)
        error_page = ErrorPage(self.driver)
        self.assertEqual(error_page.message, 'You are not allowed to do this',
                         msg="Waiting recipe can't be accessed by user different than author")
