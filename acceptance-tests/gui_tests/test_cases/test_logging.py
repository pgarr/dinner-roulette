from gui_tests.base_test import BaseTest
from gui_tests.helpers import wait_page_changes
from gui_tests.models.pages import HomePage, LoginPage, WaitingRecipesPage, MyRecipesPage, NewRecipePage


class LoggingUserTest(BaseTest):
    def test_login(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)

        home_page.go_to_login_page()
        login_page = wait_page_changes(home_page, LoginPage(self.driver))

        login_page.login('test', 'test')
        wait_page_changes(login_page, home_page)

        self.assertEqual(home_page.user_name, 'test')

    def test_add_recipe_leads_to_login_if_not_logged(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)
        home_page.go_to_new_recipe_page()
        login_page = wait_page_changes(home_page, LoginPage(self.driver))

    def test_waiting_recipes_leads_to_login_if_not_logged(self):
        waiting_recipes_page = WaitingRecipesPage(self.driver)
        self.driver.get(waiting_recipes_page.url)

        login_page = LoginPage(self.driver)
        self.assertTrue(login_page.is_title_correct())

    def test_my_recipes_leads_to_login_if_not_logged(self):
        my_recipes_page = MyRecipesPage(self.driver)
        self.driver.get(my_recipes_page.url)

        login_page = LoginPage(self.driver)
        self.assertTrue(login_page.is_title_correct())

    def test_when_add_recipe_leads_to_logging_logging_leads_to_add_recipe(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)
        home_page.go_to_new_recipe_page()
        login_page = wait_page_changes(home_page, LoginPage(self.driver))

        login_page.login("test", "test")
        new_recipe_page = wait_page_changes(login_page, NewRecipePage(self.driver))
