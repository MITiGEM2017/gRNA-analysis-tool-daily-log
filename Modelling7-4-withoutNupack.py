# -*- coding: utf-8 -*-
"""
Created on Wed Jun 3 14:59:28 2017

@author: wangq
"""

# All packages

import sys
import ast
import re
import csv
import time
from timeit import default_timer as timer
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from random import randint
from tqdm import *


"""
Our Intron sequence: GTGAGTCTATGGGACCCTTGATGTTTTCTTTCCCCTTCTTTTCTATGGTTAAGTTCATGTCATAGGAAGGGGAGAAGTAACAGGGTACAGTTTAGAATGGGAAACAGACGAATGATTGCATCAGTGTGGAAGTCTCAGGATCGTTTTAGTTTCTTTTATTTGCTGTTCATAACAATTGTTTTCTTTTGTTTAATTCTTGCTTTCTTTTTTTTTCTTCTCCGCAATTTTTACTATTATACTTAATGCCTTAACATTGTGTATAACAAAAGGAAATATCTCTGAGATACATTAAGTAACTTAAAAAAAAACTTTACACAGTCTGCCTAGTACATTACTATTTGGAATATATGTGTGCTTATTTGCATATTCATAATCTCCCTACTTTATTTTCTTTTATTTTTAATTGATACATAATCATTATACATATTTATGGGTTAAAGTGTAATGTTTTAATATGTGTACACATATTGACCAAATCAGGGTAATTTTGCATTTGTAATTTTAAAAAATGCTTTCTTCTTTTAATATACTTTTTTGTTTATCTTATTTCTAATACTTTCCCTAATCTCTTTCTTTCAGGGCAATAATGATACAATGTATCATGCCTCTTTGCACCATTCTAAAGAATAACAGTGATAATTTCTGGGTTAAGGCAATAGCAATATTTCTGCATATAAATATTTCTGCATATAAATTGTAACTGATGTAAGAGGTTTCATATTGCTAATAGCAGCTACAATCCAGCTACCATTCTGCTTTTATTTTATGGTTGGGATAAGGCTGGATTATTCTGAGTCCAAGCTAGGCCCTTTTGCTAATCATGTTCATACCTCTTATCTTCCTCCCACAG
upstream exon sequence (20 nt): ccttcatcaaccacacccag
downstream exon sequence (20nt): ggcttcacctgggaaagagt
"""

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
        elif (seq[:2]!="GT" or seq[len(seq)-2:]!="AG"):
            print("Invalid input. [Conserved sequence invalid]")
        else:
            num = 0
            while num<len(seq):
                if seq[num] not in 'ATCG':
                    print("Invalid input. [Nucleotides other than A,T,C,G]")
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
    pos = 0

    while pos<(len(seq)-gRNA_len):
        signal = True
        if(seq[pos+gRNA_len]=="G"):
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
            index = "ATCG".find(base)
            complement = "UAGC"[index]
            temp += complement
        gRNA_list.append(temp)
    #return a list containing all the guide RNA sequences
    print ("The number of guide RNA sequences is ",len(gRNA_list))
    #Count the number of the gRNA sequences - for test use
    return gRNA_list



def diff_letters(a,b):
    return sum ( a[i] != b[i] for i in range(len(a)) )


def off_target_mismatch(mRNA_seq,gRNA_seq):
    crRNA_seq = gRNA_seq[-gRNA_length:]
    print(crRNA_seq)

    count = 0
    difference_list = []
    RNA_complement = ""
    for num in range(len(crRNA_seq)):
        base = crRNA_seq[num]
        index = "UAGC".find(base)
        complement = "ATCG"[index]
        RNA_complement += complement
    print(RNA_complement)

    for start_pos in range (len(mRNA_seq)-len(crRNA_seq)+1):
        DNA_seq = mRNA_seq[start_pos:(start_pos+len(crRNA_seq))]
        #print(RNA_complement)
        if diff_letters(RNA_complement,DNA_seq) < off_target_mismatch_threshold:
            count +=1
            difference_list.append(diff_letters(RNA_complement,DNA_seq))
            
        if (start_pos%100000 == 0):
            print("Currently at",start_pos,"th base.")

    return count, difference_list


