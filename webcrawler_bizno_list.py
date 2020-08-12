import os
import re
import numpy as np
import pandas as pd
import math

from automation.common import *
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

driver = None
input_path = ''


class App:
    def __init__(self):
        self.app_id = []
        self.app_name = []
        self.bizno = []

    def set_header(self, app_id, app_name, bizno):
        self.app_id.append(app_id)
        self.app_name.append(app_name)
        self.bizno.append(bizno)

    def set_property(self, app_id, app_name, bizno):
        self.app_id.append(app_id)
        self.app_name.append(app_name)
        self.bizno.append(bizno)

    def save(self, path):
        row = {"app_id": self.app_id,
               "app_name": self.app_name,
               "bizno": self.bizno}
        df = pd.DataFrame(row)
        df.to_csv(path, mode='a', encoding='euc-kr', index=False, header=False)


def run(path, bizno_path, user_id, user_pw):
    #global variable
    global input_path
    input_path = path

    setting(user_id, user_pw)
    core(bizno_path)
    print('program end')


def setting(user_id, user_pw):
    #global variable
    global driver

    # Initialise Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    url = #{your_url_here}

    # Open webpage
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    driver.get(url)

    # Sign-in
    sleep(1)
    driver.find_element_by_css_selector('#input_id').send_keys(user_id)
    driver.find_element_by_css_selector('#input_password').send_keys(user_pw)
    driver.find_element_by_css_selector('button[type="submit"]').click()


def core(bizno_path):
    #global variable
    global input_path
    global driver
    df = pd.read_csv(input_path, encoding='euc-kr')
    app_id_array = df['app_id']  # app name array
    check_array = df['check']

    if type(check_array[0]) != str:
        app = App()
        app.set_header('app_id', 'app_name', 'bizno')
        app.save(bizno_path)

    for index, app_id in enumerate(app_id_array):
        if type(check_array[index]) == str:
            print('continue')
            continue
        element = "N/A"
        app_url = #{your_specific_url_here}

        try:
            driver.get(app_url)
            body = wait_element(driver, 'body')
            app_name = body.find_element_by_css_selector('h3').text
            Overalls = body.find_elements_by_css_selector('your_css_selector_here')
            for i in range(len(Overalls)):
                rowname = Overalls[i].find_element_by_css_selector('th').text
                if "{TARGET}" in rowname.strip():
                    element = Overalls[i].find_element_by_css_selector('td').text

        except Exception as e:
            print(e)
            print('acccount-id selection error')
            break
        print(app_name)
        app = App()
        app.set_property(app_id, app_name, element)
        app.save(bizno_path)

        check_array[index] = 'O'
        save_csv(df, input_path)
