from selenium.common.exceptions import NoSuchElementException

from utils.errors import NotLoggedInError, UserLoggedInError
from models.locators import BasePageLocators, LoginPageLocators


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
        except NoSuchElementException as e:
            raise UserLoggedInError from e

    @property
    def user_menu_dropdown(self):
        """Visible for logged in user"""
        try:
            return self.driver.find_element(*BasePageLocators.USER_MENU_DROPDOWN)
        except NoSuchElementException as e:
            raise NotLoggedInError from e

    @property
    def waiting_recipes_button(self):
        """Visible for logged in user"""
        try:
            return self.driver.find_element(*BasePageLocators.WAITING_RECIPES_BUTTON)
        except NoSuchElementException as e:
            raise NotLoggedInError from e

    @property
    def logout_button(self):
        """Visible for logged in user"""
        try:
            return self.driver.find_element(*BasePageLocators.LOGOUT_BUTTON)
        except NoSuchElementException as e:
            raise NotLoggedInError from e

    @property
    def user_name(self):
        return self.user_menu_dropdown.text

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
        return super().url + '/index'


class LoginPage(BasePage):

    @property
    def url(self):
        return super().url + '/auth/login'

    @property
    def username_field(self):
        return self.driver.find_element(*LoginPageLocators.USERNAME_FIELD)

    @property
    def password_field(self):
        return self.driver.find_element(*LoginPageLocators.PASSWORD_FIELD)

    @property
    def remember_me_checkbox(self):
        return self.driver.find_element(*LoginPageLocators.REMEMBER_ME_CHECKBOX)

    @property
    def submit_button(self):
        return self.driver.find_element(*LoginPageLocators.SUBMIT_BUTTON)

    @property
    def new_user_button(self):
        return self.driver.find_element(*LoginPageLocators.NEW_USER_BUTTON)

    @property
    def forgotten_password_button(self):
        return self.driver.find_element(*LoginPageLocators.FORGOTTEN_PASSWORD_BUTTON)

    def login(self, username, password):
        self.username_field.send_keys(username)
        self.password_field.send_keys(password)
        self.submit_button.click()
        return HomePage(self.driver)