def remove_values_from_list(the_list, val):
    while val in the_list:
        the_list.remove(val)


def RBP_data_scrap(analyze_seq):
    # RBPmap mapping binding sites of RNA bindinG proteins
    # "http://rbpmap.technion.ac.il/"

    RBP_driver = webdriver.Chrome()
    RBP_driver.get("http://rbpmap.technion.ac.il/")

    mRNA_input = analyze_seq


    # The following is to find the text field and input sequence
    mRNA_input_Xpath = "//textarea"
    mRNA_input_Field = WebDriverWait(RBP_driver,10).until(lambda RBP_driver: RBP_driver.find_element_by_xpath(mRNA_input_Xpath))
    mRNA_input_Field.clear()
    mRNA_input_Field.send_keys(mRNA_input)
    # send the input in the text box


    mode_Xpath = "//*[@id=\"motifs_block\"]/div[1]/div[2]/div[2]/input[1]"
    mode_field = WebDriverWait(RBP_driver,10).until(lambda RBP_driver: RBP_driver.find_element_by_xpath(mode_Xpath))
    mode_field.click()
    # click the mode selection


    click_here_Xpath = "//*[@id=\"motifs_block\"]/div[1]/div[2]/div[2]/a"
    click_here_field = WebDriverWait(RBP_driver,10).until(lambda RBP_driver: RBP_driver.find_element_by_xpath(click_here_Xpath))
    click_here_field.click()
    #click the "click here" button


    RBP_driver.switch_to_window(RBP_driver.window_handles[1])
    choose_RBP_Xpath = "/html/body/form/table/tbody/tr[2]/td/div[1]/input"
    choose_RBP_field = WebDriverWait(RBP_driver,10).until(lambda RBP_driver: RBP_driver.find_element_by_xpath(choose_RBP_Xpath))
    choose_RBP_field.click()
    # click the "Human" RBPs in the new window


    submit_RBP_Xpath = "/html/body/form/table/tbody/tr[4]/td/input"
    submit_RBP_field = WebDriverWait(RBP_driver,10).until(lambda RBP_driver: RBP_driver.find_element_by_xpath(submit_RBP_Xpath))
    submit_RBP_field.click()
    # click submit button


    RBP_driver.switch_to_window(RBP_driver.window_handles[0])
    submit_analysis_Xpath = "/html/body/table/tbody/tr[2]/td[2]/form/table/tbody/tr[6]/td/input[1]"
    #submit_analysis_Xpath = "(//input[@value])[14]"
    submit_analysis_field = WebDriverWait(RBP_driver,10).until(lambda RBP_driver: RBP_driver.find_element_by_xpath(submit_analysis_Xpath))
    submit_analysis_field.click()
    #click the submit button for the analysis

    print ("RNA binding protein site analysis in progress ------")
    print ("This process should take less than 1 minute.")
    view_result_Xpath = "/html/body/table/tbody/tr[2]/td[2]/div[8]/div[3]/a"
    view_result_field = WebDriverWait(RBP_driver,60).until(lambda RBP_driver: RBP_driver.find_element_by_xpath(view_result_Xpath))
    print ("Process finished.")
    # waiting for the result for at most 1 minute(s), could be modified
    view_result_field.click()


    table_Xpath = "(//table)[3]"
    RBP_initial_table = WebDriverWait(RBP_driver,30).until(lambda RBP_driver: RBP_driver.find_elements_by_xpath(table_Xpath))
    RBP_rearranged_table = [x.text for x in RBP_initial_table][0]  # String we want
    nicer_table = RBP_rearranged_table.split("\n")
    remove_values_from_list(nicer_table, 'Position Motif Occurrence Z-score P-value')


    count = 0
    final_table = []
    nicer_table.append("xxx")
    while count<(len(nicer_table)):
        reading = nicer_table[count]
        temp = ""
        if reading[:7] == "Protein":
            temp += (reading[:8] + reading[9:])
            inner_count = 1
            while (nicer_table[inner_count+count][:7] != "Protein"):
                if(inner_count+count)<(len(nicer_table)-1):
                    add_content = temp+" "+nicer_table[inner_count+count]
                    final_table.append(add_content)
                    inner_count +=1
                else:
                    break

        #final_table.append(temp)
        #print (temp)
        count += inner_count

    ult_table = []
    for data_string in final_table:
        temp = data_string.split()
        del temp[3]
        temp.append(len(temp[2]))  # add a column containing length of the motif
        temp[0] = temp[0][8:-7]
        temp[1] = int(temp[1]) - len(upstream_exon)
        temp[3] = float(temp[3])
        temp[4] = float(temp[4])
        temp.append((len(temp[2])+temp[1]-1)) # add a colum containing the end position of the motif
        ult_table.append(temp)

    RBP_driver.quit()
    return ult_table


