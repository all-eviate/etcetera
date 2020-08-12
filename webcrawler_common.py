import os
import time
import subprocess
from time import sleep
from datetime import date

import enum
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  

def save_csv(df, save_path, duplicated_drop_list = ['app_id']):
    try:
        df.drop_duplicates(duplicated_drop_list, keep='first')
        df.to_csv(save_path, encoding='euc-kr', index = False)
        print("csv written")
    except:
        duplicated_drop_list = ['channel_id']
        df.drop_duplicates(duplicated_drop_list, keep='first')
        df.to_csv(save_path, encoding='euc-kr', index = False)
        print("csv written")

def wait_element(driver, selector, second = 10):
    return WebDriverWait(driver,second).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))

def get_inner_html(element):
    #TODO : 전체적용
    return element.get_attribute('innerHTML')

def get_outer_html(element):
    #TODO : 전체적용
    return element.get_attribute('outerHTML')

def clear_cache(driver):
    package = driver.current_package
    os.system(f'adb shell pm clear {package}')
