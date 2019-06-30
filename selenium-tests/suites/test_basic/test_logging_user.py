from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from models.pages import HomePage
from suites.test_basic.base_test import BaseTest


class LoggingUserTest(BaseTest):

    def test_login(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)
        login_page = home_page.go_to_login_page()
        self.assertTrue(login_page.is_url_correct())
        login_page.login('test', 'test')

        wait = WebDriverWait(self.driver, 5)

        try:
            page_loaded = wait.until_not(lambda driver: login_page.is_url_correct())
        except TimeoutException:
            self.fail("Loading timeout expired")

        self.assertTrue(home_page.is_url_correct())
        self.assertEqual(home_page.user_name, 'test')
