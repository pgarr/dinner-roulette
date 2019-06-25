from unittest import TestCase

from selenium import webdriver

from models.pages import HomePage


class BaseTest(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    def test_online(self):
        self.driver.get('http://127.0.0.1:5000')
        self.assertEqual('Strona domowa - Cookbook', self.driver.title)  # TODO: i18n  - use english

    def test_login(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)
        login_page = home_page.go_to_login_page()
        self.assertEqual('Zaloguj się - Cookbook', login_page.title)  # TODO: i18n - use english
        self.assertTrue(login_page.is_url_correct())
        # TODO: login
