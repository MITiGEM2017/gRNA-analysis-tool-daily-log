# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 18:50:44 2017

@author: wangq
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from timeit import default_timer as timer

# Nupack
#"http://www.nupack.org/partition/new"

def Nupack_data_scrap(gRNA_seq):
    start = timer()
    hp_driver = webdriver.Chrome()
    hp_driver.get("http://www.nupack.org/partition/new")

    # The following is to find the text field and input sequence
    gRNA_input_Xpath = "//textarea"
    gRNA_input_Field = WebDriverWait(hp_driver,30).until(lambda hp_driver: hp_driver.find_element_by_xpath(gRNA_input_Xpath))
    gRNA_input_Field.clear()
    gRNA_input_Field.send_keys(gRNA_seq)

    analyze_button_name = "commit"
    analyze_button_element = WebDriverWait(hp_driver,30).until(lambda hp_driver: hp_driver.find_element_by_name(analyze_button_name))
    analyze_button_element.click()

    switch_element = WebDriverWait(hp_driver,60).until(lambda hp_driver: hp_driver.find_element_by_id("dp"))
    switch_element.click()

    download_data_Xpath = "//*[@id=\"svg_link\"]/a[2]"
    download_data_element = WebDriverWait(hp_driver,30).until(lambda hp_driver: hp_driver.find_element_by_xpath(download_data_Xpath))
    download_data_element.click()

    data_elements = WebDriverWait(hp_driver,30).until(lambda hp_driver: hp_driver.find_elements_by_tag_name("body"))
    improved_data = [x.text for x in data_elements][0]
    better_table = improved_data.split("\n")
    better_table = better_table[13:]
    
    final_list =[]
    for line in better_table:
        temp = line.split()
        final_list.append(temp)
            
    end = timer()
    print ("It takes ",round(end-start)," seconds to finish the Nupack analysis.")
    return final_list


