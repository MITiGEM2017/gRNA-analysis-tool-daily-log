# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 09:48:20 2017

@author: wangq

README:
    Transfer into a function that produces running time and a list of the statistics of the gRNA sequence
    statisics include: 
    Sequence, Complement, Length, GC Content, Melt temp, Molecular weight, Extinction coefficient, nmole/OD260, ug/OD260

"""
from timeit import default_timer as timer
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


gRNA_input = "AUGCAUGCAUGCAUGAUGAUCGAUCGAUCGA"  #Test value needs to be modified later


def hairpin_gRNA(gRNA_seq):
    print ("[Process Reminder] -----------> Webdriving started.")
    start = timer()
    hp_driver = webdriver.Chrome()
    hp_driver.get("https://www.idtdna.com/calc/analyzer")

    # The following is to find the text field and input sequence
    gRNA_input_Xpath = "//textarea"
    gRNA_input_Field = WebDriverWait(hp_driver,10).until(lambda hp_driver: hp_driver.find_element_by_xpath(gRNA_input_Xpath))
    gRNA_input_Field.clear()
    gRNA_input_Field.send_keys(gRNA_seq)

    # The following is to click the analyze button
    gRNA_input_ID = "analyze-button"
    analyze_button_element = WebDriverWait(hp_driver,10).until(lambda hp_driver: hp_driver.find_element_by_id(gRNA_input_ID))
    analyze_button_element.click()

    #table_Xpath = "(//table[@class=\"table\"])[1]")
    hp_initial_table = WebDriverWait(hp_driver,10).until(lambda hp_driver: hp_driver.find_elements_by_class_name("table"))
    hp_rearranged_table = [x.text for x in hp_initial_table][0]  # String we want
    final_hp_list = hp_rearranged_table.split("\n")              # A list of data
    end = timer()
    print ("[Process Reminder] -----------> Webdriving and scraping finished")
    print ("It takes ",end-start,"seconds to run the test for secondary structure of the gRNA with sequence: ",gRNA_seq)
    return final_hp_list

"""
index for each variable in the list[final_hp_list]:
Sequence: 0
Complement: 1
Length: 2
GC Content: 3
Melt temp: 4
Molecular weight: 5
Extinction coefficient: 6
nmole/OD260: 7
ug/OD260:8

For test use
"""
#print (final_hp_list)
#for each_item in final_hp_list:
#    print(each_item)