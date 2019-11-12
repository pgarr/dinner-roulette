from base_test import BaseTest
from models.pages import HomePage, WaitingRecipesPage, NewRecipePage, WaitingRecipePage, ErrorPage, \
    RecipePage


class RecipesVisibilityTest(BaseTest):

    def test_new_recipes_is_in_waiting_list(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)
        recipes_count = len(home_page.recipes)

        self.smart_login('test', 'test')

        home_page.go_to_waiting_page()
        waiting_list_page = self.wait_page_changes(home_page, WaitingRecipesPage(self.driver))

        waiting_recipes_count = len(waiting_list_page.recipes)
        waiting_list_page.go_to_new_recipe_page()
        new_recipe_page = self.wait_page_changes(waiting_list_page, NewRecipePage(self.driver))

        new_recipe_page.name.set_text('Test')
        new_recipe_page.submit()
        waiting_recipe_page = self.wait_page_changes(new_recipe_page, WaitingRecipePage(self.driver))

        waiting_recipe_page.go_to_home_page()
        self.wait_page_changes(waiting_recipe_page, home_page)

        self.assertEqual(len(home_page.recipes), recipes_count,
                         msg="After adding new recipe, recipes count is the same")
        home_page.go_to_waiting_page()
        self.wait_page_changes(home_page, waiting_list_page)

        self.assertEqual(len(waiting_list_page.recipes), waiting_recipes_count + 1,
                         msg="After adding new recipe, waiting recipes count is higher by 1")

    def test_waiting_recipe_not_visible_for_other_user(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)

        self.smart_login('test', 'test')

        home_page.go_to_waiting_page()
        waiting_list_page = self.wait_page_changes(home_page, WaitingRecipesPage(self.driver))

        waiting_recipes_count = len(waiting_list_page.recipes)

        self.smart_login('test2', 'test')

        home_page.go_to_new_recipe_page()
        new_recipe_page = self.wait_page_changes(waiting_list_page, NewRecipePage(self.driver))

        new_recipe_page.name.set_text('Test')
        new_recipe_page.submit()
        waiting_recipe_page = self.wait_page_changes(new_recipe_page, WaitingRecipePage(self.driver))

        waiting_link = self.driver.current_url

        self.smart_login('test', 'test')

        home_page.go_to_waiting_page()
        self.wait_page_changes(home_page, waiting_list_page)

        self.assertEqual(len(waiting_list_page.recipes), waiting_recipes_count,
                         msg="New waiting recipe is not visible for other user")

        self.driver.get(waiting_link)
        error_page = ErrorPage(self.driver)
        self.assertEqual(error_page.message, 'You are not allowed to do this',
                         msg="Waiting recipe can't be accessed by user different than author")

    def test_accepted_new_recipe_is_in_recipes_list(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)
        recipes_count = len(home_page.recipes)

        self.smart_login('test', 'test')

        home_page.go_to_waiting_page()
        waiting_list_page = self.wait_page_changes(home_page, WaitingRecipesPage(self.driver))

        waiting_recipes_count = len(waiting_list_page.recipes)
        waiting_list_page.go_to_new_recipe_page()
        new_recipe_page = self.wait_page_changes(waiting_list_page, NewRecipePage(self.driver))

        new_recipe_page.name.set_text('Test')
        new_recipe_page.submit()
        waiting_recipe_page = self.wait_page_changes(new_recipe_page, WaitingRecipePage(self.driver))

        waiting_link = self.driver.current_url

        self.smart_login('admin', 'admin')

        self.driver.get(waiting_link)
        self.assertTrue(waiting_recipe_page.is_title_correct())
        waiting_recipe_page.accept()

        recipe_page = self.wait_page_changes(waiting_recipe_page, RecipePage(self.driver))

        self.smart_login('test', 'test')

        self.assertEqual(len(home_page.recipes), recipes_count + 1,
                         msg="After accepting new recipe, recipes count is higher by 1")

        home_page.go_to_waiting_page()
        self.wait_page_changes(home_page, waiting_list_page)

        self.assertEqual(len(waiting_list_page.recipes), waiting_recipes_count,
                         msg="After accepting new recipe, waiting recipes count is same as before adding this recipe")
