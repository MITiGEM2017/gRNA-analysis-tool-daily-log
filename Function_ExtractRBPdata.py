# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 20:02:45 2017

@author: wangq
"""

def extract_RBP_Kd(RBP_data_table, RBP_name):
    for each_RBP in RBP_data_table:
        if(each_RBP[0]==RBP_name):
            return float(each_RBP[1])
    return False

kd_value = extract_RBP_Kd(kd_data_list,"CUG-BP")
