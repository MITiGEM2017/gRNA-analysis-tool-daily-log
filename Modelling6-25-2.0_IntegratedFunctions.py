# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 10:11:52 2017

@author: wangq
"""

# All packages
import re
from timeit import default_timer as timer
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


# Input function
# User input intron sequence
# 5' GU
# 3' AG
# Polyprimidine
# AUCG
def intron_input():
    t = True
    AUCG_test = True
    while t and AUCG_test:
        seq = input('Please input your intron sequence...   ')
        seq = seq.upper()
        if len(seq)<26:
            print("Invalid input. [Length of the intron invalid]")
        elif (seq[:2]!="GU" or seq[len(seq)-2:]!="AG"):
            print("Invalid input. [Conserved sequence invalid]")
        else:
            num = 0
            while num<len(seq):
                if seq[num] not in 'AUCG':
                    print("Invalid input. [Nucleotides other than A,U,C,G]")
                    print("Invalid base position:",num)
                    num=100000
                else:
                    num+=1

            if num != 100000:
                print("Your input intron sequence is",seq)
                t=False
                AUCG_test = False
    print("The size of the intron is ",len(seq)," nucleotides.")
    return seq


"""
#Factors of the System
1. Secondary Structure of intron and gRNA
2. Off-target binding
3. GC content
4. location on Cas13a
5. Competition of proteins at the site
6. Location of activator/repressor
"""



def start_site(seq,gRNA_len):
    site=[]
    pos = 3
    while pos<(len(seq)-gRNA_len):
        site.append(pos)
        pos+=1
    #print (site)
    return site
#return the available start site of guide RNA



"""
Produce gRNA in a list
Could be traced with position number
"""

#Tiling
def gen_gRNA_seq(seq,site,gRNA_len):
    gRNA_list = []
    for gRNA_pos in site:
        temp = ""+tracrRNA_seq
        for num in range(gRNA_len):
            position = num+gRNA_pos-1
            base = seq[position]
            index = "AUCG".find(base)
            complement = "UAGC"[index]
            temp += complement
        gRNA_list.append(temp)
    #return a list containing all the guide RNA sequences
    print ("The number of guide RNA sequences is ",len(gRNA_list))
    #Count the number of the gRNA sequences - for test use
    return gRNA_list


def hairpin_gRNA(gRNA_seq):
    print ("[Process Reminder] -----------> Webdriving started.")
    print ("\n")
    print ("Webdriving and Scraping in process -----------> Please wait patiently.")
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
    print ("\n")
    print ("[Process Reminder] -----------> Webdriving and scraping finished")
    print ("\n")
    print ("It takes ",end-start,"seconds to run OligoAnalyzer for the gRNA with sequence: ",gRNA_seq)
    print ("\n")
    hp_driver.quit()
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
    """

def oligoAnalyzer_extract_specific_info(final_hp_list,variable_name):
    variable_list = ["sequence","complement","length","gc content","melt temp","molecular weight","extinction coefficient","nmole","ug"]
    if variable_name not in variable_list:
        return ("Invalid input variable name. ")
    index = variable_list.index(variable_name)
    result = []    
    for hp_each_list in final_hp_list:
        #temp = [float(s) for s in hp_each_list[index].split() if s.isdigit()]
        temp = re.findall("\d+\.\d+", hp_each_list[index])
        if (len(temp)==0):
            temp = [float(s) for s in hp_each_list[index].split() if s.isdigit()]
        result.append(temp)
        
    return result


# Global Constant
gRNA_length = 22
intron_seq = intron_input()
tracrRNA_seq = "CCACCCCAAUAUCGAAGGGGACUAAAAC"

# Where running codes start
gRNA_start_site = start_site(intron_seq, gRNA_length)
gRNA_seq_list = gen_gRNA_seq(intron_seq, gRNA_start_site,gRNA_length)


gRNA_stats_list = []

t1 = timer()
for gRNA_sequence in gRNA_seq_list:
    print ("\n")
    print ("---------------------separation line------------------------")
    print ("\n")
    stats_list_secondary_structure = hairpin_gRNA(gRNA_sequence)
    print("Data fetched for this gRNA is following: ")
    print ("\n")
    for reading in stats_list_secondary_structure:
        print ("Data reading -----> ",reading)
    gRNA_stats_list.append(stats_list_secondary_structure)
    print
t2 = timer()
print ("\n")
print ("[Process Reminder] -----> Obataining all data completed.")
print ("It takes ",(t2-t1)," seconds in total to finish obtaining data from OligoAnalyzer. ")
#print (gRNA_stats_list)














#CG distribution
#score_list = [] #the list containing all the numbers of hydrogen bonds
#for gRNA in gRNA_list:
#    score = 0
#    for base in gRNA:
#        if (base=="C" or base=="G"):
#            score += 3
#        else:
#            score += 2
#    score_list.append(score)
