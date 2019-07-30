import time
from unittest import TestCase

from selenium import webdriver


class BaseTest(TestCase):
    def setUp(self):
        # set language preferences
        options = webdriver.ChromeOptions()
        options.add_argument('--lang=en')

        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()
