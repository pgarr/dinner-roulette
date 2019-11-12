import os
from unittest import TestCase

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from config import MAX_LOADING_TIME
from models.pages import BasePage
from utils.aut import Aut


class BaseTest(TestCase):
    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        load_dotenv(os.path.join(basedir, '.env'))
        # run aut
        self.aut = Aut()
        self.aut.run(10)

        # set language preferences
        options = webdriver.ChromeOptions()
        options.add_argument('--lang=en')

        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()

        self.wait = WebDriverWait(self.driver, MAX_LOADING_TIME)

    def tearDown(self):
        self.driver.quit()
        self.aut.stop()

    def wait_for_change_page(self, current_page: BasePage):
        try:
            page_loaded = self.wait.until_not(lambda driver: current_page.is_title_correct())
        except TimeoutException:
            self.fail("Loading timeout expired")
