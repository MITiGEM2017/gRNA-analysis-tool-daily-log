# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 17:49:10 2017

@author: wangq
"""

def RBP_competition_score(site,gRNA_seq,gRNA_list,RBP_data_list):
    start_pos = site[gRNA_list.index(gRNA_seq)]
    end_pos = start_pos + gRNA_length -1
    print (start_pos)
    print (end_pos)
    
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
    
    print(potential_RBP_list)
    print("\n")
    print(partial_RBP_list)
    
RBP_competition_score(gRNA_start_site, 'CCACCCCAAUAUCGAAGGGGACUAAAACGAGUCCUAGCAAAAUCAAAGAA', gRNA_seq_list, RBP_data)