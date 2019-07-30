from selenium.webdriver.common.by import By


class BasePageLocators:
    """Base class to initialize the base page locators that will be called from all locators"""

    # NAVIGATION BAR
    HOME_BUTTON = (By.CLASS_NAME, 'navbar-brand')
    ADD_RECIPE_BUTTON = (By.XPATH, '//*[@id="navbarTogglerBasic"]/ul/li[1]/a')
    LOGIN_BUTTON = (By.XPATH, '//*[@id="navbarTogglerBasic"]/ul/li[2]/a')

    # LOGGED IN USER NAVIGATION BAR
    USER_MENU_DROPDOWN = (By.ID, 'navbarDropdown')
    WAITING_RECIPES_BUTTON = (By.XPATH, '//*[@id="navbarTogglerBasic"]/ul/li[2]/div/a[1]')
    LOGOUT_BUTTON = (By.XPATH, '//*[@id="navbarTogglerBasic"]/ul/li[2]/div/a[2]')


class HomePageLocators:
    RECIPES_LIST = (By.TAG_NAME, 'tbody')
    RECIPE_ROW = (By.TAG_NAME, 'tr')


class LoginPageLocators:
    USERNAME_FIELD = (By.ID, 'username')
    PASSWORD_FIELD = (By.ID, 'password')
    REMEMBER_ME_CHECKBOX = (By.ID, 'remember_me')
    SUBMIT_BUTTON = (By.ID, 'submit')
    NEW_USER_BUTTON = (By.CSS_SELECTOR, 'a:contains("New user?")')
    FORGOTTEN_PASSWORD_BUTTON = (By.CSS_SELECTOR, 'a:contains("Forgotten password?")')


class RecipePageLocators:
    TITLE_HEADER = (By.TAG_NAME, 'h2')
    AUTHOR_NAME_PTAG = (By.CSS_SELECTOR, '.author > p')
    EDIT_LINK = (By.CSS_SELECTOR, 'a:contains("Edit")')
    TIME_PTAG = (By.XPATH, '/html/body/div[2]/div[2]/div[1]/p')
    DIFFICULTY_STAR = (By.CSS_SELECTOR, '.fas.fa-star')
    INGREDIENTS_LIST = (By.TAG_NAME, 'tbody')
    INGREDIENT_ROW = (By.TAG_NAME, 'tr')
    PREPARATION_PTAG = (By.XPATH, '/html/body/div[2]/div[3]/div[2]/p')
    SOURCE_LINK = (By.CSS_SELECTOR, 'a:contains("source")')
