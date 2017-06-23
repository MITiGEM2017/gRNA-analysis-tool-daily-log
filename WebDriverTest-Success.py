# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 15:02:35 2017

@author: wangq
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait



driver = webdriver.Chrome()
driver.get("https://www.facebook.com")

facebookUsername = "1517078450@qq.com"
facebookPassword = "qchwang14657"
emailFieldID = "email"
passFieldID = "pass"
loginButtonXpath = "//input[@value='Log In']"
fbLogoXpath = "(//div[@dir='ltr'])[3]"

emailFieldElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_id(emailFieldID))
passFieldElement  = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_id(passFieldID))
loginButtonElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(loginButtonXpath))


emailFieldElement.clear()
emailFieldElement.send_keys(facebookUsername)
passFieldElement.clear()
passFieldElement.send_keys(facebookPassword)
loginButtonElement.click()

#messElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(fbLogoXpath))
#messElement.click()