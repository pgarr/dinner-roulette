from selenium.webdriver.support.wait import WebDriverWait

from config import MAX_LOADING_TIME
from gui_tests.models.pages import BasePage


class WrongPageLoadedError(Exception):
    def __init__(self, expected=None, actual=None):
        message = "Wrong page loaded."
        if expected:
            message += " Expected: %s. " % expected
        if actual:
            message += " Actual: %s. " % actual
        super().__init__(message)


def wait_page_changes(current_page: BasePage, expected_page: BasePage = None):
    wait = WebDriverWait(current_page.driver, MAX_LOADING_TIME)
    page_loaded = wait.until_not(lambda driver: current_page.is_title_correct())  # throws TimeoutException
    if expected_page and not expected_page.is_title_correct():
        raise WrongPageLoadedError()
    else:
        return expected_page
