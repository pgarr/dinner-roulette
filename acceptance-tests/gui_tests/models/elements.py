class TextFieldElement:
    """Text field class that is used to define text fields in Page classes"""

    def __init__(self, driver, locator):
        self.driver = driver
        self.locator = locator

    def set_text(self, value):
        """Sets the text to the value supplied"""
        element = self.driver.find_element(*self.locator)
        element.clear()
        element.send_keys(value)

    def get_text(self):
        """Gets the text in the field"""
        return self.driver.find_element(*self.locator).get_attribute("value")
