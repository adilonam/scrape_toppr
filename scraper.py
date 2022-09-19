

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
from selenium.common.exceptions import NoSuchElementException  
from slugify import slugify

class Scraper():
    question_index = 0
    base_url = 'https://www.toppr.com/ask/content/cbse/class-'
    host = 'https://www.toppr.com'
    PAUSE_TIME = 1
    SCROLL_GAP = 10
    CLICK_REPEAT = 10
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
            class_url  = self.base_url+str(class_name)
            for subject in self.subjects:
                subject_url = class_url + '/'+ slugify(subject)
                self.driver.get(subject_url)
                topic_urls = []
                topic_elements = self.driver.find_elements(By.XPATH, '//a[contains(@class, "ChapterList_chapterItem__")]')
                for topic_element in topic_elements:
                    _topic_url = topic_element.get_attribute('href')
                    topic_urls.append(_topic_url)
                for topic_url in topic_urls:
                    self.driver.get(topic_url)
                    topic_element = self.driver.find_element(By.XPATH, '//div[contains(@class, "chapter_title__")]')
                    topic = topic_element.text
                    difficulty_elements =  self.driver.find_elements(By.XPATH, '//a[contains(@class, "QuestionSets_storybookButton__")]')
                    difficulty_urls = []
                    for difficulty_element in difficulty_elements:
                        _difficulty_url = difficulty_element.get_attribute('href')
                        difficulty_urls.append(_difficulty_url)
                    for difficulty_url in difficulty_urls:
                        difficulty = re.findall(r'\w+(?=\/)', difficulty_url)[-1]
                        self.scrape(difficulty_url, class_name, subject, topic, difficulty)

                    a = 0

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
            
        questions_body = self.driver.find_elements(By.XPATH, '//div[contains(@class, "Question_body__")]')
        make_header = True
        for question_body in questions_body:
            #get question
            question_element = question_body.find_element(By.XPATH,  './/h2[contains(@class, "Question_question__")]')
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
                    answer_check = True
                    while answer_check:
                        try:
                            self.actions.move_to_element(option).click().perform()
                            answer_element = question_body.find_element(By.XPATH,  './/div[contains(@class, "Option_correct__")]')
                            answer_check = False
                        except:
                            time.sleep(self.PAUSE_TIME)
                    # option.click()
                _letter = alc[option_counter].capitalize()
                option_class = option.get_attribute('class')
                if re.search(r'Option_correct__', option_class):
                    answer +=  _letter + ','
                try:
                    option_element = option.find_element(By.XPATH,  './/div[contains(@class, "Option_content__")]/div[1]')
                    _op = option_element.text
                except NoSuchElementException:
                    option_element = option.find_element(By.XPATH,  './/div[contains(@class, "Option_content__")]/img[1]')
                    _op = option_element.get_attribute('src')
                _data[f'op{_letter}'] = _op
                option_counter += 1
            answer = answer[:-1]
            _data['a'] = answer
            # get explanation
            view_solution = question_body.find_element(By.XPATH, './/div[contains(@class, "Question_answerCtaWrapper_")]')
            explanation_check = True
            while explanation_check:
                try : 
                    self.actions.move_to_element(view_solution).click().perform()
                    explanation_element = question_body.find_element(By.XPATH, './/div[contains(@class, "Question_list__")]')
                    explanation_check = False
                except:
                    time.sleep(self.PAUSE_TIME)
            explanation = explanation_element.text
            _data['e'] = explanation
            df = pd.DataFrame(data=_data,  index=[0])
            df.to_csv('.data/data.csv', mode='a', index=False, sep='|',  header=make_header)
            make_header = False
            del _data, df
            self.question_index += 1
            print(f'{self.question_index} questions loaded , current subject : {subject} .')
