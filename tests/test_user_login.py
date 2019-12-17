# Imports
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pytest

# Setup
driver = webdriver.Chrome()

# 1 Test access to login page


def test_access():
    driver.get('http://localhost:8000/admin')
    assert "Log in | Django site admin" in driver.title

#
