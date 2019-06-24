from unittest import TestCase

from selenium import webdriver


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
        self.driver.get('http://127.0.0.1:5000')
        login_link = self.driver.find_element_by_xpath('//*[@id="navbarTogglerBasic"]/ul/li[2]/a')
        login_link.click()
        self.assertEqual('Zaloguj się - Cookbook', self.driver.title)  # TODO: i18n - use english
        # TODO: login
