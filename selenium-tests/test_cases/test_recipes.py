from models.pages import HomePage
from base_test import BaseTest


class RecipesListTest(BaseTest):

    def test_show_list(self):
        home_page = HomePage(self.driver)
        self.driver.get(home_page.url)
        print(home_page.recipes)

