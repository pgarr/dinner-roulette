from selenium.webdriver.support.wait import WebDriverWait

import config


class WrongPageLoadedError(Exception):
    def __init__(self, expected=None, actual=None):
        message = "Wrong page loaded."
        if expected:
            message += " Expected: %s. " % expected
        if actual:
            message += " Actual: %s. " % actual
        super().__init__(message)


def wait_page_changes(current_page, expected_page=None):
    wait = WebDriverWait(current_page.driver, config.MAX_LOADING_TIME)
    page_loaded = wait.until_not(lambda driver: current_page.is_title_correct())  # throws TimeoutException
    if expected_page and not expected_page.is_title_correct():
        raise WrongPageLoadedError()
    else:
        return expected_page