# Function used to extract the dissociation constant for a given RBP name and the data_list
def extract_RBP_Kd(RBP_Kd_list, RBP_name):
    for each_RBP in RBP_Kd_list:
        if(each_RBP[0]==RBP_name):
            return float(each_RBP[1])
    return False


#RBP score calculation tool
def RBP_competition_score(site,gRNA_seq,gRNA_list,RBP_data_list,RBP_Kd_list):
    start_pos = site[gRNA_list.index(gRNA_seq)]
    end_pos = start_pos + gRNA_length -1
    potential_RBP_list = []
    partial_RBP_list = []

    for row in RBP_data_list:
        if (row[1]<=end_pos and row[1]>=start_pos):
            if(row[-1]<=end_pos):
                potential_RBP_list.append(row)
            else:
                partial_RBP_list.append(row)
        elif (row[-1]>=start_pos and row[1]<start_pos):
            partial_RBP_list.append(row)


    sum_RBP_interference_score = 0  # return value

    # For the score from RBPs that completely bind in the region
    sum_complete_bind = 0
    RBP_num_count = 0
    while RBP_num_count < len(potential_RBP_list):
        potential_info_list = potential_RBP_list[RBP_num_count]
        potential_start_pos = potential_info_list[1]
        potential_RBP_test = True
        power_count = 0
        base_score = ((1-potential_info_list[4])**binding_prob_power)*extract_RBP_Kd(RBP_Kd_list,potential_info_list[0])
        complete_score_list = []
        complete_score_list.append(base_score)
        while (potential_RBP_test and (RBP_num_count+power_count+1)<len(potential_RBP_list)):
            if(potential_RBP_list[RBP_num_count+power_count+1][1] == potential_start_pos):
                power_count += 1
                potential_info_list = potential_RBP_list[RBP_num_count+power_count]
                additional_score = ((1-potential_info_list[4])**binding_prob_power)*extract_RBP_Kd(RBP_Kd_list,potential_info_list[0])  #temporary score
                complete_score_list.append(additional_score)
            else:
                potential_RBP_test = False
                RBP_num_count += power_count


        if len(complete_score_list) > 1:
            while len(complete_score_list) > 1:
                minimum_score = min(complete_score_list)
                sum_complete_bind += minimum_score*(weighted_factor**power_count)
                power_count -= 1
                complete_score_list.remove(minimum_score)

        else:
            sum_complete_bind += base_score


        RBP_num_count += 1



    # Score for partially bind RBPs in the region
    sum_partially_bind = 0
    RBP_num_count = 0
    while RBP_num_count < len(partial_RBP_list):
        potential_info_list = partial_RBP_list[RBP_num_count]
        potential_start_pos = potential_info_list[1]
        potential_RBP_test = True
        power_count = 0
        factor = min((potential_info_list[6]-start_pos+1),(end_pos-potential_info_list[1]+1))/potential_info_list[5]
        base_score = ((1-potential_info_list[4])**binding_prob_power)*extract_RBP_Kd(RBP_Kd_list,potential_info_list[0])*factor
        complete_score_list = []
        complete_score_list.append(base_score)
        while (potential_RBP_test and (RBP_num_count+power_count+1)<len(partial_RBP_list)):
            if(partial_RBP_list[RBP_num_count+power_count+1][1] == potential_start_pos):
                power_count += 1
                potential_info_list = partial_RBP_list[RBP_num_count+power_count]
                factor = min((potential_info_list[6]-start_pos+1),(end_pos-potential_info_list[1]+1))/potential_info_list[5]
                additional_score = ((1-potential_info_list[4])**binding_prob_power)*extract_RBP_Kd(RBP_Kd_list,potential_info_list[0])*factor  #temporary score
                complete_score_list.append(additional_score)
            else:
                potential_RBP_test = False
                RBP_num_count += power_count

        if len(complete_score_list) > 1:
            while len(complete_score_list) > 1:
                minimum_score = min(complete_score_list)
                sum_partially_bind += minimum_score*(weighted_factor**power_count)
                power_count -= 1
                complete_score_list.remove(minimum_score)
        else:
            sum_partially_bind += base_score

        RBP_num_count += 1

    sum_RBP_interference_score = sum_partially_bind+sum_complete_bind


    return sum_RBP_interference_score



