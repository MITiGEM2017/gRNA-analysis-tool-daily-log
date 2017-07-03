# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 19:12:30 2017

@author: wangq
"""

import csv

kd_data_list = []
with open('RBP_binding_affinity_data.csv',"r") as file:
    filereader = csv.reader(file)
    for row in filereader:
        kd_data_list.append(row)

kd_data_list[0][0] = kd_data_list[0][0][-4:]       