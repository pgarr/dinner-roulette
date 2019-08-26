import re

from selenium.common.exceptions import NoSuchElementException

from models.locators import BasePageLocators, LoginPageLocators, HomePageLocators, RecipePageLocators
from utils.errors import NotLoggedInError, UserLoggedInError


class BasePage:
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver
        self._url = 'http://127.0.0.1:5000'

    @property
    def url(self):
        return self._url

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
    class RecipeRow:
        def __init__(self, row):
            self._row = row
            self.index = int(self._row.find_element(*HomePageLocators.RECIPE_INDEX_CELL).text)
            self._tds = self._row.find_elements(
                *HomePageLocators.ROW_CELLS)  # TODO: remove and change childs to css selector
            self.link = self._tds[0].find_element(*HomePageLocators.RECIPE_LINK)
            self.time = int(self._tds[1].text.replace("'", ""))
            self.difficulty = len(self._tds[2].find_elements(*HomePageLocators.DIFFICULTY_STAR))
            self.name = self.link.text

        def go_to_details(self):
            self.link.click()

        def __repr__(self):
            return "RecipeRow: id: %d, name: %s, time: %d, difficulty: %d" % (
                self.index, self.name, self.time, self.difficulty)

    @property
    def url(self):
        return super().url + '/index'

    @property
    def recipes(self):
        rows_container = self.driver.find_element(*HomePageLocators.RECIPES_LIST)
        rows = rows_container.find_elements(*HomePageLocators.RECIPE_ROW)
        recipes = []
        for row in rows:
            recipes.append(self.RecipeRow(row))
        return recipes


class WaitingRecipesPage(HomePage):

    @property
    def url(self):
        return self._url + '/waiting'


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


class RecipePage(BasePage):
    class IngredientRow:
        def __init__(self, row):
            self._row = row
            self.name = self._row.find_element_by_tag_name(*RecipePageLocators.INGREDIENT_NAME).text
            self.amount, self.unit = self._decode_amount()

        def _decode_amount(self):
            text = self._row.find_element_by_tag_name(*RecipePageLocators.INGREDIENT_AMOUNT).text
            match = re.match(r'(?P<amount>\d*) ?(?P<unit>[a-zA-Z]*)', text)
            return int(match.group('amount')), match.group('unit')

        def __repr__(self):
            return "IngredientRow: name: %s, amount: %d, unit: %s" % (self.name, self.amount, self.unit)

    @property
    def url(self):
        return super().url + '/recipe/id'  # TODO: numer

    @property
    def recipe_title(self):
        return self.driver.find_element(*RecipePageLocators.TITLE_HEADER).text

    @property
    def author_name(self):
        text = self.driver.find_element(*RecipePageLocators.AUTHOR_NAME_PTAG).text
        return text.replace('Author: ', '')

    @property
    def preparation_time(self):
        text = self.driver.find_element(*RecipePageLocators.TIME_PTAG).text
        return int(text.replace("'", ''))

    @property
    def difficulty(self):
        return len(self.driver.find_elements(*RecipePageLocators.DIFFICULTY_STAR))

    @property
    def preparation(self):
        return self.driver.find_element(*RecipePageLocators.PREPARATION_PTAG).text

    @property
    def ingredients(self):
        rows_container = self.driver.find_element(*RecipePageLocators.INGREDIENTS_LIST)
        rows = rows_container.find_elements(*RecipePageLocators.INGREDIENT_ROW)
        ingredients = []
        for row in rows:
            ingredients.append(self.IngredientRow(row))
        return ingredients

    @property
    def edit_link(self):
        return self.driver.find_element(*RecipePageLocators.EDIT_LINK)

    @property
    def source_link(self):
        return self.driver.find_element(*RecipePageLocators.SOURCE_LINK)

    def edit(self):
        self.edit_link.click()
        return EditRecipePage(self.driver)


class WaitingRecipePage(RecipePage):
    pass


class NewRecipePage(BasePage):
    pass


class EditRecipePage(BasePage):
    pass


class EditWaitingRecipePage(EditRecipePage):
    pass
