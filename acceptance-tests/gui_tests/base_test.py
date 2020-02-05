import os
from unittest import TestCase

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

from config import MAX_LOADING_TIME
from gui_tests.helpers import wait_page_changes
from gui_tests.models.pages import BasePage, LoginPage, NavigationBar
from utils.aut import Aut


class BaseTest(TestCase):

    def setUp_users(self):
        return [{"username": "test", "email": "test@test.com", "password": "test"},
                {"username": "test2", "email": "test2@test.com", "password": "test"},
                {"username": "admin", "email": "admin@test.com", "password": "admin"}]

    def setUp_recipes(self):
        return None

    def setUp_waiting_recipes(self):
        return None

    @classmethod
    def setUpClass(cls):
        basedir = os.path.abspath(os.path.dirname(__file__))
        load_dotenv(os.path.join(basedir, '..', '.env'))

    def setUp(self):
        # run aut
        self._aut = Aut(users=self.setUp_users(), recipes=self.setUp_recipes(),
                        waiting_recipes=self.setUp_waiting_recipes())
        self._aut.run(10)
        # set language preferences
        options = webdriver.ChromeOptions()
        options.add_argument('--lang=en')

        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()

        self.wait = WebDriverWait(self.driver, MAX_LOADING_TIME)
        self.navbar = NavigationBar(self.driver)

    def tearDown(self):
        self.driver.quit()
        self._aut.stop()

    # helper methods:

    def smart_login(self, login, password):
        """logs in with credentials, but first logs out if already logged in with different user"""
        base_page = BasePage(self.driver)

        if self.navbar.user_name != login:
            try:
                self.navbar.logout()
                # wait until name is None
                try:
                    page_loaded = self.wait.until_not(lambda driver: self.navbar.user_name)
                except TimeoutException:
                    self.fail("Loading timeout expired")
            except NoSuchElementException:
                pass
            self.navbar.go_to_login_page()
            login_page = wait_page_changes(base_page, LoginPage(self.driver))

            login_page.login(login, password)
            wait_page_changes(current_page=login_page)

            self.assertEqual(self.navbar.user_name, login)
