import os
from unittest import TestCase

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

from config import MAX_LOADING_TIME
from models.pages import BasePage, LoginPage
from utils.aut import Aut


class BaseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        basedir = os.path.abspath(os.path.dirname(__file__))
        load_dotenv(os.path.join(basedir, '.env'))
        # run aut
        cls._aut = Aut()
        cls._aut.run(10)

    def setUp(self):
        # set language preferences
        options = webdriver.ChromeOptions()
        options.add_argument('--lang=en')

        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()

        self.wait = WebDriverWait(self.driver, MAX_LOADING_TIME)

    def tearDown(self):
        self.driver.quit()

    @classmethod
    def tearDownClass(cls):
        cls._aut.stop()

    # helper methods:
    def wait_page_changes(self, current_page: BasePage, expected_page: BasePage = None):
        try:
            page_loaded = self.wait.until_not(lambda driver: current_page.is_title_correct())
        except TimeoutException:
            self.fail("Loading timeout expired")
        if expected_page:
            self.assertTrue(expected_page.is_title_correct())
            return expected_page
        else:
            return None

    def smart_login(self, login, password):
        base_page = BasePage(self.driver)

        if base_page.user_name != login:
            try:
                base_page.logout()
                # wait until name is None
                try:
                    page_loaded = self.wait.until_not(lambda driver: base_page.user_name)
                except TimeoutException:
                    self.fail("Loading timeout expired")
            except NoSuchElementException:
                pass
            base_page.go_to_login_page()
            login_page = self.wait_page_changes(base_page, LoginPage(self.driver))

            login_page.login(login, password)
            self.wait_page_changes(current_page=login_page)

            self.assertEqual(base_page.user_name, login)
