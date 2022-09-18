

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver.v2 as uc





class Scraper():
    SCROLL_PAUSE_TIME = 1
    SCROLL_GAP = 10
    def __init__(self) -> None:
        self.driver = uc.Chrome()
    def scrape(self, url):
        self.driver.get(url)
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        body = self.driver.find_element(By.XPATH, '/html/body')
        while True:
            # # Scroll down to bottom
            position_scroll_top =int(self.driver.execute_script("return document.documentElement.scrollTop || document.body.scrollTop ;"))
            self.driver.execute_script(f"window.scrollTo(0, {(position_scroll_top+self.SCROLL_GAP)});")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # body.send_keys(Keys.PAGE_DOWN)
            # Wait to load page
            time.sleep(self.SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
        questions_body = self.driver.find_elements(By.XPATH, '//div[starts-with(@class, "Question_body__")]')
        a = 0
        # players = driver.find_elements(By.XPATH, '//td[@class="name"]')