# Nupack
#"http://www.nupack.org/partition/new"
# Secondary Structure analysis

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

    final_Nupack_gRNA_list =[]
    for line in better_table:
        temp = line.split()
        final_Nupack_gRNA_list.append(temp)


    hp_driver.quit()



    end = timer()
    print ("It takes ",round(end-start)," seconds to finish the Nupack analysis for the sequence: ", gRNA_seq)
    return final_Nupack_gRNA_list




def Nupack_gRNA_score(final_Nupack_gRNA_list):
    Nupack_gRNA_score_list = []
    for each_gRNA_data in final_Nupack_gRNA_list:
        temp_list = each_gRNA_data[-(len(tracrRNA_seq)+gRNA_length):]  # Get the range of -50: ---> all containing individual probabilities of stem loop
        temp_product = 1

        for subset in temp_list:
            if (subset[1]=="-1"):
                prob = float(subset[2])
            else:
                prob = 0.001

            temp_product *= prob

        Nupack_gRNA_score_list.append(temp_product)

    return Nupack_gRNA_score_list




# calculate the GC content of the givern sequence - sgRNA
def GC_content(gRNA_seq):
    return round((gRNA_seq.count("C")+gRNA_seq.count("G"))/(len(gRNA_seq)),3)







print ("The default setting for this program is not to have a log file.")
log_choice = input("Would you like to have a log file? ---- press y to answer YES.        ")
log_judge = (log_choice.lower() == "y")




# Global Constant
gRNA_length = 22
intron_seq = intron_input()
tracrRNA_seq = "CCACCCCAAUAUCGAAGGGGACUAAAAC"
off_target_mismatch_threshold = 4
upstream_exon = "CCTTCATCAACCACACCCAG"
downstream_exon = "GGCTTCACCTGGGAAAGAGT"
weighted_factor = 0.4
binding_prob_power = 2



# Start the log or not
if(log_judge):
    print ("The rest of the process would not be shown on the interface. Instead, it will be recorded as message.log in your working directory.")
    old_stdout = sys.stdout
    log_file = open("message.log","w")
    sys.stdout = log_file



#Generate a random mRNA
mRNA = ""
for n in range (7000):
    mRNA += "ATCG"[randint(0,3)]


# Where running codes start
gRNA_start_site = start_site(intron_seq, gRNA_length)
gRNA_seq_list = gen_gRNA_seq(intron_seq, gRNA_start_site,gRNA_length)



gRNA_stats_list = []



