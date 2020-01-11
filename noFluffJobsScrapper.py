from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import re
import os

class fluffScrapper():

    def __init__(self):
        
        self.driver = webdriver.Chrome(os.path.dirname(__file__), 'chromedriver.exe')

if __name__ == '__main__':

    scrapper = fluffScrapper()