# Imports
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pytest
import time
import unittest


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8000/admin")

        # Input elements
        self.username_input = self.driver.find_element_by_xpath(
            "//input[@id='id_username']")
        self.password_input = self.driver.find_element_by_xpath(
            "//input[@id='id_password']")

    def tearDown(self):
        self.driver.quit()

    # Helper functions
    def clearInputs(self):
        self.username_input.clear()
        self.password_input.clear()

    # # 1 Test access to login page
    def test_access(self):
        driver = self.driver
        assert "Log in | Django site admin" in driver.title

    # # 2 Test login
    # # 2.1 Test invalid username
    def test_invalid_username(self):
        self.clearInputs()
        self.username_input.send_keys("invalidusername")
        self.password_input.send_keys("123456AB")
        self.password_input.send_keys(Keys.RETURN)
        assert None != self.driver.find_element_by_xpath(
            "//div[@id='content']/p[@class='errornote']")

    # # 2.2 Test invalid password
    def test_invalid_password(self):
        self.username_input.send_keys("TeamNotCircle")
        self.password_input.send_keys("invalidpassword")
        self.password_input.send_keys(Keys.RETURN)
        assert None != self.driver.find_element_by_xpath(
            "//div[@id='content']/p[@class='errornote']")

    # 2.3 Test valid username and password
    def test_valid_username_password(self):
        self.username_input.send_keys("TeamNotCircle")
        self.password_input.send_keys("123456AB")
        self.password_input.send_keys(Keys.RETURN)
        current_url = self.driver.current_url
        assert current_url == 'http://localhost:8000/admin/'
