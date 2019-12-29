# Imports
import django
from django.test import TestCase, Client
from django.test.utils import setup_test_environment
from django.contrib.auth.models import User
from django.urls import reverse

import pytest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from todo.models import TodoItem
from todo.views import todo_view, add_todo, delete_todo, archive_todo, team_contributions_view

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
class TestTodoPageSelenium(TestCase):
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

    # # # FOR SPRINT 1
    # # 5 Test archive todo
    # def test_archive_todo_selenium(self):
    #     content = str(uuid.uuid4())
    #     self.create_todo_selenium(new_content=content)
    #     time.sleep(1)
    #     archive_btn = self.driver.find_element_by_xpath(
    #         "//form[@name='{}']/input[@name='archive_btn']".format(content))
    #     archive_btn.click()
    #     time.sleep(1)
    #     archive_btn_disabled = self.driver.find_element_by_xpath(
    #         "//form[@name='{}']/input[@name='archive_btn']".format(content))
    #     assert False == archive_btn_disabled.is_enabled()


# BACKEND TEST
@pytest.mark.django_db
class TestTodoPageBackend(TestCase):
    def setUp(self):
        print('Setup')
        self.user1 = User.objects.create_user(username=valid_username,
                                              password=valid_password)
        self.user2 = User.objects.create_user(username='user2',
                                              password='valid_password')

    def tearDown(self):
        print('Tear down')

    # Helper functions
    def create_todo_backend(self, todo_content, user):
        new_todo = TodoItem.objects.create(content=todo_content, user=user)
        return new_todo

    def get_first_or_create_todo_backend(self):
        if (TodoItem.objects.count()) < 1:
            self.create_todo_backend('This is a new todo!', self.user1)
        all_todo = TodoItem.objects.all()
        return all_todo[0]

    # 1 Test add empty todo
    def test_empty_todo_backend(self):
        new_todo = self.create_todo_backend('', user=self.user1)
        assert True == TodoItem.objects.filter(pk=new_todo.pk).exists()

    # 2 Test add valid todo
    def test_valid_todo_backend(self):
        new_todo = self.create_todo_backend('This is a new todo!',
                                            user=self.user1)
        assert True == TodoItem.objects.filter(pk=new_todo.pk).exists()

    # 3 Test delete todo
    def test_delete_todo_backend(self):
        to_be_deleted = self.get_first_or_create_todo_backend()
        to_be_deleted.deleted = True
        to_be_deleted.save()
        assert True == TodoItem.objects.get(pk=to_be_deleted.pk).deleted

    # # # FOR SPRINT 1
    # # 4 Test archive todo
    # def test_archive_todo_backend(self):
    #     to_be_archived = self.get_first_or_create_todo_backend()
    #     to_be_archived.archive = True
    #     to_be_archived.save()
    #     assert True == TodoItem.objects.get(pk=to_be_archived.pk).archive

    # 5 Test filter todo by user
    def test_filter_todo_by_user(self):
        user1_todo = self.create_todo_backend(todo_content=uuid.uuid4(),
                                              user=self.user1)
        user2_todo = self.create_todo_backend(todo_content=uuid.uuid4(),
                                              user=self.user2)
        filtered_todo = TodoItem.objects.filter(user=self.user1)
        assert user1_todo in filtered_todo
        assert user2_todo not in filtered_todo

    # 6 Test todo is archived
    def test_todo_is_archived(self):
        new_todo = self.create_todo_backend('This is a new todo!',
                                            user=self.user1)
        assert True == new_todo.archive

    # 7 Test todo has created timestamp
    def test_todo_created_timestamp(self):
        new_todo = self.create_todo_backend('This is a new todo!',
                                            user=self.user1)
        assert None is not new_todo.created_at


# VIEW TEST
@pytest.mark.django_db()
class TestTodoPageView(TestCase):
    def setUp(self):
        print('Setup')
        self.unauth_client = Client()
        self.auth_client = Client()
        self.user = User.objects.create_user(username=valid_username,
                                             password=valid_password)
        self.auth_client.login(username=valid_username,
                               password=valid_password)

    def tearDown(self):
        print('Tear down')

    # 1 Test logged out user access to todo view
    def test_todo_view_unauthorized(self):
        res = self.unauth_client.get(reverse('todo_view', ))
        assert 302 == res.status_code

    # 2 Test logged in user access to todo view
    def test_todo_view_authorized(self):

        res = self.auth_client.get(reverse('todo_view'),
                                   {'user': self.auth_client})
        print(self.auth_client.login)
        assert 200 == res.status_code

    # 3 Test logged out user access to add todo view
    def test_add_todo_view_unauthorized(self):
        res = self.unauth_client.post(reverse('add_todo_view'), {
            'content': 'New Todo!!!',
            'user': self.unauth_client
        })
        assert (302 == res.status_code) and (
            '/accounts/login/?next=/addTodo/' == res.url)

    # 4 Test logged in user access to add todo view
    def test_add_todo_view_authorized(self):
        res = self.auth_client.post(reverse('add_todo_view'), {
            'content': 'New Todo!!!',
            'user': self.auth_client
        })
        assert (302 == res.status_code) and ('/todo/' == res.url)

    # 5 Test logged out user access to delete todo view
    def test_delete_todo_view_unauthorized(self):
        new_todo = TodoItem.objects.create(content=todo_content,
                                           user=self.user)
        res = self.unauth_client.post(
            reverse('delete_todo_view', kwargs={'todo_id': new_todo.pk}))
        print(res)
        assert (302 == res.status_code) and (
            '/accounts/login/?next=/deleteTodo/{}/'.format(
                new_todo.pk) == res.url)

    # 6 Test logged in user access to delete todo view
    def test_delete_todo_view_authorized(self):
        new_todo = TodoItem.objects.create(content=todo_content,
                                           user=self.user)
        res = self.auth_client.post(
            reverse('delete_todo_view', kwargs={'todo_id': new_todo.pk}))
        print(res)
        assert (302 == res.status_code) and ('/todo/' == res.url)

    # 7 Test logged out user access to archive todo view
    def test_archive_todo_view_unauthorized(self):
        new_todo = TodoItem.objects.create(content=todo_content,
                                           user=self.user)
        res = self.unauth_client.post(
            reverse('archive_todo_view', kwargs={'todo_id': new_todo.pk}))
        print(res)
        assert (302 == res.status_code) and (
            '/accounts/login/?next=/archiveTodo/{}/'.format(
                new_todo.pk) == res.url)

    # 8 Test logged in user access to archive todo view
    def test_archive_todo_view_authorized(self):
        new_todo = TodoItem.objects.create(content=todo_content,
                                           user=self.user)
        res = self.auth_client.post(
            reverse('archive_todo_view', kwargs={'todo_id': new_todo.pk}))
        print(res)
        assert (302 == res.status_code) and ('/todo/' == res.url)
