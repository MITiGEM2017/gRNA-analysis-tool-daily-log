# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 15:36:52 2017

@author: wangq
"""

fh = open("human.txt","r")

info_list = fh.readlines()


seq = ""

count = 1
for line in info_list:
    if line[0] != ">":
        seq += line[:-1]
    print(count)
    count += 1

text_file = open("human-cDNA.txt", "w")

text_file.write(seq)

text_file.close()