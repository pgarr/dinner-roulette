class TextFieldElement:
    """Text field class that is used to define text fields in Page classes"""

    def __init__(self, driver, locator):
        self.driver = driver
        self.obj = self.driver.find_element(*locator)

    def __set__(self, value):
        """Sets the text to the value supplied"""
        self.obj.send_keys(value)

    def __get__(self):
        """Gets the text in the field"""
        return self.obj.text
