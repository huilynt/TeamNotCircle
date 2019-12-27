# Imports
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from todo.models import TodoItem
import pytest
import time
import unittest
import uuid
from django.contrib.auth.models import User

# Test values/variables
todo_content = 'This is a new Todo!!'
valid_username = 'TeamNotCircle'
valid_password = '123456Ab'


# SELENIUM TEST
@pytest.mark.django_db
class TestTodoPageSelenium(unittest.TestCase):
    def setUp(self):
        print('Setup')

        self.driver = webdriver.Chrome()
        self.login()

        # Elements
        self.todo_input = self.driver.find_element_by_xpath(
            "//input[@id='todo_input']")
        self.submit_btn = self.driver.find_element_by_xpath(
            "//input[@id='submit_btn']")

    def tearDown(self):
        print('Tear down')
        self.driver.quit()

    # Helper functions
    def clear_inputs(self):
        self.todo_input.clear()

    def create_todo_selenium(self, new_content):
        self.todo_input.send_keys(new_content)
        self.submit_btn.click()

    def login(self):
        self.driver.get("http://localhost:8000/accounts/login")
        username_input = self.driver.find_element_by_xpath(
            "//input[@id='id_username']")
        password_input = self.driver.find_element_by_xpath(
            "//input[@id='id_password']")
        username_input.send_keys(valid_username)
        password_input.send_keys(valid_password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(1)

    # SELENIUM TEST
    # 1 Test access to todo page
    def test_access(self):
        assert "Todo Page" in self.driver.title

    # 2 Test add empty todo
    def test_empty_todo_selenium(self):
        self.clear_inputs()
        original_page_source = self.driver.page_source
        self.submit_btn.click()
        assert original_page_source == self.driver.page_source

    # 3 Test add valid todo
    def test_valid_todo_selenium(self):
        self.create_todo_selenium(todo_content)
        assert todo_content in self.driver.page_source

    # 4 Test delete todo
    def test_delete_todo_selenium(self):
        content = str(uuid.uuid4())
        self.create_todo_selenium(new_content=content)
        time.sleep(1)
        delete_btn = self.driver.find_element_by_xpath(
            "//form[@name='{}']/input[@name='delete_btn']".format(content))
        delete_btn.click()
        time.sleep(1)
        assert content not in self.driver.page_source

    # 5 Test archive todo
    def test_archive_todo_selenium(self):
        content = str(uuid.uuid4())
        self.create_todo_selenium(new_content=content)
        time.sleep(1)
        archive_btn = self.driver.find_element_by_xpath(
            "//form[@name='{}']/input[@name='archive_btn']".format(content))
        archive_btn.click()
        assert content not in self.driver.page_source


# BACKEND TEST
@pytest.mark.django_db
class TestTodoPageBackend(unittest.TestCase):
    def setUp(self):
        print('Setup')
        self.user = User.objects.create_user(username=valid_username,
                                             password=valid_password)

    def tearDown(self):
        print('Tear down')

    # Helper functions
    def create_todo_backend(self, todo_content):
        new_todo = TodoItem.objects.create(content=todo_content,
                                           user=self.user)
        return new_todo

    def get_first_or_create_todo_backend(self):
        if (TodoItem.objects.count()) < 1:
            self.create_todo_backend('This is a new todo!')
        all_todo = TodoItem.objects.all()
        return all_todo[0]

    # 1 Test add empty todo
    def test_empty_todo_backend(self):
        new_todo = self.create_todo_backend('')
        assert True == TodoItem.objects.filter(pk=new_todo.pk).exists()

    # 2 Test add valid todo
    def test_valid_todo_backend(self):
        new_todo = self.create_todo_backend('This is a new todo!')
        assert True == TodoItem.objects.filter(pk=new_todo.pk).exists()

    # 3 Test delete todo
    def test_delete_todo_backend(self):
        to_be_deleted = self.get_first_or_create_todo_backend()
        to_be_deleted.delete()
        assert False == TodoItem.objects.filter(pk=to_be_deleted.pk).exists()

    # 4 Test archive todo
    def test_archive_todo_backend(self):
        to_be_archived = self.get_first_or_create_todo_backend()
        to_be_archived.archive = True
        to_be_archived.save()
        assert True == TodoItem.objects.get(pk=to_be_archived.pk).archive
