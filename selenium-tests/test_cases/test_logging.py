from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from base_test import BaseTest
from config import MAX_LOADING_TIME
from models.pages import HomePage, LoginPage, WaitingRecipesPage, NewRecipePage


class LoggingUserTest(BaseTest):
    def test_login(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)
        login_page = home_page.go_to_login_page()
        self.assertTrue(login_page.is_title_correct())
        login_page.login('test', 'test')

        wait = WebDriverWait(self.driver, MAX_LOADING_TIME)

        try:
            page_loaded = wait.until_not(lambda driver: login_page.is_title_correct())
        except TimeoutException:
            self.fail("Loading timeout expired")

        self.assertTrue(home_page.is_title_correct())
        self.assertEqual(home_page.user_name, 'test')

    def test_add_recipe_leads_to_login_if_not_logged(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)
        home_page.add_recipe_button.click()

        wait = WebDriverWait(self.driver, MAX_LOADING_TIME)
        try:
            page_loaded = wait.until_not(lambda driver: home_page.is_title_correct())
        except TimeoutException:
            self.fail("Loading timeout expired")

        login_page = LoginPage(self.driver)
        self.assertTrue(login_page.is_title_correct())

    def test_waiting_recipes_leads_to_login_if_not_logged(self):
        waiting_recipes_page = WaitingRecipesPage(self.driver)
        self.driver.get(waiting_recipes_page.url)

        login_page = LoginPage(self.driver)
        self.assertTrue(login_page.is_title_correct())

    def test_when_add_recipe_leads_to_logging_logging_leads_to_add_recipe(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)
        home_page.add_recipe_button.click()

        wait = WebDriverWait(self.driver, MAX_LOADING_TIME)
        try:
            page_loaded = wait.until_not(lambda driver: home_page.is_title_correct())
        except TimeoutException:
            self.fail("Loading timeout expired")

        login_page = LoginPage(self.driver)
        self.assertTrue(login_page.is_title_correct())

        login_page.login("test", "test")

        try:
            page_loaded = wait.until_not(lambda driver: login_page.is_title_correct())
        except TimeoutException:
            self.fail("Loading timeout expired")

        new_recipe_page = NewRecipePage(self.driver)
        self.assertTrue(new_recipe_page.is_title_correct())
