# Imports
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import pytest
import time
import unittest


class TestLogin(unittest.TestCase):
    def setUp(self):
        print('Setup')
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8000/admin")

        self.valid_username = 'TeamNotCircle'
        self.valid_password = '123456Ab'
        self.invalid_username = 'InvalidUsername'
        self.invalid_password = 'InvalidPassword'

        # Elements
        self.username_input = self.driver.find_element_by_xpath(
            "//input[@id='id_username']")
        self.password_input = self.driver.find_element_by_xpath(
            "//input[@id='id_password']")

        # Create user object
        userExists = User.objects.filter(username=self.valid_username).exists()
        if (not userExists):
            print('Creating new user')
            user = User.objects.create_user(username=self.valid_username,
                                            password=self.valid_password)
            print('New user {} created'.format(self.valid_username), user)
        else:
            print('User {} exists'.format(self.valid_username))

    def tearDown(self):
        print('Tear down')
        self.driver.quit()

    # Helper functions
    def clearInputs(self):
        self.username_input.clear()
        self.password_input.clear()

    # SELENIUM TEST
    # 1 Test access to login page
    def test_access(self):
        assert "Log in | Django site admin" in self.driver.title

    # 2 Test empty login
    def test_login_empty_selenium(self):
        original_page_source = self.driver.page_source
        self.username_input.send_keys(Keys.RETURN)
        assert original_page_source == self.driver.page_source

    # 3 Test invalid username
    def test_invalid_username_selenium(self):
        self.clearInputs()
        self.username_input.send_keys(self.invalid_username)
        self.password_input.send_keys(self.valid_password)
        self.password_input.send_keys(Keys.RETURN)
        assert None != self.driver.find_element_by_xpath(
            "//div[@id='content']/p[@class='errornote']")

    # 4 Test invalid password
    def test_invalid_password_selenium(self):
        self.username_input.send_keys(self.valid_username)
        self.password_input.send_keys(self.invalid_password)
        self.password_input.send_keys(Keys.RETURN)
        assert None != self.driver.find_element_by_xpath(
            "//div[@id='content']/p[@class='errornote']")

    # 5 Test valid username and password
    def test_valid_username_password_selenium(self):
        self.username_input.send_keys(self.valid_username)
        self.password_input.send_keys(self.valid_password)
        self.password_input.send_keys(Keys.RETURN)
        current_url = self.driver.current_url
        assert 'http://localhost:8000/admin/' == current_url

    # BACKEND TEST
    # 1 Test empty login
    def test_login_empty_backend(self):
        user = authenticate(username='', password='')
        assert None is user

    # 2 Test invalid username
    def test_invalid_username_backend(self):
        user = authenticate(username=self.invalid_username,
                            password=self.valid_password)
        assert None is user

    # 3 Test invalid password
    def test_invalid_password_backend(self):
        user = authenticate(username=self.valid_username,
                            password=self.invalid_password)
        assert None is user

    # 4 Test valid username and password
    def test_valid_username_password_backend(self):
        user = authenticate(username=self.valid_username,
                            password=self.valid_password)
        assert None is not user
