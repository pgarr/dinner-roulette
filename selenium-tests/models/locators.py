from selenium.webdriver.common.by import By


class BasePageLocators:
    """Base class to initialize the base page locators that will be called from all locators"""

    # NAVIGATION BAR
    HOME_BUTTON = (By.XPATH, '/html/body/div[1]/nav/a')
    ADD_RECIPE_BUTTON = (By.XPATH, '//*[@id="navbarTogglerBasic"]/ul/li[1]/a')
    LOGIN_BUTTON = (By.XPATH, '//*[@id="navbarTogglerBasic"]/ul/li[2]/a')

    # LOGGED IN USER NAVIGATION BAR
    USER_MENU_DROPDOWN = (By.ID, 'navbarDropdown')
    WAITING_RECIPES_BUTTON = (By.XPATH, '//*[@id="navbarTogglerBasic"]/ul/li[2]/div/a[1]')
    LOGOUT_BUTTON = (By.XPATH, '//*[@id="navbarTogglerBasic"]/ul/li[2]/div/a[2]')


class HomePageLocators(BasePageLocators):
    pass


class LoginPageLocators(BasePageLocators):
    pass