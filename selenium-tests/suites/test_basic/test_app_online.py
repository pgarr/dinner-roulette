from unittest import TestCase

from selenium import webdriver


class BaseTest(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_online(self):
        self.driver.get('http://127.0.0.1:5000')
        # response = urllib2.urlopen('http://127.0.0.1:5000')
        # self.assertEqual(response.code, 200)

