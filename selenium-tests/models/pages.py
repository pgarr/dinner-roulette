from selenium.common.exceptions import NoSuchElementException

from errors import NotLoggedInError, UserLoggedInError
from models.locators import BasePageLocators


class BasePage:
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver

    @property
    def url(self):
        return 'http://127.0.0.1:5000'

    @property
    def title(self):
        return self.driver.title

    @property
    def home_button(self):
        return self.driver.find_element(*BasePageLocators.HOME_BUTTON)

    @property
    def add_recipe_button(self):
        return self.driver.find_element(*BasePageLocators.ADD_RECIPE_BUTTON)

    @property
    def login_button(self):
        """Visible if user is not logged in"""
        try:
            return self.driver.find_element(*BasePageLocators.LOGIN_BUTTON)
        except NoSuchElementException:
            raise UserLoggedInError

    @property
    def user_menu_dropdown(self):
        """Visible for logged in user"""
        try:
            return self.driver.find_element(*BasePageLocators.USER_MENU_DROPDOWN)
        except NoSuchElementException:
            raise NotLoggedInError

    @property
    def waiting_recipes_button(self):
        """Visible for logged in user"""
        try:
            return self.driver.find_element(*BasePageLocators.WAITING_RECIPES_BUTTON)
        except NoSuchElementException:
            raise NotLoggedInError()

    @property
    def logout_button(self):
        """Visible for logged in user"""
        try:
            return self.driver.find_element(*BasePageLocators.LOGOUT_BUTTON)
        except NoSuchElementException:
            raise NotLoggedInError()

    @property
    def user_name(self):
        return self.user_menu_dropdown.text()

    def is_url_correct(self):
        return self.driver.current_url == self.url

    def go_to_login_page(self):
        self.login_button.click()
        return LoginPage(self.driver)

    def go_to_home_page(self):
        self.home_button.click()
        return HomePage(self.driver)


class HomePage(BasePage):

    @property
    def url(self):
        return super().url + '/'


class LoginPage(BasePage):

    @property
    def url(self):
        return super().url + '/auth/login'
