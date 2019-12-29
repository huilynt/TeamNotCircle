# Imports
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import django
from django.test import TestCase, Client
from django.test.utils import setup_test_environment
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User

import pytest
import time
import uuid
import unittest

# Test values/variables
existing_username = 'TeamNotCircle'
valid_password = 'testingPassWord11'
common_password = '123456Ab'
invalid_username = 'InvalidUsername'
empty_password = ''


# SELENIUM TEST
@pytest.mark.django_db
class TestSignupSelenium(TestCase):
    def setUp(self):
        print('Setup')
        User.objects.create_user(username=invalid_username,
                                 password=valid_password)
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8000/accounts/signup/")
        # Elements
        self.username_input = self.driver.find_element_by_xpath(
            "//input[@id='id_username']")
        self.password_input = self.driver.find_element_by_xpath(
            "//input[@id='id_password']")
        self.password2_input = self.driver.find_element_by_xpath(
            "//input[@id='id_password2']")

    def tearDown(self):
        print('Tear down')
        self.driver.quit()

    # Helper functions
    def clear_inputs(self):
        self.username_input.clear()
        self.password_input.clear()
        self.password2_input.clear()

    # 1 Test access
    def test_access_selenium(self):
        assert "Sign up | User" in self.driver.title

    # 2 Test empty fields
    def test_signup_empty_selenium(self):
        original_page_source = self.driver.page_source
        self.username_input.send_keys(Keys.RETURN)
        assert original_page_source == self.driver.page_source

    # 3 Test empty username
    def test_empty_username_selenium(self):
        original_page_source = self.driver.page_source
        self.clear_inputs()
        self.username_input.send_keys('')
        self.password_input.send_keys(valid_password)
        self.password2_input.send_keys(valid_password)
        self.password2_input.send_keys(Keys.RETURN)
        assert original_page_source == self.driver.page_source

    # 4 Test existing username
    def test_existing_username_selenium(self):
        self.username_input.send_keys(existing_username)
        self.password_input.send_keys(valid_password)
        self.password2_input.send_keys(valid_password)
        self.password2_input.send_keys(Keys.RETURN)
        assert (None != self.driver.find_element_by_xpath(
            "//div[contains(@class,'errornote')]")) and (
                "A user with that username already exists." in
                self.driver.page_source)

    # 5 Test empty password
    def test_empty_password_selenium(self):
        original_page_source = self.driver.page_source
        self.username_input.send_keys(str(uuid.uuid4()))
        self.password_input.send_keys(empty_password)
        self.password2_input.send_keys(empty_password)
        self.password2_input.send_keys(Keys.RETURN)
        assert original_page_source == self.driver.page_source

    # 6 Test common username and password
    def test_common_password_selenium(self):
        self.username_input.send_keys(str(uuid.uuid4()))
        self.password_input.send_keys(common_password)
        self.password2_input.send_keys(common_password)
        self.password2_input.send_keys(Keys.RETURN)
        assert (None != self.driver.find_element_by_xpath(
            "//div[contains(@class,'errornote')]")) and (
                "This password is too common." in self.driver.page_source)

    # 7 Test mismatched password
    def test_mismatch_password_selenium(self):
        self.username_input.send_keys(str(uuid.uuid4()))
        self.password_input.send_keys(valid_password)
        self.password2_input.send_keys('mismatch')
        self.password2_input.send_keys(Keys.RETURN)
        assert (None != self.driver.find_element_by_xpath(
            "//div[contains(@class,'errornote')]")) and (
                "The two password fields didn't match." in
                self.driver.page_source)

    # 8 Test all valid fields
    def test_valid_username_password_selenium(self):
        self.username_input.send_keys(str(uuid.uuid4()))
        self.password_input.send_keys(valid_password)
        self.password2_input.send_keys(valid_password)
        self.password2_input.send_keys(Keys.RETURN)
        assert 'http://localhost:8000/todo/' == self.driver.current_url


# VIEWS TEST
@pytest.mark.django_db
class TestSignupView(TestCase):
    def setUp(self):
        print('Setup')
        self.auth_client = Client()
        self.user = User.objects.create_user(username=existing_username,
                                             password=valid_password)

    def tearDown(self):
        print('Tear down')

    # 1 Test access
    def test_access_view(self):
        res = self.auth_client.get(reverse('signup'))
        print(res)
        assert 200 == res.status_code

    # 2 Test empty username
    def test_empty_username_view(self):
        res = self.auth_client.post(
            reverse('signup'), {
                'username': '',
                'password1': valid_password,
                'password2': valid_password
            })
        print(res)
        assert 200 == res.status_code

    # 3 Test existing username
    def test_existing_username_view(self):
        res = self.auth_client.post(
            reverse('signup'), {
                'username': existing_username,
                'password1': valid_password,
                'password2': 'valid_password'
            })
        print(res)
        assert 200 == res.status_code

    # 4 Test mismatched password
    def test_mismatch_password_view(self):
        res = self.auth_client.post(reverse('signup'), {
            'username': '',
            'password1': valid_password,
            'password2': 'mismatch'
        })
        print(res)
        assert 200 == res.status_code

    # 5 Test all valid fields
    def test_all_valid_view(self):
        res = self.auth_client.post(
            reverse('signup'), {
                'username': str(uuid.uuid4()),
                'password1': valid_password,
                'password2': valid_password
            })
        print(res)
        assert (302 == res.status_code) and ('/todo/' == res.url)

    # 6 Test get sign up view
    def test_get_view(self):
        res = self.auth_client.get(reverse('signup'))
        print(res)
        assert 200 == res.status_code
