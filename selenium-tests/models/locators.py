from selenium.webdriver.common.by import By


class BasePageLocators:
    """Base class to initialize the base page locators that will be called from all locators"""

    # NAVIGATION BAR
    HOME_BUTTON = (By.CLASS_NAME, 'navbar-brand')
    ADD_RECIPE_BUTTON = (By.XPATH, '//*[@id="navbarTogglerBasic"]/ul/li[1]/a')
    LOGIN_BUTTON = (By.XPATH, '//*[@id="navbarTogglerBasic"]/ul/li[2]/a')

    # LOGGED IN USER NAVIGATION BAR
    USER_MENU_DROPDOWN = (By.ID, 'navbarDropdown')
    MY_RECIPES_BUTTON = (By.XPATH, "//a[contains(text(), 'My recipes')]")
    WAITING_RECIPES_BUTTON = (By.XPATH, "//a[contains(text(), 'Pending recipes')]")
    LOGOUT_BUTTON = (By.XPATH, "//a[contains(text(), 'Logout')]")


class HomePageLocators:
    RECIPE_ROW = (By.CSS_SELECTOR, 'table > tbody > tr')
    ROW_CELLS = (By.TAG_NAME, 'td')  # inside RECIPE_ROW
    DIFFICULTY_STAR = (By.CSS_SELECTOR, '.fas.fa-star')  # in ROW_CELLS
    RECIPE_LINK = (By.TAG_NAME, 'a')  # inside ROW_CELLS
    RECIPE_INDEX_CELL = (By.TAG_NAME, 'th')  # inside ROW_CELLS


class LoginPageLocators:
    USERNAME_FIELD = (By.ID, 'username')
    PASSWORD_FIELD = (By.ID, 'password')
    REMEMBER_ME_CHECKBOX = (By.ID, 'remember_me')
    SUBMIT_BUTTON = (By.ID, 'submit')
    NEW_USER_BUTTON = (By.XPATH, "//a[contains(text(), 'New user?')]")
    FORGOTTEN_PASSWORD_BUTTON = (By.XPATH, "//a[contains(text(), 'Forgotten password?')]")


class RecipePageLocators:
    TITLE_HEADER = (By.TAG_NAME, 'h2')
    AUTHOR_NAME_PTAG = (By.CSS_SELECTOR, '.author > p')
    EDIT_LINK = (By.CSS_SELECTOR, 'a:contains("Edit")')
    TIME_PTAG = (By.XPATH, '/html/body/div[2]/div[2]/div[1]/p')
    DIFFICULTY_STAR = (By.CSS_SELECTOR, '.fas.fa-star')
    INGREDIENT_ROW = (By.CSS_SELECTOR, 'table > tbody > tr')
    INGREDIENT_NAME = (By.TAG_NAME, 'th')  # inside INGREDIENT_ROW
    INGREDIENT_AMOUNT = (By.TAG_NAME, 'td')  # inside INGREDIENT_ROW
    PREPARATION_PTAG = (By.XPATH, '/html/body/div[2]/div[3]/div[2]/p')
    SOURCE_LINK = (By.XPATH, "//a[contains(text(), 'source')]")


class WaitingRecipePageLocators:
    ACCEPT_LINK = (By.XPATH, "//a[contains(text(), 'Accept')]")


class NewRecipePageLocators:
    SOURCE_TEXT_FIELD = (By.ID, 'link')
    DIFFICULTY_TEXT_FIELD = (By.ID, 'difficulty')
    TIME_TEXT_FIELD = (By.ID, 'time')
    NAME_TEXT_FIELD = (By.ID, 'title')
    ADD_INGREDIENT_BUTTON = (By.ID, 'add_ingredient')
    REMOVE_INGREDIENT_BUTTON = (By.ID, 'remove_ingredient')
    CONFIRM_BUTTON = (By.ID, 'submit')
    PREPARATION_TEXT_FIELD = (By.ID, 'preparation')
    INGREDIENT_ROW = (By.CSS_SELECTOR, '.ingredients-top-margin')
    INGREDIENT_NAME_FIELD = (By.ID, 'ingredients-%d-title')
    INGREDIENT_AMOUNT_FIELD = (By.ID, 'ingredients-%d-amount')
    INGREDIENT_UNIT_FIELD = (By.ID, 'ingredients-%d-unit')


class ErrorPageLocators:
    ERROR_MESSAGE = (By.CLASS_NAME, 'error-msg')
