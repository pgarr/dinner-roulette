from unittest import TestCase

from selenium import webdriver

from utils.aut import Aut


class BaseTest(TestCase):
    def setUp(self):
        # run aut
        self.aut = Aut()
        self.aut.run(10)

        # set language preferences
        options = webdriver.ChromeOptions()
        options.add_argument('--lang=en')

        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()
        self.aut.stop()