# Following is for a separate run if no Nupack data locally
"""
t1 = timer()
gRNA_count = 0
total_time = 0


for gRNA_sequence in gRNA_seq_list:
    print ("\n")
    print ("---------------------separation line------------------------")
    print ("\n")

    s = timer()

    stats_list_secondary_structure = Nupack_data_scrap(gRNA_sequence)
    print("\n")
    print("Data fetched for this gRNA is following: ")
    print ("\n")
    for reading in stats_list_secondary_structure:
       print ("Data reading -----> ",reading)
    gRNA_stats_list.append(stats_list_secondary_structure)
    gRNA_count += 1

    e = timer()
    time = e - s
    total_time += time
    average_time = float(total_time/gRNA_count)

    print ("\n")
    print (float(100*gRNA_count/(len(gRNA_seq_list)))," % of gRNA has been analyzed.")
    pending_time = average_time*(len(gRNA_seq_list)-gRNA_count)
    #print(pending_time)
    if pending_time > 3600:
        print ("Pending time: Approximately ",int(pending_time/3600)," hour(s) and ",int((pending_time%3600)/60), " minute(s).")
    elif pending_time > 60:
        print ("Pending time: Approximately ", int(pending_time/60)," minute(s) and ", int(pending_time%60)," second(s).")
    else:
        print("Pending time: Approximately ", int(pending_time), " seconds.")




t2 = timer()
print ("\n")
print ("[Process Reminder] -----> Obataining all data completed.")

total_time = t2-t1
if total_time>3600:
    print ("It takes ",int(total_time/3600)," hour(s)", int(total_time%60)," minute(s) in total to finish obtaining data from Nupack. ")
elif total_time > 60:
    print ("It takes ",int(total_time/60)," minute(s)", round((total_time%60),1)," seconds in total to finish obtaining data from Nupack. ")
else:
    print ("It takes ",total_time," seconds in total to finish obtaining data from Nupack. ")
#print (gRNA_stats_list)



with open('Nupack_data.csv','w',newline='') as fp:
    a = csv.writer(fp,delimiter=',')
    a.writerows(gRNA_stats_list)
"""


with open("Nupack_data.csv", "r") as nfile:
    nreader = csv.reader(nfile)
    for row in nreader:
        gRNA_stats_list.append(row)

for each_gRNA in gRNA_stats_list:
    for data in each_gRNA:
        each_gRNA[each_gRNA.index(data)] = ast.literal_eval(data)

Nupack_gRNA_final_score = Nupack_gRNA_score(gRNA_stats_list)





# RBP data list from RBPmap
RBP_time1 = timer()
RBP_initial_data = RBP_data_scrap((upstream_exon+intron_seq+downstream_exon))
RBP_data = sorted(RBP_initial_data,key=lambda x:x[1]) # Sort the RBP data list based on position value, which is in 2nd columm
RBP_time2 = timer()
print("The RBP data scrapping takes ", int(RBP_time2-RBP_time1), "second(s) to finish. ")


# dissociation constant data for RBPs
kd_data_list = []
with open('RBP_binding_affinity_data.csv',"r") as file:
    filereader = csv.reader(file)
    for row in filereader:
        kd_data_list.append(row)

kd_data_list[0][0] = kd_data_list[0][0][-4:]


RBP_competition_score_list = []
for each_gRNA in tqdm(gRNA_seq_list):
    temp_score = RBP_competition_score(gRNA_start_site,each_gRNA, gRNA_seq_list, RBP_data,kd_data_list)
    RBP_competition_score_list.append(temp_score)

RBP_score_factor_num = 0
RBP_competition_rearranged_score_list = [0]
while max(RBP_competition_rearranged_score_list)<1:
    RBP_score_factor_num += 1
    RBP_competition_rearranged_score_list = [each_score*(10**RBP_score_factor_num) for each_score in RBP_competition_score_list]




# Log recording ends
if(log_judge):
    sys.stdout = old_stdout
    log_file.close()
