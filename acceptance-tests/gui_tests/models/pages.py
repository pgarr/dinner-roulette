import os
import re

from selenium.common.exceptions import NoSuchElementException

from gui_tests.models.elements import TextFieldElement
from gui_tests.models.locators import BasePageLocators, HomePageLocators, LoginPageLocators, RecipePageLocators, \
    NewRecipePageLocators, WaitingRecipePageLocators, ErrorPageLocators


class NavigationBar:
    def __init__(self, driver):
        self.driver = driver

    @property
    def home_button(self):
        return self.driver.find_element(*BasePageLocators.HOME_BUTTON)

    @property
    def add_recipe_button(self):
        return self.driver.find_element(*BasePageLocators.ADD_RECIPE_BUTTON)

    @property
    def login_button(self):
        """Visible if user is not logged in"""
        return self.driver.find_element(*BasePageLocators.LOGIN_BUTTON)

    @property
    def user_menu_dropdown(self):
        """Visible for logged in user"""
        return self.driver.find_element(*BasePageLocators.USER_MENU_DROPDOWN)

    @property
    def waiting_recipes_button(self):
        """Visible for logged in user"""
        return self.driver.find_element(*BasePageLocators.WAITING_RECIPES_BUTTON)

    @property
    def my_recipes_button(self):
        """Visible for logged in user"""
        return self.driver.find_element(*BasePageLocators.MY_RECIPES_BUTTON)

    @property
    def logout_button(self):
        """Visible for logged in user"""
        return self.driver.find_element(*BasePageLocators.LOGOUT_BUTTON)

    @property
    def user_name(self):
        try:
            return self.user_menu_dropdown.text
        except NoSuchElementException:
            return None

    def go_to_login_page(self):
        self.login_button.click()

    def go_to_home_page(self):
        self.home_button.click()

    def go_to_waiting_page(self):
        self.user_menu_dropdown.click()
        self.waiting_recipes_button.click()

    def go_to_new_recipe_page(self):
        self.add_recipe_button.click()

    def go_to_my_recipes_page(self):
        self.user_menu_dropdown.click()
        self.my_recipes_button.click()

    def logout(self):
        self.user_menu_dropdown.click()
        self.logout_button.click()


class BasePage:
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver
        self._url = 'http://127.0.0.1:' + os.environ.get('AUT_PORT')

    @property
    def url(self):
        return self._url

    @property
    def title(self):
        return "Base Page"

    def is_url_correct(self):
        return self.driver.current_url == self.url

    def is_title_correct(self):
        return self.driver.title == self.title


class BasePageUrlRegex(BasePage):

    @property
    def url(self):
        raise ValueError("Url is dynamic!")  # TODO

    @property
    def url_regex(self):
        return self._url

    def is_url_correct(self):
        match = re.match(self.url_regex, self.driver.current_url)
        return True if match else False


class HomePage(BasePage):
    class RecipeRow:
        def __init__(self, row):
            self._row = row
            self.index = int(self._row.find_element(*HomePageLocators.RECIPE_INDEX_CELL).text)
            self._tds = self._row.find_elements(*HomePageLocators.ROW_CELLS)
            self.link = self._tds[0].find_element(*HomePageLocators.RECIPE_LINK)
            try:
                self.time = int(self._tds[1].text.replace("'", ""))
            except ValueError:
                self.time = None
            self.difficulty = len(self._tds[2].find_elements(*HomePageLocators.DIFFICULTY_STAR))
            self.name = self.link.text

        def go_to_details(self):
            self.link.click()

        def __repr__(self):
            return "RecipeRow: id: %d, name: %s, time: %d, difficulty: %d" % (
                self.index, self.name, self.time, self.difficulty)

    @property
    def url(self):
        return self._url + '/index'

    @property
    def title(self):
        return "Home Page - Cookbook"

    @property
    def recipes(self):
        rows = self.driver.find_elements(*HomePageLocators.RECIPE_ROW)
        recipes = []
        for row in rows:
            recipes.append(self.RecipeRow(row))
        return recipes


class WaitingRecipesPage(HomePage):

    @property
    def url(self):
        return self._url + '/waiting'

    @property
    def title(self):
        return "Waiting Recipes - Cookbook"


class MyRecipesPage(HomePage):
    @property
    def url(self):
        return self._url + '/recipes/my'

    @property
    def title(self):
        return "My Recipes - Cookbook"


class LoginPage(BasePage):

    @property
    def url(self):
        return self._url + '/auth/login'

    @property
    def title(self):
        return "Sign In - Cookbook"

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


