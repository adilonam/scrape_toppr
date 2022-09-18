

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver.v2 as uc
from string import ascii_lowercase as alc
from selenium.webdriver.common.action_chains import ActionChains
import re
from slugify import slugify

class Scraper():
    base_url = 'https://www.toppr.com/ask/content/cbse/class-'
    PAUSE_TIME = 1
    SCROLL_GAP = 10
    subjects = ['Economics', 'History', 'Biology', 'Civics', 'English', 'Geography', 'Elements of Book Keeping and Accountancy', 'Maths', 'General Knowledge', 'Physics', 'Chemistry', 'Elements of Business']
    data_structure = {
        'q': '',
        'qImage': '',
        'opA': '',
        'opB': '',
        'opC': '',
        'opD': '',
        'opE': '',
        'a': '',
         'e': '',
        'eImage': '',
        'pL': '',
        'topic': '',
        'subject': '',
        'difficulty': '',
        'class': ''
    }
    def __init__(self) -> None:
        self.driver = uc.Chrome()
        self.actions = ActionChains(self.driver)
    def start(self, classes):
        for class_name in classes:
            class_url  = self.base_url+str(class_name) + '/'
            for subject in self.subjects:
                subject_url = class_url + slugify(subject)
                self.driver.get(subject_url)
    def scrape(self, url, class_number,subject,topic, difficulty):
        self.driver.get(url)
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # # Scroll down to bottom
            position_scroll_top =int(self.driver.execute_script("return document.documentElement.scrollTop || document.body.scrollTop ;"))
            self.driver.execute_script(f"window.scrollTo(0, {(position_scroll_top+self.SCROLL_GAP)});")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # body.send_keys(Keys.PAGE_DOWN)
            # Wait to load page
            time.sleep(self.PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
        questions_body = self.driver.find_elements(By.XPATH, '//div[starts-with(@class, "Question_body__")]')
        make_header = True
        for question_body in questions_body:
            #get question
            question_element = question_body.find_element(By.XPATH,  './/h2[starts-with(@class, "Question_question__")]')
            _data = self.data_structure.copy()
            _data['topic'] = topic
            _data['class'] = class_number
            _data['subject'] = subject
            _data['difficulty'] = difficulty

            _q = question_element.text
            _data['q'] = _q
            options = question_body.find_elements(By.XPATH,  './/div[contains(@class, "Option_choices__")]')
            option_counter = 0
            # time.sleep(self.PAUSE_TIME)
            answer = ''
            #get options and correct answer
            for option in options:
                if option_counter == 0:
                    self.actions.move_to_element(option).click().perform()
                    # option.click()
                _letter = alc[option_counter].capitalize()
                option_class = option.get_attribute('class')
                if re.search(r'Option_correct__', option_class):
                    answer +=  _letter + ','
                option_element = option.find_element(By.XPATH,  './/div[contains(@class, "Option_content__")]/div[1]')
                _op = option_element.text
                _data[f'op{_letter}'] = _op
                option_counter += 1
            answer = answer[:-1]
            _data['a'] = answer
            # get explanation
            view_solution = question_body.find_element(By.XPATH, './/div[contains(@class, "Question_answerCtaWrapper__")]')
            self.actions.move_to_element(view_solution).click().perform()
            explanation_element = question_body.find_element(By.XPATH, './/div[contains(@class, "Question_list__")]')
            explanation = explanation_element.text
            _data['e'] = explanation
            df = pd.DataFrame(data=_data,  index=[0])
            df.to_csv('.data/data.csv', mode='a', index=False, sep='|',  header=make_header)
            make_header = False
            del _data, df
