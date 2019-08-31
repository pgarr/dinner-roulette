from models.pages import HomePage, LoginPage, WaitingRecipesPage, NewRecipePage
from base_test import BaseTest


class RecipesVisibilityTest(BaseTest):

    def test_new_recipes_is_in_waiting_list(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)
        recipes_count = len(home_page.recipes)

        home_page.go_to_login_page()

        self.wait_for_load(home_page)
        login_page = LoginPage(self.driver)
        self.assertTrue(login_page.is_title_correct())
        login_page.login('test', 'test')

        self.wait_for_load(login_page)
        home_page.go_to_waiting_page()

        self.wait_for_load(home_page)
        waiting_page = WaitingRecipesPage(self.driver)
        self.assertTrue(waiting_page.is_title_correct())
        waiting_recipes_count = len(waiting_page.recipes)

        waiting_page.go_to_new_recipe_page()

        self.wait_for_load(waiting_page)
        new_recipe_page = NewRecipePage(self.driver)
        self.assertTrue(new_recipe_page.is_title_correct())

        new_recipe_page.name.set_text('Test')
        new_recipe_page.submit()

        self.wait_for_load(new_recipe_page)
        self.driver.get(home_page.url)
        self.assertEqual(len(home_page.recipes), recipes_count,
                         msg="After adding new recipe, recipes count is the same")

        home_page.go_to_waiting_page()
        self.wait_for_load(home_page)
        self.assertTrue(waiting_page.is_title_correct())
        self.assertEqual(len(waiting_page.recipes), waiting_recipes_count + 1,
                         msg="After adding new recipe, waiting recipes count is higher by 1")
