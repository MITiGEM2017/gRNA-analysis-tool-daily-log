# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 15:19:32 2017

@author: wangq
"""
import csv
direct_repeat_sequence = "CCACCCCAATATCGAAGGGGACTAAAAC"

pre_structure_data_list =[]
for gRNA in tqdm(gRNA_seq_list):
    gRNA_seq = gRNA[-gRNA_length:]
    pre_structure = direct_repeat_sequence + gRNA_seq + direct_repeat_sequence
    pre_structure_data = Nupack_data_scrap(pre_structure)
    pre_structure_data_list.append(pre_structure_data)

with open('Pre_crRNA_structure_Nupack_data.csv','w',newline='') as fp:
    a = csv.writer(fp,delimiter=',')
    a.writerows(pre_structure_data_list)