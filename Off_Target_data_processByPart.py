# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 21:09:34 2017

@author: wangq
"""
import csv
from timeit import default_timer as timer
import time
from tqdm import *


off_target_mismatch_threshold = 4
gRNA_length = 22

def diff_letters(a,b):
    return sum ( a[i] != b[i] for i in range(len(a)) )

def off_target_mismatch(mRNA_seq,gRNA_seq):
    crRNA_seq = gRNA_seq[-gRNA_length:]
    print("\n")
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
        
    start_pos = 0
    while start_pos < (len(mRNA_seq)-len(crRNA_seq)+1):
        DNA_seq = mRNA_seq[start_pos:(start_pos+len(crRNA_seq))]
        diff = diff_letters(RNA_complement, DNA_seq)
        if diff <= off_target_mismatch_threshold:
            count +=1
            difference_list.append(diff)
            start_pos += 1

        else:
            start_pos += (diff-off_target_mismatch_threshold)

    return count, difference_list

file = open("human-cDNA.txt","r")
cDNA_seq = file.readline()
off_target_data_output = []

for gRNA in tqdm(gRNA_seq_list[0:200]):
    start = timer()
    num_mismatch, mismatch_list = off_target_mismatch(cDNA_seq,gRNA)
    off_target_gRNA = [num_mismatch, mismatch_list]
    end = timer()
    print("In total:    ", int((end-start)/60),"minute(s) and",(end-start)%60,"second(s) for the gRNA sequence:", gRNA)
    off_target_data_output.append(off_target_gRNA)

with open('Off_target_data_1.csv','w',newline='') as fp:
    a = csv.writer(fp,delimiter=',')
    a.writerows(off_target_data_output)