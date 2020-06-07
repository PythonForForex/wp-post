#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

''' Auto post to WordPress using Selenium
this has not been tested with Gutenberg and will likely only 
work with the previous version of WordPress '''

class wp_post():
	def __init__(self, base_url, wp_login, wp_pass):
		self.base_url = base_url
		self.post_page = 'post-new.php'
		self.wp_login = wp_login
		self.wp_pass = wp_pass
		self.alt_text = None
		self.link_upload = None

	def login(self):
		''' wp login - Note: no error checking for incorrect user/passwd '''
		form_user_login = self.driver.find_element_by_id('user_login')
		form_user_pass = self.driver.find_element_by_id('user_pass')
		form_user_login.clear()
		form_user_pass.clear()
		form_user_login.send_keys(self.wp_login)
		form_user_pass.send_keys(self.wp_pass)
		form_user_login.submit()

	def post_contents(self, contents):
		''' overwrite this function for custom content posting '''
		self.driver.find_element_by_id('content-html').click()
		self.driver.find_element_by_id('content').send_keys(contents)

	def create_post(self, title=None, contents=None, excerpt=None, category=None, tags=None, ft_img=None):
		''' main function to create a new post '''
		self.driver = webdriver.Chrome()
		self.driver.get(self.base_url+self.post_page)
		if 'login.php' in self.driver.current_url:
			self.login()

		if title:
			self.driver.find_element_by_name('post_title').send_keys(title)
		
		if contents:
			self.post_contents(contents)

		if excerpt:
			self.driver.find_element_by_name('excerpt').send_keys(excerpt)

		if category:
			self.driver.find_element_by_link_text('All Categories').send_keys(Keys.ENTER)
			sleep(2)
			all_categories = self.driver.find_element_by_id('category-all')
			categories = all_categories.find_elements_by_class_name('popular-category')
			for item in categories:
				if item.text != '' and item.text in category:
					item.find_element_by_class_name('selectit').send_keys(Keys.SPACE)

		if tags:
			self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
			cloud = self.driver.find_element_by_id('link-post_tag')
			if cloud.get_attribute('aria-expanded') == 'false':
				cloud.send_keys(Keys.SPACE)
				sleep(2)
			link_tags = self.driver.find_elements_by_class_name('tag-cloud-link')

			#check if tags exist to avoid creating new unwanted wp pages
			for tag in link_tags:
				if tag.text in tags:
					tag.send_keys(Keys.ENTER)
					sleep(1)

		if ft_img:
			self.driver.find_element_by_link_text('Set featured image').send_keys(Keys.ENTER)
            #ToDO: Use JavaScript method to check ReadyState rather than use sleep
			sleep(5)
			self.upload_img(ft_img)
			#remove title for featured image and insert alt text if exists
			if self.alt_text:
				alt_text_box = self.driver.find_elements_by_id('attachment-details-alt-text')
				for item in alt_text_box:
					if item.is_displayed():
						item.send_keys(self.alt_text)
				title_box = self.driver.find_elements_by_id('attachment-details-title')
				for item in title_box:
					if item.is_displayed():
						item.clear()
				sleep(3)
			button = self.driver.find_elements_by_class_name('media-button')
            #ToDo: WP uses multiple modals to upload images. The below method will check for the active window
            #better method is to search for the active modal first by div ID.
			for item in button:
				if item.is_displayed():
					item.click()

	def upload_img(self, img):
		self.driver.find_element_by_xpath("//input[starts-with(@id,'html5_')]").send_keys(img)
		button = self.driver.find_element_by_class_name('media-button')
		while not button.is_enabled():
			sleep(1)
			button = self.driver.find_element_by_class_name('media-button')
		sleep(1)
		ready = self.driver.find_element_by_class_name('media-uploader-status')
		#redundant error checking as this function is prone to failure due to lengthy upload times
		for _ in range(10):
			if 'block' in ready.get_attribute('style'):
				sleep(2)
			else:
				return button