from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Test_Login_And_Register_Page(LiveServerTestCase):
 
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.close()
 
    # Can load login page and attempt to login with incorrect details?
    def test_incorrect_login(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/login")
        user = driver.find_element_by_name("username")
        user.clear()
        user.send_keys("wrong")
        password = driver.find_element_by_name("password")
        password.clear()
        password.send_keys("wrong")
        driver.find_element_by_name("submit").click()
        message = driver.find_element_by_name("error_message").text
        expected = "Username or password is incorrect. If you have forgotten your password please contact us"
        self.assertEqual(message, expected)

    # Can load login page and attempt to login with correct details?
    def test_correct_login(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/login")
        assert "LW Bespoke Tuition" in driver.title
        user = driver.find_element_by_name("username")
        user.clear()
        user.send_keys("boo2")
        password = driver.find_element_by_name("password")
        password.clear()
        password.send_keys("thistest1")
        driver.find_element_by_name("submit").click()
        driver.get("http://127.0.0.1:8000")
        username = driver.find_element_by_name("username").text
        expected = "Hello, boo2"
        self.assertEqual(username, expected)


'''
class Test_Login_And_Register(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.close()

    def test_correct_login(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/login")
        assert "LW Bespoke Tuition" in driver.title
        user = driver.find_element_by_name("username")
        user.clear()
        user.send_keys("boo2")
        password = driver.find_element_by_name("password")
        password.clear()
        password.send_keys("thistest1")
        driver.find_element_by_name("submit").click()
        driver.get("http://127.0.0.1:8000")
        username = driver.find_element_by_name("username").text
        expected = "Hello, boo2"
        self.assertEqual(username, expected)
'''
