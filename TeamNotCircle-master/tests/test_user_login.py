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

# Test values/variables
valid_username = 'TeamNotCircle'
valid_password = '123456Ab'
invalid_username = 'InvalidUsername'
invalid_password = 'InvalidPassword'


# SELENIUM TEST
@pytest.mark.django_db
class TestLoginSelenium(unittest.TestCase):
    def setUp(self):
        print('Setup')
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8000/accounts/login/")
        # Elements
        self.username_input = self.driver.find_element_by_xpath(
            "//input[@id='id_username']")
        self.password_input = self.driver.find_element_by_xpath(
            "//input[@id='id_password']")

    def tearDown(self):
        print('Tear down')
        self.driver.quit()

    # Helper functions
    def clear_inputs(self):
        self.username_input.clear()
        self.password_input.clear()

    # 1 Test access to login page
    def test_access(self):
        assert "Log in | User" in self.driver.title

    # 2 Test empty login
    def test_login_empty_selenium(self):
        original_page_source = self.driver.page_source
        self.username_input.send_keys(Keys.RETURN)
        assert original_page_source == self.driver.page_source

    # 3 Test invalid username
    def test_invalid_username_selenium(self):
        self.clear_inputs()
        self.username_input.send_keys(invalid_username)
        self.password_input.send_keys(valid_password)
        self.password_input.send_keys(Keys.RETURN)
        assert None != self.driver.find_element_by_xpath(
            "//div[contains(@class,'errornote')]")

    # 4 Test invalid password
    def test_invalid_password_selenium(self):
        self.username_input.send_keys(valid_username)
        self.password_input.send_keys(invalid_password)
        self.password_input.send_keys(Keys.RETURN)
        assert None != self.driver.find_element_by_xpath(
            "//div[contains(@class,'errornote')]")

    # 5 Test valid username and password
    def test_valid_username_password_selenium(self):
        self.username_input.send_keys(valid_username)
        self.password_input.send_keys(valid_password)
        self.password_input.send_keys(Keys.RETURN)
        time.sleep(1)
        current_url = self.driver.current_url
        assert 'http://localhost:8000/todo/' == current_url


# BACKEND TEST
@pytest.mark.django_db
class TestLoginBackend(unittest.TestCase):
    def setUp(self):
        print('Setup')
        # Create user object
        userExists = User.objects.filter(username=valid_username).exists()
        if (not userExists):
            print('User {0} does not exist\nCreating user {0}'.format(
                valid_username))
            print('Creating new user')
            user = User.objects.create_user(username=valid_username,
                                            password=valid_password)
            user.is_staff = True
            user.save()
            print('New user {} created'.format(valid_username))

    def tearDown(self):
        print('Tear down')

    # 1 Test empty login
    def test_login_empty_backend(self):
        user = authenticate(username='', password='')
        assert None is user

    # 2 Test invalid username
    def test_invalid_username_backend(self):
        user = authenticate(username=invalid_username, password=valid_password)
        assert None is user

    # 3 Test invalid password
    def test_invalid_password_backend(self):
        user = authenticate(username=valid_username, password=invalid_password)
        assert None is user

    # 4 Test valid username and password
    def test_valid_username_password_backend(self):
        user = authenticate(username=valid_username, password=valid_password)
        assert None is not user
