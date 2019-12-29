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


@pytest.mark.django_db
class TestTeamContributionsView(TestCase):
    def test_access_view(self):
        res = Client().get(reverse('contributions_view'))
        assert 200 == res.status_code