class RecipePage(BasePageUrlRegex):
    class IngredientRow:
        def __init__(self, row):
            self._row = row
            self.name = self._row.find_element(*RecipePageLocators.INGREDIENT_NAME).text
            self.amount, self.unit = self._decode_amount()

        def _decode_amount(self):
            text = self._row.find_element(*RecipePageLocators.INGREDIENT_AMOUNT).text
            match = re.match(r'(?P<amount>\d*) ?(?P<unit>[a-zA-Z]*)', text)
            return int(match.group('amount')), match.group('unit')

        def __repr__(self):
            return "IngredientRow: name: %s, amount: %d, unit: %s" % (self.name, self.amount, self.unit)

    @property
    def url_regex(self):
        return self._url + '/recipe/(?P<id>\d+)'

    @property
    def title(self):
        return "Recipe - Cookbook"

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
        rows = self.driver.find_elements(*RecipePageLocators.INGREDIENT_ROW)
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


class WaitingRecipePage(RecipePage):

    @property
    def url_regex(self):
        return self._url + '/waiting/(?P<id>\d+)'

    @property
    def title(self):
        return "Waiting Recipe - Cookbook"

    @property
    def accept_link(self):
        return self.driver.find_element(*WaitingRecipePageLocators.ACCEPT_LINK)

    def accept(self):
        self.accept_link.click()


class NewRecipePage(BasePage):
    class IngredientRow:
        def __init__(self, driver, row_id):
            self.name = TextFieldElement(driver,
                                         self._make_locator(row_id, *NewRecipePageLocators.INGREDIENT_NAME_FIELD))
            self.amount = TextFieldElement(driver,
                                           self._make_locator(row_id, *NewRecipePageLocators.INGREDIENT_AMOUNT_FIELD))
            self.unit = TextFieldElement(driver,
                                         self._make_locator(row_id, *NewRecipePageLocators.INGREDIENT_UNIT_FIELD))

        def _make_locator(self, row_id, method, text):
            numbered_text = text % row_id
            return method, numbered_text

        def __repr__(self):
            return "IngredientRow: name: %s, amount: %d, unit: %s" % (
                self.name.get_text(), self.amount.get_text(), self.unit.get_text())

    def __init__(self, driver):
        super().__init__(driver)
        self.name = TextFieldElement(self.driver, NewRecipePageLocators.NAME_TEXT_FIELD)
        self.time = TextFieldElement(self.driver, NewRecipePageLocators.TIME_TEXT_FIELD)
        self.difficulty = TextFieldElement(self.driver, NewRecipePageLocators.DIFFICULTY_TEXT_FIELD)
        self.source = TextFieldElement(self.driver, NewRecipePageLocators.SOURCE_TEXT_FIELD)
        self.preparation = TextFieldElement(self.driver, NewRecipePageLocators.PREPARATION_TEXT_FIELD)

    @property
    def url(self):
        return self._url + '/new'

    @property
    def title(self):
        return "New Recipe - Cookbook"

    @property
    def ingredients(self):
        rows = len(self.driver.find_elements(*NewRecipePageLocators.INGREDIENT_ROW)) - 1
        ingredients = []
        for i in range(rows):
            ingredients.append(self.IngredientRow(self.driver, i))
        return ingredients

    @property
    def add_ingredient_button(self):
        return self.driver.find_element(*NewRecipePageLocators.ADD_INGREDIENT_BUTTON)

    @property
    def remove_ingredient_button(self):
        return self.driver.find_element(*NewRecipePageLocators.REMOVE_INGREDIENT_BUTTON)

    @property
    def confirm_button(self):
        return self.driver.find_element(*NewRecipePageLocators.CONFIRM_BUTTON)

    def submit(self):
        self.confirm_button.click()

    def add_ingredient(self):
        self.add_ingredient_button.click()

    def remove_ingredient(self):
        self.remove_ingredient_button.click()


class EditRecipePage(BasePageUrlRegex, NewRecipePage):

    @property
    def url_regex(self):
        return self._url + '/edit/(?P<id>\d+)'

    @property
    def title(self):
        return "Edit Recipe - Cookbook"

    # def is_url_correct(self):
    #     return super(BasePageUrlRegex).is_url_correct()  # should not be needed based on C3 MRO algorithm


class EditWaitingRecipePage(EditRecipePage):

    @property
    def url_regex(self):
        return self._url + '/waiting/(?P<id>\d+)/edit'

    @property
    def title(self):
        return "Edit Waiting Recipe - Cookbook"


class ErrorPage(BasePage):

    @property
    def message(self):
        return self.driver.find_element(*ErrorPageLocators.ERROR_MESSAGE).text
