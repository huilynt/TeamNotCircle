# Imports
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from todo.models import TodoItem
import pytest


#Login Details
valid_username = 'TeamNotCircle'
valid_password = '123456Ab'

#Input for todo
todo_content = 'Test Todo'

#Selenium Test Case
@pytest.mark.django_db
class TestHistoryPageSelenium(unittest.TestCase):

	def setUp(self):
		print('Setup')
		self.driver = webdriver.Chrome()
		self.login()

		 self.todo_input = self.driver.find_element_by_xpath(
            "//input[@id='todo_input']")
        self.submit_btn = self.driver.find_element_by_xpath(
            "//input[@id='submit_btn']")

    def tearDown(self):
        print('Tear down')
        self.driver.quit()

    def create_todo(self, new_content):
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


    #Test for access to todo page
    def test_todo_access(self):
    	assert "Todo Page" in self.driver.title

    #Test to archive newly created Todo item
    def test_archive_todo(self):
    	new_created_content = self.create_todo(todo_content)
    	input_id = new_created_content.input_id
    	archive_btn = self.driver.find_element_by_xpath("//form[@name='{}']/input[@name='archive_btn']".format(input_id))
    	archive_btn.click()

    #Test to check for archived item display
    def test_archived_history(self):
    	self.driver.get("http://localhost:8000/historyTodo")
    	assert todo_content in self.driver.page_source

    #Test to check for newly added item in history
    def test_added_in_history(self):
        #create new object
    	self.driver.get("http://localhost:8000/todo")
    	self.create_todo(todo_content)
    	#check in history that content has been added
    	self.driver.get("http://localhost:8000/historyTodo")
    	assert todo_content in self.driver.page_source

    #Test to check for deleted item in history
    def test_deleted_in_history(self):
        #create new object
    	self.driver.get("http://localhost:8000/todo")
    	new_created_content = self.create_todo(todo_content)
    	input_id = new_created_content.input_id
    	delete_btn = self.driver.find_element_by_xpath(
            "//form[@name='{}']/input[@name='delete_btn']".format(input_id))
    	delete_btn.click()
    	#check in history that content has been added
    	self.driver.get("http://localhost:8000/historyTodo")
    	assert todo_content in self.driver.page_source
        
