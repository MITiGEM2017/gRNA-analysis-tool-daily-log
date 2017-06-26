# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 13:59:44 2017

@author: wangq
"""

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
from random import randint



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
#  Factors of the System
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
    signal = True
    while pos<(len(seq)-gRNA_len):
        if(seq[pos+gRNA_len-1]=="G"):
            signal = False
        
        if(signal):
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


def hairpin_gRNA_TypeA(gRNA_seq):
    print ("[Process Reminder] -----------> Webdriving started.")
    print ("\n")
    print ("[ATTENTION] --------------> Type A OligoAnalyzer data Scraping.")
    print ("\n")
    print ("----------------------- Type A Analysis in Progress ------------------------------")
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

    hairpin_button_Xpath = "//*[@id=\"OligoAnalyzer\"]/div[2]/div[1]/div/div[3]/button[2]"
    hairpin_button_element = WebDriverWait(hp_driver,10).until(lambda hp_driver: hp_driver.find_element_by_xpath(hairpin_button_Xpath))
    hairpin_button_element.click()


    end = timer()
    print ("\n")
    print ("[Process Reminder] -----------> Webdriving and scraping finished")
    print ("\n")
    print ("----------------------- Type A Analysis Finished ------------------------------")
    print ("\n")
    print ("It takes ",end-start,"seconds to run Type A OligoAnalyzer for the gRNA with sequence: ",gRNA_seq)
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




def hairpin_gRNA_TypeB(gRNA_seq):
    print ("[Process Reminder] -----------> Webdriving started.")
    print ("\n")
    print ("[ATTENTION] --------------> Type B OligoAnalyzer data Scraping.")
    print ("\n")
    print ("------------------------ Type B Analysis in Progress -------------------------------")
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

    hairpin_button_Xpath = "//*[@id=\"OligoAnalyzer\"]/div[2]/div[1]/div/div[3]/button[2]"
    hairpin_button_element = WebDriverWait(hp_driver,10).until(lambda hp_driver: hp_driver.find_element_by_xpath(hairpin_button_Xpath))
    hairpin_button_element.click()

    table_Xpath = "//*[@id=\"OAResults\"]/div/div[2]/div[7]/div/table/tbody"
    hp_initial_table2 = WebDriverWait(hp_driver,10).until(lambda hp_driver: hp_driver.find_elements_by_xpath(table_Xpath))
    hp_rearranged_table2 = [x.text for x in hp_initial_table2][0]  # String we want
    final_hp_list2_temp = hp_rearranged_table2.split("\n")

    final_hp_list2 = []
    for stats in final_hp_list2_temp:
        temp = stats[2:]
        final_hp_list2.append(temp.split())

    end = timer()
    print ("\n")
    print ("[Process Reminder] -----------> Webdriving and scraping finished")
    print ("\n")
    print ("----------------------- Type B Analysis Finished ------------------------------")
    print ("\n")
    print ("It takes ",end-start,"seconds to run Type B OligoAnalyzer for the gRNA with sequence: ",gRNA_seq)
    print ("\n")
    hp_driver.quit()
    return final_hp_list2








def oligoAnalyzer_extract_specific_info_TypeA(final_hp_list,variable_name):
    variable_list = ["sequence","complement","length","gc content","melt temp","molecular weight","extinction coefficient","nmole","ug"]
    if variable_name not in variable_list:
        return ("Invalid input variable name. ")
    index = variable_list.index(variable_name)
    hp_result1 = []
    for hp_each_list in final_hp_list:
        #temp = [float(s) for s in hp_each_list[index].split() if s.isdigit()]
        temp = re.findall("\d+\.\d+", hp_each_list[index])
        if (len(temp)==0):
            temp = [float(s) for s in hp_each_list[index].split() if s.isdigit()]
        hp_result1.append(temp)

    return hp_result1


def oligoAnalyzer_extract_specific_info_TypeB(final_hp_list,index):
    hp_result2 = []
    for hp_each_list in final_hp_list:
        #temp = [float(s) for s in hp_each_list[index].split() if s.isdigit()]
        #temp = re.findall("\d+\.\d+", hp_each_list[index])
        #if (len(temp)==0):
        #temp = [float(s) for s in hp_each_list[index].split() if s.isdigit()]
        hp_result2.append(hp_each_list[index])

    return hp_result2


# Function for 100% match on the mRNA somewhere
def off_target_completeMatch(mRNA_seq,gRNA_seq):
    crRNA_seq = gRNA_seq[-gRNA_length:]
    count = 0
    for start_pos in range (len(mRNA_seq)-len(crRNA_seq)+1):
        DNA_seq = mRNA_seq[start_pos:(start_pos+len(crRNA_seq))]
        RNA_complement = ""
        for num in range(len(DNA_seq)):
            base = DNA_seq[num]
            index = "ATCG".find(base)
            complement = "UAGC"[index]
            RNA_complement += complement
        #print(RNA_complement)
        if RNA_complement == crRNA_seq:
            count += 1
    return count


def diff_letters(a,b):
    return sum ( a[i] != b[i] for i in range(len(a)) )

def off_target_mismatch(mRNA_seq,gRNA_seq):
    crRNA_seq = gRNA_seq[-gRNA_length:]
    count = 0
    for start_pos in range (len(mRNA_seq)-len(crRNA_seq)+1):
        DNA_seq = mRNA_seq[start_pos:(start_pos+len(crRNA_seq))]
        RNA_complement = ""
        for num in range(len(DNA_seq)):
            base = DNA_seq[num]
            index = "ATCG".find(base)
            complement = "UAGC"[index]
            RNA_complement += complement

        #print(RNA_complement)
        if diff_letters(RNA_complement,crRNA_seq) < off_target_mismatch_threshold:
            count +=1

    return count









# Global Constant
gRNA_length = 22
intron_seq = intron_input()
tracrRNA_seq = "CCACCCCAAUAUCGAAGGGGACUAAAAC"
off_target_mismatch_threshold = 10


#Generate a random mRNA
mRNA = ""
for n in range (7000):
    mRNA += "ATCG"[randint(0,3)]


# Where running codes start
gRNA_start_site = start_site(intron_seq, gRNA_length)
gRNA_seq_list = gen_gRNA_seq(intron_seq, gRNA_start_site,gRNA_length)





gRNA_stats_list1 = []
gRNA_stats_list2 = []

t1 = timer()
for gRNA_sequence in gRNA_seq_list:
    print ("\n")
    print ("---------------------separation line------------------------")
    print ("\n")


    stats_list_secondary_structure1 = hairpin_gRNA_TypeA(gRNA_sequence)
    print("\n")
    print("Data fetched for this gRNA is following: ")
    print ("\n")
    for reading in stats_list_secondary_structure1:
        print ("Data reading -----> ",reading)
    gRNA_stats_list1.append(stats_list_secondary_structure1)


    print("\n")
    print("---------------------separation line------------------------")
    stats_list_secondary_structure2 = hairpin_gRNA_TypeB(gRNA_sequence)
    print("\n")
    print("Data fetched for this gRNA is following: ")
    print ("\n")
    for reading in stats_list_secondary_structure2:
        print ("Data reading -----> ",reading)
    gRNA_stats_list2.append(stats_list_secondary_structure2)


"""
*****************NOTE:
gRNA_stats_list1 is a double list - innest is string
gRNA_stats_list2 is a triple list - innest is float

"""


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
