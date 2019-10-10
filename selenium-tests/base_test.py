import os
from unittest import TestCase

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

from config import MAX_LOADING_TIME
from models.pages import BasePage
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

    def wait_page_changes(self, current_page: BasePage, expected_page: BasePage):
        try:
            page_loaded = self.wait.until_not(lambda driver: current_page.is_title_correct())
        except TimeoutException:
            self.fail("Loading timeout expired")
        self.assertTrue(expected_page.is_title_correct())
        return expected_page
