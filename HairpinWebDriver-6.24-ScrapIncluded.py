# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 16:14:45 2017

@author: wangq
"""

#https://www.idtdna.com/calc/analyzer
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

hp_driver = webdriver.Chrome()
hp_driver.get("https://www.idtdna.com/calc/analyzer")

gRNA_input = "AUGCAUGCAUGCAUGAUGAUCGAUCGAUCGA"  #Test value needs to be modified later


# The following is to find the text field and input sequence
gRNA_input_Xpath = "//textarea"
gRNA_input_Field = WebDriverWait(hp_driver,10).until(lambda hp_driver: hp_driver.find_element_by_xpath(gRNA_input_Xpath))
gRNA_input_Field.clear()
gRNA_input_Field.send_keys(gRNA_input)

# The following is to click the analyze button
gRNA_input_ID = "analyze-button"
analyze_button_element = WebDriverWait(hp_driver,10).until(lambda hp_driver: hp_driver.find_element_by_id(gRNA_input_ID))
analyze_button_element.click()

#table_Xpath = "(//table[@class=\"table\"])[1]")
hp_initial_table = WebDriverWait(hp_driver,10).until(lambda hp_driver: hp_driver.find_elements_by_class_name("table"))
hp_rearranged_table = [x.text for x in hp_initial_table][0]  # String we want
final_hp_list = hp_rearranged_table.split("\n")              # A list of data

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