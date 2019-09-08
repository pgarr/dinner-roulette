from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from base_test import BaseTest
from config import MAX_LOADING_TIME
from models.pages import HomePage, LoginPage, WaitingRecipesPage, NewRecipePage


class LoggingUserTest(BaseTest):
    def test_login(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)

        home_page.go_to_login_page()
        login_page = LoginPage(self.driver)

        self.assertTrue(login_page.is_title_correct())
        login_page.login('test', 'test')
        self.wait_page_changes(login_page, home_page)

        self.assertEqual(home_page.user_name, 'test')

    def test_add_recipe_leads_to_login_if_not_logged(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)
        home_page.go_to_new_recipe_page()
        login_page = self.wait_page_changes(home_page, LoginPage(self.driver))

    def test_waiting_recipes_leads_to_login_if_not_logged(self):
        waiting_recipes_page = WaitingRecipesPage(self.driver)
        self.driver.get(waiting_recipes_page.url)

        login_page = LoginPage(self.driver)
        self.assertTrue(login_page.is_title_correct())

    def test_when_add_recipe_leads_to_logging_logging_leads_to_add_recipe(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)
        home_page.go_to_new_recipe_page()
        login_page = self.wait_page_changes(home_page, LoginPage(self.driver))

        login_page.login("test", "test")
        new_recipe_page = self.wait_page_changes(login_page, NewRecipePage(self.driver))
