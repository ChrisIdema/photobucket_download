#!/usr/bin/python3


from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from login import *

import time

driver = webdriver.Chrome(r'C:\chromedriver.exe')


def turn_down():
	try:
		turn_down_btn = driver.find_element_by_xpath(r'//*[@id="postpone"]')
		turn_down_btn.click()
		print("Turned down stupid offer")
	except Exception:
		print("Stupid offer not found")

def login():	
	driver.get('https://photobucket.com/login')

	email_input = driver.find_element_by_xpath(r'//*[@id="username"]')
	email_input.send_keys(EMAIL)

	psd_input = driver.find_element_by_xpath(r'//*[@id="password"]')
	psd_input.send_keys(PASSWORD)

	login_btn = driver.find_element_by_xpath(r'//*[@id="loginPageForm"]/input[2]')
	login_btn.click()
	
	driver.get('https://photobucket.com')
	
	turn_down()
	
#only works when cursor is in window	
def download():
	
	starting_url = driver.current_url
	
	while True:
		download_btn = driver.find_element_by_id('download_button')
		download_btn.click()
		
		#time.sleep(5)		
		
		next_btn = driver.find_element_by_xpath(r'//*[@id="next"]/div/span')
		#next_btn = driver.find_element_by_id('btnnext')
		next_btn.click()
		
		#time.sleep(5)
		current_url = driver.current_url
		if current_url == starting_url:
			print("Finished downloading this album")
			break;

		

def album_list_get(url):
	album_list = []
	album_list.append(url)
	driver.get(url)
	turn_down()
	time.sleep(30)#delay because the list loads after the page has loaded
	i = 0
	while True:
		try:
			albumi_xpath = r'//*[@id="albumList"]/div/div[' + str(i + 1)  + r']/div[2]/h2/a' 
			album_element = driver.find_element_by_xpath(albumi_xpath)
			print("Found album: ", album_element.text)
			album_link = album_element.get_attribute('href')
			album_list.append(album_link)
			i += 1
		except Exception as e:
			print(e.args)
			print("Done searching list")
			break
			
	return album_list
	
def albums_download(album_list):
	
	for album_url in album_list:	
		driver.get(album_url)
		album_element = driver.find_element_by_xpath(r"//a[@class='thumbnailLink media']")
		album_first_image = album_element.get_attribute('href')
		driver.get(album_first_image)
		download()


		
def main():
	login()
	
	#stats_get() //*[@id="userMenu"]/ul/li[1]/a
	
	album_element = driver.find_element_by_xpath(r"//*[@id='libraryMenu']/a")
	root_album_url = album_element.get_attribute('href')
		
	album_list = album_list_get(root_album_url)
	
	print("Album url list:",album_list)
	
	albums_download(album_list)
	
if __name__ == "__main__":
	main()