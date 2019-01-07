import unittest
from selenium import webdriver
import time

class MyTestCase(unittest.TestCase):
    def setUpClass(self):
        self.browser = webdriver.Chrome360()

    def tearDown(self):
        self.browser.quit()

    def test_home_page(self):
        self.browser.get('http://127.0.0.1:5000/')
        self.assertIn('首页', self.browser.title)

    def test_about_like(self):
        self.browser.get('http://127.0.0.1:5000/about')
        a = int(self.browser.find_element_by_id('liked').text)
        self.browser.find_element_by_xpath("//div[@class='btn btn-danger btn-large btn-block btn-like-add']").click()
        time.sleep(2)
        self.assertEqual(int(self.browser.find_element_by_id('liked').text), a+1)


if __name__ == '__main__':
    unittest.main()
